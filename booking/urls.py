from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
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
    path('make-booking', login_required(views.MakeBooking.as_view()),
         name='make_booking'),
    path('my-bookings', login_required(views.MyBookings.as_view()),
         name='my_bookings'),
    path('edit-booking/<int:booking_id>',
         login_required(views.EditBooking.as_view()),
         name='edit_booking'),
    path('cancel-booking/<int:booking_id>',
         views.CancelBooking.as_view(),
         name='cancel_booking'),
    path('menus', views.Menus.as_view(), name='menus'),
]
