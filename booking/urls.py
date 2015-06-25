from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onepass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^services/$', views.ServiceDetails.as_view(), name = 'services'),
    #url(r'^search/$', views.SearchResults.as_view(), name = 'search'),
    url(r'^my_booking/$', views.GetActiveBookings.as_view(), name = 'my_booking'),
    url(r'^cancel_booking/$', views.CancelBooking.as_view(), name = 'cancel_booking'),
    url(r'^validate_code/$', views.ValidateBookingCode.as_view(), name = 'validate_code'),
    url(r'^get_booking/$', views.ValidateBookingCode.as_view(), name = 'get_booking'),
    url(r'^add_review/$', views.AddReviews.as_view(), name = 'add_review'),



)
