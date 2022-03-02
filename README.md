# The Night Garden
The Night Garden is a website for an outdoor restaurant serving evening meals in a garden setting based in Cardiff. 

Users that do not have an account with the site can view details about the restaurant on the Home page, the Menus page and the Contact page. They also have access to a registration page in order to create an account. Registered users can login to their account via the login page which gives them access to a 'My Bookings' page showing all of their bookings, from which they can edit or delete bookings. They also have access to a 'Make a Booking' page where they can make new restaurant bookings for up to 10 guests. 

The site's admin user can manage the restaurant tables and time slots for sittings. The admin decides which tables are made available for which time slots. The Admin user can also make bookings for users (this would be primarily for making large bookings of over 10 guests or for special events where the whole restaurant may be booked out for a user over several time slots). The Admin can also approve bookings for users. The booking system automatically checks whether there is table availability for a booking and books the best table configuration but the Admin has the final say over approving bookings e.g. if a user wants to book for 2 guests and they have been allocated an 8 person table by the booking system because that is the only available table for their chosen date and time slot, the Admin may not want to approve the booking. 

The live project can be viewed [here](https://the-night-garden.herokuapp.com/). 

![Responsive view of live website Home page](/readme-documents/screenshots/home-pg-screenshot.png)

## Restaurant Business Model
The restaurant is currently designed to have an intimate feel and so only holds a maximum of 32 guests at any one time. As a new restaurant, the owners have decided to have 2 hour 'sittings' at 5:30pm, 6pm, 7:30pm, 8pm, 9:30pm and 10pm with set menus for the chefs to better plan and manage meals and to see how the restaurant is initially received. These time slots may change in the future. There is a maximum of 16 guests per sitting to avoid the restuarant having more than 32 guests at any one time.

The restaurant only wants guests to be able to make bookings via the website for up to 10 people. Any larger bookings are to be booked through the restaurant admin. If a user wants to book for a party of between 11 and 16 guests then the restaurant admin staff can make this booking for them. If a user wants to book out the restaurant for a special event, the staff need to be able to book out multiple overlapping time slots for that user. The restaurant wants to maintain control of large and special event bookings and so does not want users to be able to change or cancel these types of bookings through the website although the website should show a user's large or special event bookings on their 'My Bookings' page when they are logged in. A user would have to contact the restuarant by email or phone to make any changes to or cancel large or special event bookings.

At the moment the restaurant has purchased enough chairs and tables to cover 32 guests being seated at any one time. They have purchased 5 x 2 person tables, 2 x 4 person tables, 1 x 6 person table and 1 x 8 person table. Any of the tables can be pushed together to make larger tables but obviously larger tables such as the 8 person table cannot be split up into smaller tables. The restaurant has already decided which tables will be allocated to which time slots although this may change in the future.

The restaurant has decided to close on Mondays and Tuesdays at the moment and, in terms of holidays, to only close over the Christmas period from and including 24 December until the first non-public holiday working day after New Year that is not a Monday or Tuesday. These holiday dates are fixed for now but may change in the future as the restaurant finds its feet and determines what opening times and dates suit it best.

## UX (User Experience) 
### User Stories
* 1: Admin Management of Restaurant Tables
As a Site Admin I can create, read, update, delete and filter the restaurant tables so that I can manage the size and number of tables available for guests to book.
* 2: Admin Management of Restaurant Time Slots
As a Site Admin I can create, read, update, delete and filter the restaurant time slots so that I can manage the time slots available for guests to book and which tables are available for those time slots.
* 3: Admin Management of Restaurant Bookings
As a Site Admin I can create, read, update, delete and filter the restaurant bookings so that I can manage large bookings and events and see the status of the bookings at any given time.
* 4: Admin can approve guest bookings
As a Site Admin I can approve or decide not to approve guest bookings so that I can manage the bookings, particularly if a user has been allocated a large table for a small number of guests.
* 5: User can register for an account and login
As a Site User I can register to create an account so that I can make restaurant bookings, view my bookings and manage my bookings.
* 6: User must provide details required by the restaurant on registration
As a Site Admin I can require users to provide an email address and their first and last names on registration so that I can contact users if required and can address them by name when contacting them.
* 7: User can create a new booking 
As a Site User I can make bookings at The Night Garden restaurant so that I have a dining reservation
* 8: User cannot make more than one booking per date/edit a booking to have more than one booking per date
As a Site Admin I can prevent a user making more than one booking per day/editing a booking to have more than one booking per day so that large events for one User are within the control of the Site Admin.
* 9: User cannot make a booking/edit a booking for today for a time in the past 
As a Site Admin I can prevent a user making a booking today/editing a booking for today for a time in the past so that I only receive valid bookings for the restaurant and minimise user error.
* 10: User cannot make a booking/edit a booking if there are not enough free tables to seat the guests
As a Site User I can prevent a user from making a booking/editing a booking if there are not enough free tables to seat the guests so that the restaurant does not get overbooked.
* 11: User can edit an existing booking
As a Site User I can edit an existing booking so that I have flexibility to change my bookings if my circumstances change.
* 12: User cannot edit another user's booking
As a Site Admin I can prevent a user from editing another user's booking so that user's bookings are secure.
* 13: User can delete a booking
As a Site User I can delete a booking that I have made so that so that I have flexibility to cancel my bookings if my circumstances change.
* 14: User can view their current bookings
As a Site User I can view my current bookings so that I can see which bookings I have currently made and whether or not they have been approved.
* 15: Table selection where only 1 table is available or only 1 table is a match
As a Site Admin I can control allocation of tables where only one table is available for a user's booking or only one table is a match so that I can ensure the most optimised allocation of tables for a booking.
* 16: Table selection where no one table is a match and all tables are larger in size than the number of guests for the booking
As a Site Admin I can control allocation of tables where no one table is a match for the user's booking and all tables are larger in size than the number of guests for the booking so that I can ensure the most optimised allocation of tables for a booking.
* 17: Table selection where no one table is a match and all tables are smaller in size than the number of guests for the booking.
As a Site Admin I can control allocation of tables where no one table is a match for the user's booking and all tables are smaller in size than the number of guests for the booking so that I can ensure the most optimised allocation of tables for a booking.
* 18: Table selection where no one table is a match and some tables are smaller and some are larger than the number of guests for the booking.
As a Site Admin I can control allocation of tables where no one table is a match for the user's booking and some tables are smaller in size than the number of guests for the booking and some are larger so that I can ensure the most optimised allocation of tables for a booking.
* 19: Site Navigation
As a Site User I can easily navigate the site so that I can find exactly what I want quickly.
* 20: Site Appearance and Imagery
As a Site User, I can see a comforting familiar layout as I explore the site with an attractive colour scheme and imagery so that I can be inspired by and interested in visiting The Night Garden restaurant.
* 21: Site Menu Information
As a Site User I can view and download the menus for the restaurant so that I know if I want to register with the site to book a table and eat there.

## Features
### Existing Features

### Further Feature Ideas
* At the moment if a Site Admin user does not want to approve a user's booking, they would have to contact the user manually by email to let them know that their booking was not approved before deleting it. It would be good to have an automated mechanism whereby the Site Admin could click on a button to say that they want to delete a particular booking for a particular reason and an appropriate email template would be automatically generated and sent to the user using their email address saved in the database. A bonus would be to have a mechanism that also displays a message to the user on their 'My Bookings' page to explain why the booking has been refused. The mechanism could then automatically delete the booking from the database.
* At the moment the closed Christmas holiday dates have been manually entered into the code itself. A mechanism would need to be included to generate the closed Christmas dates for each year rather than just for Christmas 2022. Ideally the Site Admin would be able to enter closed dates via the Admin panel for these to be communicated to the application so that the user would be prevented from selecting such dates in the datepicker. Giving the Site Admin control in the Admin panel would be ideal as the Site Admin could enter closed dates other than for the Christmas period/change closed dates as required. 
* Rather than the user having to click on 'Make a Booking' for the system to check whether there are enough free tables to accommodate the number of guests and the user receiving feedback that their booking is unavailable if there are not enough free tables, it would be good to implement a system whereby as the user selects their chosen date and number of guests, a check is made as to free tables at that point so that the user is only shown time slots for that date that can accommodate the booking in the dropdown. If there are no time slots that can accommodate the number of guests on the chosen date, the user can be told at that point before they even click the 'Make a Booking' button. 
* For dates that are fully booked for all time slots, it would be good to have a mechanism whereby those dates could be disabled in the datepicker so that users cannot select them.
* Currently if the Site Admin tries to make a booking via the Admin panel, all of the restaurant tables are present for selection, rather than just those applicable to the time slot the Admin chooses. It would be good, once the Admin selected the applicable time slot, for only those tables allocated to that time slot to be available for selection so that the Admin wouldn't have to look this up manually.
* It would be good to have some custom 'filter by date' options for the Site Admin to filter bookings e.g. to show bookings this week, bookings tomorrow and to filter out bookings for dates that have passed.

## Wireframes

I used [Balsamiq](https://www.balsamiq.com) to create Wireframe mock-ups for laptop/large monitor, tablet and mobile devices which can be found here: 
*  

## Design

### Page Designs

### Fonts

I used [Google Fonts](https://fonts.google.com/) for the website fonts. The selected fonts and their fallbacks, should they not import into the site correctly, are as follows:

Selected Font | Fallback Font
------------- | --------------

### Colours

The colour scheme used on the site is as follows: 

Colour Name | Hexadecimal Code
------------| ---------

### Entity Relationship Diagram

## Agile Methodology
    
## Technologies Used

### Languages 
* [HTML5](https://en.wikipedia.org/wiki/HTML5) programming language for the structure and content of the website.
* [CSS3](https://en.wikipedia.org/wiki/CSS) for styling the look of the website.
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript) for adding interactivity to the website. 
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) programming language for the logic of the application.

### Frameworks, Libraries and Modules
* [Django](https://www.djangoproject.com/) was the python framework used to allow rapid, secure development and the clean, pragmatic design of this application.
* [Bootstrap](https://getbootstrap.com/) was the framework used to assist in the building of a responsive, mobile-first site.
* [Gunicorn](https://gunicorn.org/) was used as the python WSGI HTTP Server to run Django on Heroku.
* [dj_database_url](https://pypi.org/project/dj-database-url/) was used so that database URLs could be used in the Django Application to connect to the Postgres database.
* [psycopg2](https://pypi.org/project/psycopg2/) was the PostgreSQL database adapter used for the Python programming language.
* [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) was used for authentication, registration and account management for the application.
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) was used to help manage the formatting of forms in the django application.
* [Jquery](https://jquery.com/) was used to assist with HTML document traversal, manipulation and event handling.
* [Django testing tools](https://docs.djangoproject.com/en/4.0/topics/testing/tools/) were used for testing the python code.
* [coverage](https://pypi.org/project/coverage/) was used to check and report on the amount of python code covered by automated tests.
* The [inbuilt python random module](https://docs.python.org/3/library/random.html) was used to randomly choose between different suitable table options available for selection for a booking in the TableSelectionMixin class methods.
* The [inbuilt python math module](https://docs.python.org/3/library/math.html) was used to find the minimum number of tables needed for a booking (where all the tables are smaller than the party size and all the tables are the same size but there are more than 2 and not all the tables are needed) in the TableSelectionMixin class evaluate_smaller_tables method.
* The [inbuilt python itertools module](https://docs.python.org/3/library/itertools.html) was used to create a list of all possible table combinations in the TableSelectionMixin class combine_tables method and to chain querysets together in the test_table_mixin file.
* The [inbuilt python datetime module](https://docs.python.org/3/library/datetime.html) was used throughout the application for manipulating date and time objects.
* The [python pytz library](https://pypi.org/project/pytz/) and the [inbuilt unittest.mock library](https://docs.python.org/3/library/unittest.mock.html) were used in testing the 'created_on' field in the Booking model.

### Programs and Resources
* [Git](https://git-scm.com/) was the version control system used via the Gitpod terminal to commit and push code to GitHub.
* [GitHub](https://github.com/) was the git repository hosting service used to store code pushed from Git.
* [Gitpod](https://www.gitpod.io/) was the online IDE (Integrated Development Environment)/editor used to create, modify and preview the project code. 
* [Heroku](https://www.heroku.com/) was the cloud application platform used to deploy and host the application.
* [Lucidchart](https://www.lucidchart.com/pages/) was used to prepare the Flow Chart for the table selection logic in the application. 
* [dbdiagram.io](https://dbdiagram.io/home) was used to prepare the Entity Relationship Diagram.
* [The Multi Device Website Mockup Generator](https://techsini.com/multi-mockup/index.php) was used to create the screenshots showing how the website looks on different device types in conjunction with the [Ignore X-Frame headers Google Chrome Extension](https://chrome.google.com/webstore/detail/ignore-x-frame-headers/gleekbfjekiniecknbkamfmkohkpodhe).
* [Google Fonts](https://fonts.google.com/) was used to import all of the fonts used on the website. 
* [Font Awesome](https://fontawesome.com/) was used to provide all the icons throughout the site.  
* [Balsamiq](https://www.balsamiq.com) was used to prepare all of the Wireframes for the site. 
* [Chrome DevTools](https://developer.chrome.com/docs/devtools/) was used to inspect the project code throughout creation of the site. 
* [ColorSpace](https://mycolor.space/) was used to generate the colour palettes from which most of the colours for the website were taken. 
* [Eye Dropper](https://eyedropper.org/) was used to find out the names of the hex code colours used on the site.
* [Favicon Generator](https://favicon.io/favicon-generator/) was used to create the favicon for the site. 
* [Unsplash](https://unsplash.com/) provided free photos used throughout the site.
* [Cloudinary](https://cloudinary.com/) was used to store the photographs, favicon and logos used by the application.
* [Google Drive](https://www.google.com/intl/en-GB/drive/) was used to store the menus linked in the application.
* [W3 Schools](https://www.w3schools.com/), [Stack Overflow](https://stackoverflow.com/), [CSS-Tricks](https://css-tricks.com/), [MDN Web Docs](https://developer.mozilla.org/en-US/), [Python.org](https://www.python.org/) and [Django documentation](https://docs.djangoproject.com/en/4.0/) were used for general guidance and learning.  
* [What is my Viewport?](https://whatismyviewport.com/) was used to confirm the viewport screen sizes of my devices for testing the project. 
* [Can I Use?](https://caniuse.com/) was used for checking browser compatibility.
* [Compressor](https://compressor.io/) was used for compressing photos used on the site. 
* [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) was used to check the contrast of foreground text colours against their background colours.
* [The W3C Markup Validation Service](https://validator.w3.org/), [The W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/), [JSHint](https://jshint.com/) and [PEP8 Online](http://pep8online.com/), were used for testing the html, css, javascript and  python code for the site.
* [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and [Mastering Markdown](https://guides.github.com/features/mastering-markdown/) were used for preparing the README.md and TESTING.md files.
* [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/) was used to generate secret keys for the development and production environments.
* [Character Counter Online](https://www.charactercountonline.com/) was used for counting the number of characters in git commit messages.
* [cdnjs](https://cdnjs.com/) was used to provide CDN links.
* [Gijgo datepicker](https://gijgo.com/datepicker) was used to provide the datepicker for the 'Make a Booking' and 'Edit a Booking' forms.
* [Fake UK Phone Numbers](https://fakenumber.org/united-kingdom) was used to generate a fake phone number for the restaurant.
* [Canva](https://www.canva.com/en_gb/) was used for the restaurant logos and illustrations and for the design of the restaurant menus.
* [Color hex](https://www.color-hex.com/) was used to convert hex colours into rgb colours.
* [Project management on Github](https://www.topcoder.com/thrive/articles/project-management-on-github), [User Stories and Epics for the Win article](https://www.christianstrunk.com/blog/user-stories-and-epics-for-the-win), [Atlassian Agile epics: definition, examples, and templates article](https://www.atlassian.com/agile/project-management/epics) and [A Complete Guide to Agile Epics article](https://www.wrike.com/agile-guide/agile-epics-guide/) were used in drafting the epics and user stories. 

## Testing

Please see the separate [TESTING.md file](TESTING.md) for details of the project testing carried out. 

## Deployment

## Credits 

### Code

* 

### Media

#### Illustrations

All of the restaurant logo illustrations used on the website were generated with a Canva Pro subscription at [Canva](https://www.canva.com/en_gb/).

#### Photos

With thanks, the photos appearing on the website were taken by the following photographers: 

* From [Unsplash](https://unsplash.com/):
   * Home Page - [Tea lights photo](https://unsplash.com/photos/lInmrunal_M) by Mister B.
   * Register Page - [Blue flowers photo](https://unsplash.com/photos/qzoSJlPxS9k) by Tomoko Uji.
   * Login Page - [Woman pouring champage at an outdoor dining table photo](https://unsplash.com/photos/RygIdTavhkQ) by Dave Lastovskiy.
   * Make a Booking Page - [Wine and food served in ceramic bowls photo](https://unsplash.com/photos/xIFbDeGcy44) by Stefan Johnson.
   * Edit a Booking Page - [Leaves silhouette over entranceway with amber lights in the background photo](https://unsplash.com/photos/rfGVU1diIns) by Artem Kniaz.
   * Contact Us Page - [Purple flowers surrounding a lit up path photo](https://unsplash.com/photos/R_c77Rx9UzM) by Cee.
   * Logout Page - [Light up flowers photo](https://unsplash.com/photos/F2fsUga_HU8) by Arisa Chattasa.
      
### Content

* The recipe names shown on the summer and winter menus were taken from the [BBC Good Food website](https://www.bbcgoodfood.com/) and the [Delicious Magazine website](https://www.deliciousmagazine.co.uk/).

### Acknowledgments

Many thanks to:
* My mentor, Brian Macharia, for his help and guidance.
* The Code Institute tutors for their support. 
