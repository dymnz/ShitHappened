import shelve
import json
import change_check
from notification import Notification
from profile import Profile, Site
from change_check import Change_checker

class Shit_Happened:
	storage_name = None
	notification = None
	change_checker = None
	profile_dict = dict()
	site_dict = dict()

	def __init__(self, setting_name):
		self._read_setting(setting_name)

	# Read setting from file
	def _read_setting(self, setting_name):
		with open(setting_name) as data_file:    
		    setting_json = json.load(data_file)

		## Notificaiton ##
		self.notification = Notification()
		self.notification.email_config(setting_json['email_sender'])

		## Storage ##
		self.storage_name = setting_json['storage_name']		

		## Profile ##
		profile_name_list = setting_json['profile_name']
		profile_dir = setting_json['profile_dir']

		print('==Found', len(profile_name_list), 'profiles:', profile_name_list)

		# Read profiles and add them to profile list
		for profile_name in profile_name_list:
			profile = self._read_profile(profile_dir + profile_name);
			if profile is not None:
				self.profile_dict[profile.email] = profile

		## Site ##
		for profile_email, profile in self.profile_dict.items():
			for profile_site_info in profile.site_list:	# (site_name, url, xpath)

				# If the site url is not in dict, create it
				if not profile_site_info.url in self.site_dict:				
					self.site_dict[profile_site_info.url] = Site(profile_site_info.url) 			

				# Append the recipient to Site (site_name, email, xpath)
				self.site_dict[profile_site_info.url].add_recipient(
					profile_site_info.site_name, 
					profile.email, 
					profile_site_info.xpath)

		print('==Found', len(self.site_dict.keys()), 'sites')

		for site_url, site in self.site_dict.items():
			print("-{}-\nrecipients:{}".format(site.url, site.recipient_list))

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
		self.storage = shelve.open(storage_name)


		# For each site, download html content and check each xpath
		for site_url, site in self.site_dict.items():
			#print(list(site.recipient_list))
			pass



		# Notification driven by changes in site.
		# Site change -> append recipient's notification list


		self.storage.close()
		pass


setting_name = 'setting.json'
sh = Shit_Happened(setting_name)

exit()

sh.check_site()


'''

# Start
changed_sites = []

# Open hash database
storage = shelve.open(storage_name)

if change_check.check_url_change(storage, url, xpath):
	changed_sites.append((site_name, url))
	print('URL changed')
else:
	print('Nothing changed')

storage.close()

if changed_sites:
	notification.send_email(email_sender_name, email_recipient, subject, changed_sites);




'''