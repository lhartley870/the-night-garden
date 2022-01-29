from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    # The solution of using the login_required decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    #
    # The solution of using the login_required decorator in the url path
    # for class-based views was taken from an answer given by FMZ on this
    # Stack Overflow post -
    # https://stackoverflow.com/questions/28555260/django-login-required-for-class-views
    path('make-booking', login_required(views.BookingFormPage.as_view()),
         name='make_booking'),
    path('my-bookings', login_required(views.MyBookingsPg.as_view()),
         name='my_bookings'),
]
