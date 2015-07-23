
#standard library imports
from datetime import datetime

#third party imports
from django.conf import settings
from django.db import models
from django.utils import timezone

#application imports
from user_accounts.models import User
from studios.models import StudioProfile, Service




class Purchase(models.Model):

	"""table holding details of all the purchases made"""
	customer = models.ForeignKey(User, related_name = "user_who_purchased")
	purchase_amount = models.FloatField()
	actual_amount = models.FloatField()
	purchase_status = models.CharField(max_length = 30)
	status_code = models.CharField(max_length = 10)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class Coupon(models.Model):
	"""table contaning all coupon details"""

	coupon_code = models.CharField(max_length = 10)
	expiry_date = models.DateTimeField()
	for_all_studios = models.BooleanField()
	#is_service_level = models.BooleanField()
	maximum_discount = models.PositiveIntegerField()
	is_one_time = models.BooleanField()
	is_active = models.BooleanField()
	coupon_type = models.CharField(max_length = 10)
	discount_value = models.PositiveIntegerField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	

class CouponForStudios(models.Model):

	"""table for coupon applicable studios,if for_all_studios is 0"""
	coupon = models.ForeignKey(Coupon, related_name = "coupon_for_studio")
	studio = models.ForeignKey(StudioProfile, related_name = "studio_have_coupon")
	is_active = models.BooleanField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class BookingDetails(models.Model):

	"""table holding all booking related infos"""
	user = models.ForeignKey(User, related_name = "booked_by_user")
	booked_date = models.DateTimeField()
	appointment_date = models.DateField()
	appointment_start_time = models.TimeField() # ex 13.15 14.30
	appointment_end_time = models.TimeField() # ex 13.15 14.30
	mobile_no = models.CharField(max_length = 30, null = True)
	booking_code = models.CharField(max_length = 25)
	studio = models.ForeignKey(StudioProfile, related_name = "booked_on_studio")
	coupon = models.ForeignKey(Coupon, related_name = "applied_promo_code", null = True)
	status_code = models.CharField(max_length = 10)
	booking_status = models.CharField(max_length = 30)
	notification_send  = models.BooleanField(default = 0)
	is_valid = models.BooleanField(default = 1) #0- new 1-postponed
	purchase = models.ForeignKey(Purchase, related_name = "purchase_id", null = True)
	#total_duration = models.PositiveIntegerField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())

class Refund(models.Model):

	"""table holding all refund data"""
	user = models.ForeignKey(User, related_name = "refund_to_user")
	purchase = models.ForeignKey(Purchase, related_name = "refund_from_purchase")
	booking = models.ForeignKey(BookingDetails, related_name = "refund_of_booking")
	status = models.CharField(max_length = 20)
	status_code = models.CharField(max_length = 20)
	amount_refunded = models.FloatField()
	initiated_date_time = models.DateTimeField(datetime.now())
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class BookedMessageSent(models.Model):

	"""table holds whether booked/cancelled message sent to 
	mobile/email both for user and studio"""

	booking = models.ForeignKey(BookingDetails, related_name = "booking_id")
	message = models.TextField(null = True)
	is_successful = models.BooleanField(default = 0)
	type_of_message = models.CharField(max_length = 25) ##book and cancel message
	mode = models.CharField(max_length = 25) ## mobile and email
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())

class BookingServices(models.Model):

	"""table for services booked for a booking id"""
	booking = models.ForeignKey(BookingDetails, related_name = "service_booked_with")
	service = models.ForeignKey(Service, related_name = "service_booked")
	status = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())

class Payments(models.Model):

	"""table holding all payment related infos"""
	amount_paid = models.FloatField()
	initiated_time = models.DateTimeField(default = datetime.now())
	confirmation_time = models.DateTimeField(default = datetime.now())
	payment_status = models.CharField(max_length = 30)
	purchase = models.ForeignKey(Purchase, related_name = "purchase_id_payment")


class StudioReviews(models.Model):

	"""reviews for studio"""
	studio_profile = models.ForeignKey(StudioProfile, related_name = "studio_review")
	user = models.ForeignKey(User, related_name = "reviewed_by_user")
	booking = models.ForeignKey(BookingDetails, related_name = "reviewed_on_booking")
	#service = models.ForeignKey(Service, related_name = "reviewed_the_service", null = True)
	rating = models.PositiveIntegerField()
	comment = models.TextField()
	is_active = models.BooleanField(default = 1)
	has_reviewed = models.BooleanField(default = 0)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class MerchantDailyReportStatus(models.Model):

	"""table holding all information status for reports sent to merchants"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_report")
	report_date = models.DateField(default = datetime.now().date())
	report = models.FileField(upload_to = 'reports/%Y/%m/%d')
	mail_sent = models.BooleanField(default = 0)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class DailyReminder(models.Model):

	"""table holding all daily booking reminders sent"""
	booking = models.ForeignKey(BookingDetails, related_name = "dr_for_booking")
	mobile_no = models.CharField(max_length = 30)
	status = models.BooleanField(default = 1)
	message = models.TextField()
	service_updated = models.CharField(max_length = 30)
	user = models.ForeignKey(User, related_name = "dr_for_user")
	updated_date_time = models.DateTimeField(default = datetime.now())



class HourlyReminder(models.Model):

	"""table holding all hourly booking reminders sent"""
	booking = models.ForeignKey(BookingDetails, related_name = "hr_reminder_for_booking")
	mobile_no = models.CharField(max_length = 30)
	status = models.BooleanField(default = 1)
	message = models.TextField()
	service_updated = models.CharField(max_length = 30)
	user = models.ForeignKey(User, related_name = "hr_for_user")
	updated_date_time = models.DateTimeField(default = datetime.now())


class ThanksMail(models.Model):

	"""table holding all details of thanks mail sent"""
	booking = models.ForeignKey(BookingDetails, related_name = "tm_for_booking")
	email = models.CharField(max_length = 60)
	status = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 30)
	user = models.ForeignKey(User, related_name = "tm_for_user")
	updated_date_time = models.DateTimeField(default = datetime.now())



class DailyBookingConfirmation(models.Model):

	"""table holding all information status for reports sent to merchants"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_confirmed_booking")
	report_date = models.DateField(default = datetime.now().date())
	booking_pdf = models.FileField(upload_to = 'reports/%Y/%m/%d')
	mail_sent = models.BooleanField(default = 0)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class ReviewLink(models.Model):

	"""table to validate whether the user is allowed to write review when clicked on 
	review link"""
	booking = models.ForeignKey(BookingDetails, related_name = "review_link_of_booking")
	is_reviewed = models.BooleanField(default = 0)
	link_code = models.CharField(max_length = 50)
	updated_date_time = models.DateTimeField(default = datetime.now())
	service_updated = models.CharField(max_length = 30)