// wait for the DOM to finish loading before adding interactivity
$(document).ready(function() {
    addDatepicker();
    displayDateFieldErrors();
    fadeOutAlerts();
});

/**
 * This function adds a Gijgo datepicker to the date field of the booking form
 * on the Make a Booking and the Edit a Booking pages.
 */
function addDatepicker() {
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
            new Date(2023, 0, 01),
        ],
        format: 'yyyy-mm-dd',
        iconsLibrary: 'fontawesome',
        // earliest date the user can book will be the date the user visits the page to make a booking
        minDate: function() {
            let date = new Date();
            return new Date(date.getFullYear(), date.getMonth(), date.getDate());
        },
        // latest date the user can book will be approximately 3 months from the date the user visits the page
        maxDate: function() {
            let date = new Date();
            date.setDate(date.getDate()+93);
            return new Date(date.getFullYear(), date.getMonth(), date.getDate());
        },
        uiLibrary: 'bootstrap4',
    });
}

/**
 * This function is necessary to make sure that any errors for the date field in the booking form on the
 * Make a Booking and Edit a Booking pages can be seen by the user as without this function, error messages are
 * not visible due to the inclusion of the datepicker and the way it changes the usual form structure.
 */
function displayDateFieldErrors() {
    let date_error = $('#error_1_id_date').html();

    if (date_error !== undefined) {
        $('#div_id_date').after(`<p id="date-error">${date_error}</p>`);
        $('#date-error').addClass("error-feedback");
        $('.gj-datepicker').addClass("error-container");
    }
}

/**
 * This function fades out success alerts.
 */
function fadeOutAlerts() {
    $(".alert-success").fadeTo(9000, 0).slideUp(500);
}