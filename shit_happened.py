import shelve
import json
import change_check
from notification import Notification
from profile import Profile, Site

class Shit_Happened:
	storage = None
	notification = None
	profile_list = []
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
		storage_name = setting_json['storage_name']
		self.storage = shelve.open(storage_name)

		## Profile ##
		profile_name_list = setting_json['profile_name']
		profile_dir = setting_json['profile_dir']

		print('==Found', len(profile_name_list), 'profiles:', profile_name_list)

		# Read profiles and add them to profile list
		for profile_name in profile_name_list:
			profile = self._read_profile(profile_dir + profile_name);
		if profile is not None:
			self.profile_list.append(profile)

		## Site ##
		for profile in self.profile_list:
			for site in profile.site_list:
				# If the site url is not in dict, create it
				if not site[1] in self.site_dict:
					self.site_dict[site[1]] = Site(site[0], site[1]) # (name, url)
				# Append the recipient to Site
				self.site_dict[site[1]].add_recipient(profile.email)

		print('==Found', len(self.site_dict.keys()), 'sites')

		for site_url, site in self.site_dict.items():
			print("{}: {}\nrecipient:{}".format(site.name, site.url,site.recipient_email_list))

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
		# Collect every site that needs to be checked



		pass


setting_name = 'setting.json'
sh = Shit_Happened(setting_name)

sh.check_site()

exit()
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