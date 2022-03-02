# Testing

## Validators
[The W3C Markup Validation Service](https://validator.w3.org/) was used for testing the html code for the site. As this project uses Django templates, the html was tested by visiting each page of the site, right clicking, selecting 'View page source' and copying and pasting the code shown into the validator. Validation has only been carried out for pages created by the developer and the django allauth templates customised by the developer (namely the login, logout and signup pages).The following results show that no errors have been found: 
* [Home page html](/readme-documents/validation-results/clear-rendered-home-pg-results.png)
* [Register page html](readme-documents/validation-results/clear-rendered-register-pg-results.png)
* [Login page html](readme-documents/validation-results/clear-rendered-login-pg-results.png)
* [Menus page html](readme-documents/validation-results/clear-rendered-menus-pg-results.png)
* [Contact page html](readme-documents/validation-results/clear-rendered-contact-pg-results.png)
* [My Bookings page html with no bookings](readme-documents/validation-results/clear-my-bookings-pg-results-with-no-bookings.png)
* [My Bookings page html with bookings](readme-documents/validation-results/clear-rendered-my-bookings-pg-results-with-bookings.png)
* [Make a Booking page html](readme-documents/validation-results/clear-rendered-make-booking-pg-results.png)
* [Edit a Booking page html](readme-documents/validation-results/clear-rendered-edit-booking-pg-results.png)
* [Logout page html](readme-documents/validation-results/clear-rendered-logout-pg-results.png)

Initially there was an issue with most of the html pages which is highlighted in this result for the initial rendered register page:
* [Initial Register page html](readme-documents/validation-results/initial-rendered-register-pg-results.png)

There was a stray end div closing tag which was removed in all the templates affected.

[The W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used for testing the css code for the site. The following result shows that no errors have been found:
* [style.css file](readme-documents/validation-results/clear-css-result.png) 

[The JSHint Validator](https://jshint.com/) was used for testing the javascript code for the site. The following result shows that no errors have been found:
* [script.js file](readme-documents/validation-results/clear-javascript-results.png)

Initially there were some warnings highlighted in this initial result for the script.js file which were subsequently corrected:
* [Initial script.js file result](readme-documents/validation-results/initial-jquery-results.png)

[The PEP8 Online Validator Service](http://pep8online.com/) was used for testing the python code for the application. The following result shows that no errors have been found: 
* [Python code in run.py file result](/readme-documents/validator-screenshots/validator-clear.png)

Initially when the project was run through the validator the following errors were shown:
+ [Python code in run.py file initial result](/readme-documents/validator-screenshots/validator-warnings.png).

These were all errors for the same issue, stated to be *'line break before binary operator'*. This was resolved by moving the applicable line breaks to after the binary operators, in all cases the binary operator being a '+'.  

## Automated Testing

## Manual Testing

### Browser Testing

The manual testing of the website was carried out on the following devices:

1. Mobile phone (Apple iPhone 11 with a device viewport size of 414px by 896px)
2. Tablet (Apple iPad mini with a device viewport size of 768px by 1024px)
3. Laptop (Apple MacBook Pro with a device viewport size of 1440px by 900px)
4. A large monitor (Asus monitor with a device viewport size of 1920px by 1080px) connected to the MacBook Pro

The website was tested on the following browsers on all of the above devices:

1. [Google Chrome](https://www.google.co.uk/chrome/?brand=FHFK&gclid=EAIaIQobChMI3b-xi9y38QIVBrTtCh2I1g3AEAAYASAAEgJN5vD_BwE&gclsrc=aw.ds)
2. [Microsoft Edge](https://www.microsoft.com/en-us/edge)
3. [Firefox](https://www.mozilla.org/en-GB/firefox/new/)
4. [Safari](https://www.apple.com/uk/safari/) 

The site was created using the Chrome browser and Chrome DevTools and was fully tested in that environment as it was being developed. The site was then further tested after deployment on all of the above devices and browsers.

### Manual Tests

## Contrast Checker Testing

The foreground text colours and their background colours were tested using the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/). The following combinations were tested and all received at least a WCAG AA pass. The results are as follows: 

* The [         ] colour of [       ] (#) was tested against the [] colour (#) of the []:
    * [results]() 

## Fixed Bugs

*  

## Unfixed Bugs

* 
    