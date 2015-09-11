##script which send reports to all merchants about the booking
##they had previous day.The script should run every day 6AM


#standard library imports
from datetime import datetime
import logging
import traceback

#third party imports
import os,sys
import django
sys.path.append(os.path.join(os.path.dirname(__file__), 'onepass'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onepass.settings")
django.setup()


from django.contrib.auth.models import User
from django.db import transaction
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from django.core.files import File
from django.db import transaction

#application imports
from booking.models import BookingDetails,BookingServices,MerchantDailyReportStatus, DailyBookingConfirmation
from studios.models import StudioProfile, Studio,StudioInvoices
from utils import responses, generic_utils


logger_booking = logging.getLogger('log.daily_scripts')
logger_error = logging.getLogger('log.errors')


""""
--------------------------------------------------------------------------------------------------------------
Name | Mobile | Booking id | Services Booked | From Time | To Time | Booking Code | Booking Amount | Mark Used  
--------------------------------------------------------------------------------------------------------------
"""

today = datetime.today().date()
till_hour = datetime.now().hour
till_time = None
buks = None
def daily_confirmed_booking():
    try:
        ##get all used booking for the day
        time = datetime.now().replace(hour = 13, minute = 00)
        global till_time,today
        if till_hour < 13:
            till_time = time.time().replace(hour = 13, minute = 00)
            bookings = BookingDetails.objects.filter( appointment_date = today, \
            booking_status = 'BOOKED', status_code = 'B001', is_valid = True,  \
            appointment_start_time__lt = time)
        else:
            till_time = time.time().replace(hour = 23, minute = 59)
            bookings = BookingDetails.objects.filter( appointment_date = today,  \
            booking_status = 'BOOKED', status_code = 'B001', is_valid = True,  \
            appointment_start_time__gte = time)
        studios_visited = []
        to_print = {}
        for stud in bookings:
            #if stud not in studios_visited:
            try:
                services_booked = BookingServices.objects.filter(booking_id = \
                 stud.id)
                services = []
                for sun in services_booked:
                    services.append(sun.service.service_name)
                obx = {}
                obx['data'] = []
                obj = {}
                obj['booking_id'] = stud.id
                obj['user'] = stud.user.first_name
                obj['services_booked'] = services[:]
                obj['appointment_date'] = today
                obj['appointment_start_time'] = stud.appointment_start_time
                obj['appointment_end_time'] = stud.appointment_end_time
                obj['booking_code'] = stud.booking_code
                obj['booking_amount'] = stud.purchase.purchase_amount
                obj['actual_amount'] = stud.purchase.actual_amount
                obj['mobile_no'] = stud.mobile_no
                obx['data'].append(obj)
                if stud.studio_id not in studios_visited:
                    obx['studio_id'] =  stud.studio_id
                    obx['studio_name'] = stud.studio.name
                    obx['studio_address1'] = stud.studio.address_1
                    obx['studio_address2'] = stud.studio.address_2
                    obx['studio_area'] = stud.studio.area
                    obx['studio_city'] = stud.studio.city
                    obx['account_number'] = stud.studio.studio_account_detail.bank_acc_number
                    obx['bank_name'] = stud.studio.studio_account_detail.bank_name
                    obx['ifsc_code'] = stud.studio.studio_account_detail.bank_ifsc
                    obx['total_amount'] = obj['booking_amount']
                    obx['total_booking_amount'] = stud.purchase.actual_amount
                    obx['paid_amount'] = obj['booking_amount'] -  \
                    (obj['booking_amount']/int(stud.studio.commission_percent))
                    obx['fee_amount'] =  obx['total_booking_amount'] - obx['paid_amount']
                    studios_visited.append(stud.studio_id)
                    to_print[stud.studio_id] = obx
                else:
                    to_print[stud.studio_id]['total_booking_amount'] = to_print[stud.studio_id]['total_booking_amount'] +  \
                    stud.purchase.actual_amount
                    to_print[stud.studio_id]['total_amount'] = to_print[stud.studio_id]['total_amount'] +  \
                        obj['booking_amount']
                    to_print[stud.studio_id]['paid_amount'] =  (to_print[stud.studio_id]['paid_amount']  \
                        + obj['booking_amount'] -  \
                    (obj['booking_amount']/int(stud.studio.commission_percent)))
                    to_print[stud.studio_id]['fee_amount'] = to_print[stud.studio_id]['total_booking_amount'] -  \
                    to_print[stud.studio_id]['paid_amount'] 
                    to_print[stud.studio_id]['data'].append(obj)
            except Exception,jsonerr:
                logger_error.error(traceback.format_exc())
    except Exception,majErr:
        logger_error.error(traceback.format_exc())
    else:
        logger_booking.info(" data to render  "+str(to_print))
        return to_print

@transaction.commit_manually
def render_to_pdf(template_url,data,studio):
    ##generate pdf with data
    #import pdb;pdb.set_trace();
    try:
        global till_time,today
        template = get_template(template_url)
        data['todayslist']['date'] = today
        data['todayslist']['time'] = till_time
        print data
        context = Context(data)
        html =  template.render(context)
        filename = data['todayslist']['studio_name'] + str(datetime.today().date())+"__bookings"
        result = open(filename+'.pdf', 'wb')
        #result = StringIO.StringIO()
        logger_booking.info("File name "+str(filename))
        logger_booking.info("File name "+str(data))
        try:
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        except:
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding="UTF-8")
        result.close()
        if not pdf.err:
            ###get and save the pdf 
            file_ = open(filename+'.pdf', 'r')
            pdf = File(file_)
            rep = DailyBookingConfirmation(studio_id = studio, booking_pdf = pdf,  \
                service_updated = "studio report sender")
            rep.save()
            studio_dt = StudioProfile.objects.values('studio').get(id = studio)
            studio_email = Studio.objects.values('email').get(id = studio_dt['studio'])
            try:
                #send email
                message  = "Please find the booking data"
                subject = (responses.MAIL_SUBJECTS['DAILY_BOOKING_MAIL'])%(today)
                generic_utils.sendEmail('vbnetmithun@gmail.com',subject,message,filename+'.pdf')
                #generic_utils.sendEmail(studio_email['email'],subject,message)
                rep = DailyBookingConfirmation.objects.filter(studio_id = studio, report_date = \
                 today).update(mail_sent = 1, updated_date_time = datetime.now())
            except Exception,e:
                logger_error.error(traceback.format_exc())
            ##save pdf to table
            ##location should be inside studio
            file_.close();
    except Exception,pdfrenderr:
        transaction.rollback()
        logger_error.error(traceback.format_exc())
    else:
        transaction.commit()


def generate_pdf():
    to_generate = daily_confirmed_booking()
    global buks
    buks = len(to_generate)
    logger_booking.info("Sent mails to %s  studios - "%(str(buks)))
    for key,data in to_generate.iteritems():
        try:
            stud_invoice = StudioInvoices(studio_id = data['studio_id'],  \
                amount_to_be_paid = data['total_booking_amount'],  \
                total_booking = len(data['data']), fee_amount = data['fee_amount'],  \
                total_booking_amount = data['total_amount'])
            stud_invoice.save()
            data['invoice_id'] =    stud_invoice.id
            logger_booking.info("data to be rendered - "+str(key)+"---"+str(data))
            pdf_file = render_to_pdf('../templates/emails/daily_confirmed_bookings.html',  \
               {'pagesize':'A4','todayslist':data},key)
        except Exception,pdfgenrateerr:
            logger_error.error(traceback.format_exc())

     
logger_booking.info("Confirmed booking script starts running  "+datetime.strftime(datetime.now(),  \
            '%y-%m-%d %H:%M'))
generate_pdf()
message = "Sent mails to %s  studios"%(str(buks))
generic_utils.sendEmail('vbnetmithun@gmail.com', 'Daily report script run sucessfull',message)
logger_booking.info("Confirmed booking script stops running  "+datetime.strftime(datetime.now(),  \
            '%y-%m-%d %H:%M'))





