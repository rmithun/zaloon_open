#standard library imports


#third party imports
from rest_framework import serializers

#application imports
from models import *
#from studios.serializers import StudioProfileSerializer
#from user_accounts.serializers import UserNameOnlySerializer
from studios.serializers import StudioProfileBookingSerializer, ServiceSerializer

class ServicesBooked(serializers.ModelSerializer):

    service = ServiceSerializer()
    class Meta:
		model = BookingServices
		fields = ('service',)

class ActiveBookingSerializer(serializers.ModelSerializer):

	"""list of available active bookings for user"""
	#studio = StudioProfileSerializer(many = True)
	service_booked_with = ServicesBooked(many = True)
	studio = StudioProfileBookingSerializer()
	class Meta:
		model = BookingDetails
		fields = ('id', 'user', 'booked_date', 'appointment_date', 'appointment_start_time',  \
			'booking_code','studio','booking_status', 'status_code', \
			'service_booked_with','appointment_end_time','is_reviewed','booking_date')

class CouponSerializer(serializers.ModelSerializer):

	class Meta:
		model = Coupon
		fields = ('coupon_code','expiry_date','is_one_time','is_active', \
			'coupon_type','discount_value','for_all_studios','min_booking_amount')

class EmailReviewLinkSerializer(serializers.ModelSerializer):

	class Meta:
		model = ReviewLink
		fields = ('id','booking_id','link_code','is_reviewed')