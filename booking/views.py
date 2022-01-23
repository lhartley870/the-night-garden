from django.shortcuts import render
from django.views import View
from .forms import BookingForm


# Create your views here.
class HomePage(View):
    def get(self, request):
        return render(request, "index.html",)


class BookingFormPage(View):
    def get(self, request):
        return render(
            request,
            "booking_form.html",
            {
                "booking_form": BookingForm(),
            }
        )

    def post(self, request, *args, **kwargs):

        booking_form = BookingForm(data=request.POST)

        return render(
            request,
            "booking_form.html",
            {
                 "booking_form": booking_form,
            }
        )
