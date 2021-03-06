##script which send reminder notification for all the booked users
##for the hour. This runs eat 00:00 every hour



from datetime import datetime
import django
from booking.models import BookingDetails
from studios.models import StudioProfile
from utils import Responses
from django.contrib.auth.models import User
import logging
import traceback

logger_hrly  = logging.getLogger('log.daily_scripts')
logger_error = logging.getLogger('log.errors')

##get all active bookings for the hour
##get the code,date, time, studio, services
#get mobile number from BookedMessageSend
##get SMS template 
##send SMS
##Make an entry in daily_reminder table with status	


##need to integrate with thread que system when the count overflows in future
def get_hourly_bookings():
	try:
	    today = datetime.today()
        minute_15back  = (datetime.now()- timedelta(minutes = 5))
        now = datetime.now().time()
        minute_5_back = minute_5_back.time()
        bookings = BookingDetails.objects.filter(appointment_date = today,   \
        booking_status = 'BOOKED', status_code = 'B001', appointment_start_time__range =  \
        (minute_5_back , now), is_valid = True)
        ##log code starting
        for every_book in bookings:
            has_sent = HourlyReminder.objects.filter(booking_id = every_book.id, status = False)
            if len(has_sent)  == 0:
        	    code = every_book.booking_code
        	    studio_name = StudioProfile.objects.filter(id = every_book.studio).values('name')
        	    user_name = User.objects.filter(id = every_book.user).values('first_name')
        	    date = today
        	    time = datetime.strptime(str(every_book.appointment_start_time), "%H.%M").strftime("%I:%M %p")
        	    mobile_no = BookedMessageSend.objects.filter(booking_id = every_book.id).values('mobile_no')
        	    sms_template = (Responses.hourly_reminder['sms_template'])%(user_name, studio_name, date, time)
                logger_hrly.info("SMS hourly reminder text- "+str(sms_template))
        	    try:
        	        status = generic_utils.sendSMS(mobile_no,sms_template)
        	    except Exception,smserr:
                    logger_error.error(traceback.format_exc())
        		    status = False
        		    hourly_reminder = HourlyReminder(booking_id = every_book.id, mobile_no = mobile_no,  \
        	    	status = status, service_updated = "daily reminder", message = sms_template,  \
        	    	)
                    hourly_reminder.save()
        	    else:
        		    hourly_reminder = HourlyReminder(booking_id = every_book.id, mobile_no = mobile_no,  \
        	    	status = status, service_updated = "daily reminder", message = sms_template,  \
        	    	)
                    hourly_reminder.save()
    except Exception,errorz:
        logger_error.error(traceback.format_exc())
    else:

        print len(bookings)
        ###log code end stats

get_hourly_bookings()