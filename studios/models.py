#standard library imports
from datetime import datetime
from django.utils import timezone


#third party imports
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#application imports
from user_accounts.models import User



class ServiceType(models.Model):

	"""type of service types available"""
	service_name = models.CharField(max_length = 100,db_index = True)
	description = models.TextField()
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25, default = 'Admin')
	updated_date_time = models.DateTimeField(default = datetime.now())

	def __unicode__(self):
		return self.service_name


class Service(models.Model):

	"""table holding all list of services"""

	service_name = models.CharField(max_length = 100,db_index = True)
	service_type = models.ForeignKey(ServiceType, related_name = "type_of_service",db_index = True)
	#is_dependent = models.BooleanField(default = 0)
	min_duration = models.IntegerField() ##duration in mins
	is_active = models.BooleanField(default = 1)
	#unit_price = models.IntegerField()
	service_for = models.IntegerField(default = 1) #3- unisex, 1- Men 2 -Women
	service_updated = models.CharField(max_length = 25, default = 'Admin')
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.service_name



class StudioManager(BaseUserManager):
	    #method which created studios in studios.studio login table
	    def create_user(self, email, password=None):
	        if not email:
	            raise ValueError('Users must have an email address')
	 
	        user = self.model(
            email=StudioManager.normalize_email(email),
	               )
	 
	        user.set_password(password)
	        user.save(using=self._db)
	        return user
	
	    #method which creates super user in db
	    def create_superuser(self, email, password):
	        user = self.create_user(email,
	            password=password,
	            
	        )
	        user.is_admin = True
	        user.save(using=self._db)
	        return user
	
# Create your models here.
class Studio(AbstractBaseUser):
    
    #custom user model which has email as primary key
	email = models.EmailField(max_length=254)
	is_active = models.BooleanField(default=False)
	last_password_reset_datetime = models.DateTimeField(null = True)
	last_signout_datetime = models.DateTimeField(default = datetime.now(), null = True)
	    
	objects = StudioManager()
	 
	USERNAME_FIELD = 'email'
	    
	 
	def __unicode__(self):
	    return self.email
	 
	def has_perm(self, perm, obj=None):
	    # Handle whether the user has a specific permission?"
	    return True
	 
	def has_module_perms(self, app_label):
	    # Handle whether the user has permissions to view the app `app_label`?"
	    return True


class StudioAddRequest(models.Model):

	"""table holding all data related to studios want to use fairlour.com"""
	studio_name = models.CharField(max_length = 30)
	area = models.CharField(max_length = 50)
	mobile_no= models.CharField(max_length = 20)
	email = models.CharField(max_length = 60)
	service_updated = models.CharField(max_length = 30)
	updated_date_time = models.DateTimeField(default = datetime.now())

class StudioType(models.Model):

	"""type of studios"""
	type_desc = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.type_desc


class StudioGroup(models.Model):

	"""table for holding studio groups"""
	group_name = models.CharField(max_length = 50)
	address = models.TextField()
	city = models.CharField(max_length = 40, default = 'Chennai')
	country = models.CharField(max_length = 40, default = 'India')
	contact_no = models.CharField(max_length = 40, blank = True)
	#landline_no_2 = models.CharField(max_length = 40, null = True)
	#mobile_no_1 = models.CharField(max_length = 40)
	#mobile_no_2 = models.CharField(max_length = 40, null = True)
	#contact_person_1 = models.CharField(max_length = 75)
	#contact_person_2 = models.CharField(max_length = 75, null = True)
	primary_email  = models.CharField(max_length = 50, blank = True)
	#secondary_email = models.CharField(max_length = 50)
	#total_branches = models.PositiveIntegerField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.group_name
	
class StudioKind(models.Model):
	"""what kind of studio it is Men,Women,UNisex,Women and Child"""
	kind_desc = models.CharField(max_length = 20)
	is_active = models.BooleanField(default = 1)
	updated_date_time = models.DateTimeField(default = datetime.now())
	service_updated = models.CharField(max_length = 25)
	def __unicode__(self):
		return self.kind_desc

class StudioProfile(models.Model):

	"""studio basic details"""
	studio = models.OneToOneField(Studio, related_name = "studio_login")
	studio_type = models.ForeignKey(StudioType, related_name = "studio_type")
	studio_group = models.ForeignKey(StudioGroup, related_name = "studio_of_group")
	name = models.CharField(max_length = 120)
	address_1 = models.CharField(max_length = 200)
	address_2 = models.CharField(max_length = 200)
	landmark = models.CharField(max_length = 200, blank = True)
	city = models.CharField(max_length = 40, default = 'Chennai')
	country = models.CharField(max_length = 40 , default = 'India')
	area = models.CharField(max_length = 100 )
	state = models.CharField(max_length = 40, default = 'Tamil nadu')
	search_field_1 = models.CharField(max_length = 200)
	search_field_2 = models.CharField(max_length = 200)
	landline_no_1 = models.CharField(max_length = 40, blank = True, null = True)
	landline_no_2 = models.CharField(max_length = 40, blank = True, null = True	)
	incharge_mobile_no = models.CharField(max_length = 40)
	contact_mobile_no = models.CharField(max_length = 40, blank = True, null = True)
	in_charge_person = models.CharField(max_length = 75)
	contact_person  = models.CharField(max_length = 75, blank = True, null = True)
	opening_at = models.TimeField(null = True)
	closing_at = models.TimeField(null = True)
	is_active = models.BooleanField(default  = 1)
	#contract_start_date = models.DateTimeField()
	#contract_end_date = models.DateTimeField()
	is_closed = models.BooleanField(default = 0)
	#serve_type = models.CharField(max_length = 10)# men women unisex
	daily_studio_closed_from = models.TimeField(null = True,blank = True)
	daily_studio_closed_till = models.TimeField(null = True,blank = True)
	thumbnail= models.ImageField(upload_to = 'img_gallery')
	is_ac = models.BooleanField(default = 0)
	studio_kind = models.ForeignKey(StudioKind, related_name = "kind_of_studio")
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	latitude = models.CharField(max_length = 30)
	longitude = models.CharField(max_length = 30)
	has_online_payment = models.BooleanField(default = 1)
	commission_percent = models.IntegerField(default = 10)
	has_service_tax = models.FloatField(default = 15) #15- has 0- no

	def update(self):
		for field in self._meta.fields:
			if field.name == 'thumbnail':
				field.upload_to = 'img_gallery/%d' % self.id
		super(StudioProfile, self).save()
    

	def __unicode__(self):
		return str(self.name +'--'+self.area)
	"""def save(self):
		for field in self._meta.fields:
			if field.name == 'thumbnail':
			   field.upload_to = 'img_gallery/%d' % self.id
        super(Studio, self).save()"""
    
""""
class Amenities(models.Model):
	list of all amenities
	amenity_name= models.CharField(max_length = 30)
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.amenity_name

class StudioAmenities(models.Model):
	list of available amenities in studio
	studio_profile = models.ForeignKey(StudioProfile, related_name = "studio_amenities")
	amenity = models.ForeignKey(Amenities, related_name = "amenity_available")
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())"""

class StudioServiceTypes(models.Model):
	"""list of available activities in studio"""

	studio_profile = models.ForeignKey(StudioProfile, related_name = "studio_detail_for_service_type",db_index = True)
	service_type = models.ForeignKey(ServiceType, related_name = "service_type_in_studio",db_index = True)
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class StudioServices(models.Model):

	"""list of available activities in studio"""

	studio_profile = models.ForeignKey(StudioProfile, related_name = "studio_detail_for_activity",db_index = True)
	service = models.ForeignKey(Service, related_name = "service_in_studio",db_index = True)
	is_active = models.BooleanField(default = 1)
	mins_takes = models.PositiveIntegerField()
	price = models.FloatField()
	#service_for = models.IntegerField(default = 1) #3- unisex, 1- Men 2 -Women
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())

""""
class StudioStaffCounts(models.Model):

	table holding studio staff count on normal day and holiday day
	studio_profile = models.OneToOneField(StudioProfile, related_name = "studio_staff_count")
	normal_day = models.PositiveIntegerField()
	holiday = models.PositiveIntegerField()
	festive_season = models.PositiveIntegerField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())"""

""""
class PaymentModes(models.Model):

	payment modes available

	mode = models.CharField(max_length = 40)
	description = models.CharField(max_length = 75)
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.mode"""


class StudioAccountDetails(models.Model):

	"""studio bank and payment details"""
	studio = models.OneToOneField(StudioProfile, related_name = "studio_account_detail")
	#mode_of_payment = models.ForeignKey(PaymentModes, related_name = "payment_mode_for_studio_account")
	bank_name = models.CharField(max_length = 120)
	bank_branch = models.CharField(max_length = 120)
	bank_ifsc = models.CharField(max_length = 25)
	bank_city = models.CharField(max_length = 40)
	bank_acc_number = models.CharField(max_length = 120)
	name = models.CharField(max_length =300)
	#min_deposit = models.PositiveIntegerField()
	#max_deposit = models.PositiveIntegerField()
	#transaction_percent = models.PositiveIntegerField()
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class StudioPayment(models.Model):

	"""all payement details for a studio"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_payment_detail")
	#mode_of_payment = models.ForeignKey(PaymentModes, related_name = "payment_mode_for_studio_payments")
	amount_paid = models.PositiveIntegerField()
	paid_by = models.CharField(max_length = 120) ##has to be foreign key in future
	paid_date = models.DateTimeField(default = datetime.now())
	disputed = models.BooleanField(default = 0) # 1 - disputed
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class StudioBookingDetails(models.Model):

	"""all booking details for studio"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_booking_detail")
	amount_to_be_paid = models.FloatField()
	total_booking = models.PositiveIntegerField()
	fee_amount = models.FloatField()
	invoice_date = models.DateField(default = datetime.now().date())
	total_booking_amount = models.FloatField()
	service_tax_amount = models.FloatField()
	service_updated = models.CharField(max_length = 50)
	updated_date_time = models.DateTimeField(default = datetime.now())


class StudioInvoices(models.Model):

	"""all invoice details for studio"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_invoice_detail")
	amount_to_be_paid = models.FloatField()
	total_booking = models.PositiveIntegerField()
	fee_amount = models.FloatField()
	invoice_date = models.DateField(default = datetime.now().date())
	total_booking_amount = models.FloatField()
	service_tax_amount = models.FloatField()
	service_updated = models.CharField(max_length = 50)
	updated_date_time = models.DateTimeField(default = datetime.now())

class StudioPasswordReset(models.Model):

	"""all password resets for studio"""

	studio = models.ForeignKey(Studio, related_name = "studio_pwd_reset")
	password_changed_date = models.DateTimeField(default = datetime.now())
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())


class CloseDates(models.Model):

	"""general closed days for studios"""
	closed_on_day = models.CharField(max_length = 25)
	closed_on_desc = models.CharField(max_length = 50)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())
	def __unicode__(self):
		return self.closed_on_day


class StudioClosedDetails(models.Model):

	"""days on which the studio is closed"""
	studio = models.ForeignKey(StudioProfile, related_name = "studio_closed_details",db_index = True)
	closed_on = models.ForeignKey(CloseDates, related_name = "studio_close_dates")
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())

"""
class StudioClosedFromTill(models.Model):

	if studio is closed for to many days
	studio = models.ForeignKey(StudioProfile, related_name = "studio_long_closed_details")
	closed_from_date = models.DateField()
	closed_till_date = models.DateField()
	is_active = models.BooleanField(default = 1)
	service_updated = models.CharField(max_length = 25)
	updated_date_time = models.DateTimeField(default = datetime.now())"""





class StudioPicture(models.Model):

    """studios and its pictures"""
    studio_profile  = models.ForeignKey(StudioProfile, related_name = "pic_of_studio",db_index = True)
    picture = models.ImageField(upload_to = 'img_gallery', null = True, blank = True)
    service_updated = models.CharField(max_length = 25)
    updated_date_time = models.DateTimeField(default = datetime.now())

    def save(self):
        for field in self._meta.fields:
            if field.name == 'picture':
                field.upload_to = 'img_gallery/%d' % self.studio_profile_id
        super(StudioPicture, self).save()















