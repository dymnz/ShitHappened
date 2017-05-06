## ShitHappened

### What this does
Periodically checks a website for any content change (or content change under a xpath), and notifiy the user.

### How it works
1. Gather every sites and xpath from each profile
2. Loop through the sites and check each xpath against the old content (content recording is done with md5 hash, and only hash is stored)
3. Notifiy the user if their site/xpath pair has a content change

### Files
* main.py: The controller, sets the schedule of the main program
* shit_happened.py: The main program, controls the program workflow
* notification.py: Notification module
* change_check.py: Module to check website content change and hash storage update
* util.py: Logging module and common datatype definition
* profile.py: Class definition for a 'Profile' and 'Site'

### Note
* The program is tested using python3


### TODO
* The scheduling right now is stupid, change it to date.time based
* Different profiles should be able to define their own schedule
* Mailing is reaaaaaaaaally slow for some reason


