from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('make-booking', views.BookingFormPage.as_view(), name='make_booking'),
    path('my-bookings', views.MyBookingsPg.as_view(), name='my_bookings'),
]
