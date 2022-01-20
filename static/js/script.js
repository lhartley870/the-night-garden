// wait for the DOM to finish loading before adding booking form interactivity
// add a Gijgo datepicker to the date field of the booking form
$(document).ready(function() {
    /* configuration for the Gijgo datepicker and the minDate and maxDate function
    code taken and adapted from the gijgo website - https://gijgo.com/ */
    $('#id_date').datepicker({
        // prevents users booking on Mondays and Tuesdays when the restaurant is closed
        disableDaysOfWeek: [1, 2],
        // prevents users booking when the restaurant is closed over the Christmas period
        disableDates: [
            new Date(2022, 11, 24),
            new Date(2022, 11, 25),
            new Date(2022, 11, 28),
            new Date(2022, 11, 29),
            new Date(2022, 11, 30),
            new Date(2022, 11, 31),
            new Date(2023, 00, 01),
        ],
        format: 'yyyy-mm-dd',
        iconsLibrary: 'fontawesome',
        // earliest date the user can book will be the date the user visits the page to make a booking
        minDate: function() {
            let date = new Date();
            date.setDate(date.getDate()-1);
            return new Date(date.getFullYear(), date.getMonth(), date.getDate());
        },
        // latest date the user can book will be approximately 3 months from the date the user visits the page
        maxDate: function() {
            let date = new Date();
            date.setDate(date.getDate()+93);
            return new Date(date.getFullYear(), date.getMonth(), date.getDate());
        }
    });
});