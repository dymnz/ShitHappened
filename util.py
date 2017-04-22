import logging
from collections import namedtuple

Profile_Site_Info = namedtuple('Profile_Site_Info', 'site_name url xpath')
Recipient_Site_Info = namedtuple('Recipient_Site_Info', 'site_name recipient_email xpath')

class Site_State:
    No_Change = 0
    Changed = 1
    No_Record = 2

def setup_logger():
	# set up logging to file
	logging.basicConfig(
	     filename='log.txt',
	     level=logging.INFO, 
	     format= '%(asctime)s - %(message)s',
	     datefmt='%H:%M:%S'
	 )

	# set up logging to console
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(asctime)s - %(message)s', "%H:%M:%S")
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger('').addHandler(console)


