import shelve
import json
import change_check
import logging

from notification import Notification
from profile import Profile, Site
from change_check import Change_checker
from util import *

setup_logger()

class Shit_Happened:

	def __init__(self, setting_name):	
		logging.info('Shit_Happened initializing...')	
		self.storage_name = None
		self.notification = Notification()
		self.change_checker = Change_checker()
		self.profile_dict = dict()
		self.site_dict = dict()

		logging.info('Reading settings...')
		self._read_setting(setting_name)

	# Read setting from file
	def _read_setting(self, setting_name):
		with open(setting_name) as data_file:    
		    setting_json = json.load(data_file)

		## Logger ##		
		logging.getLogger('').setLevel(logging.DEBUG)  # TODO: Read debug level from setting		

		## Notification ##
		self.notification = Notification()
		self.notification.email_config(setting_json['email_sender'])

		## Storage ##
		self.storage_name = setting_json['storage_name']		

		## Profile ##
		profile_name_list = setting_json['profile_name']
		profile_dir = setting_json['profile_dir']

		logging.info('==Found {} profiles=='.format(len(profile_name_list)))
		logging.info(profile_name_list)


		# Read profiles and add them to profile list
		for profile_name in profile_name_list:
			profile = self._read_profile(profile_dir + profile_name);
			if profile is not None:
				self.profile_dict[profile.email] = profile

		## Site ##
		for profile_email, profile in self.profile_dict.items():
			for profile_site_info in profile.site_list:	# (site_name, url, xpath)

				# If the site url is not in dict, create it
				if not profile_site_info[0].url in self.site_dict:				
					self.site_dict[profile_site_info[0].url] = Site(profile_site_info[0].url) 			

				# Append the recipient to site's recepient list
				self.site_dict[profile_site_info[0].url].add_recipient(profile_site_info)

		logging.info('==Found {} sites=='.format(len(self.site_dict.keys())))

		for site_url, site in self.site_dict.items():
			logging.info(site_url)
			logging.debug("recipients:{}".format(site.recipient_list))

	# Read profile from file and return a Profile object
	def _read_profile(self, profile_name):
		try:
			with open(profile_name) as data_file:
				try:    
					profile_json = json.load(data_file)
					return Profile(profile_json)
				except Exception as e:
					print(e)
		except Exception as e:
			print(e)
			return None

	def check_site(self):
		logging.info('Checking sites...')

		storage = shelve.open(self.storage_name)

		# For each site, download html content and check each xpath
		for site_url, site in self.site_dict.items():
			logging.info('Check: {}'.format(site_url))
			logging.debug(site.recipient_list)
			
			# If the site can't be connected, move on to the next
			if self.change_checker.open_site(site_url) == False:
				continue

			# Construct a list of xpath
			xpath_list = [None] * len(site.recipient_list)
			for index, recipient_info in enumerate(site.recipient_list):
				xpath_list[index] = recipient_info[0].xpath

			logging.debug('xpath: {}'.format(xpath_list))

			# Find the xpath that is changed
			changed_list = self.change_checker.check_xpath(storage, xpath_list)
			logging.debug('changed: {}'.format(changed_list))

			# If site's content changed, set the recipient info to notify			
			for index, site_state in enumerate(changed_list):
				if site_state == Site_State.Changed:
					site.recipient_list[index][1] = True

		storage.close()
		pass

	def notify_recipients(self):
		logging.info('Notifying recipients...')

		# Loop through every recipient
		for profile_email, profile in self.profile_dict.items():
			logging.debug(profile.site_list)

			# Gather sites to be notified
			notification_site_list = []			
			for recipient_info in profile.site_list:
				if recipient_info[1] == True:					
					logging.debug(recipient_info[0].url)
					notification_site_list.append( [recipient_info[0].site_name, recipient_info[0].url])

			# Skip if there's nothing to notify
			if len(notification_site_list) == 0:
				continue;

			# Send email
			self.notification.send_email(profile.name, 
				profile.email, 
				profile.subject,
				notification_site_list )

setting_name = 'setting.json'

sh = Shit_Happened(setting_name)

sh.check_site()

sh.notify_recipients()

exit()
