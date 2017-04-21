from collections import namedtuple
import logging

logger = logging.getLogger('logger')

class Profile: 
	
	def __init__(self, profile_json):
		Profile_Site_Info = namedtuple('Profile_Site_Info', 'site_name url xpath')

		self.site_list = list()	# (name, url, xpath)

		for node in profile_json['sites']:
			self.site_list.append( Profile_Site_Info(node['name'], node['url'], node['xpath'])  )

		self.email = profile_json['email_recipient']['email']
		self.email_sender_name = profile_json['email_recipient']['sender_name']
		self.subject = profile_json['email_recipient']['subject']
		self.name = profile_json['name']

		logger.debug('Parsed profile: {}:{}'.format(self.name, self.email))


class Site:

	def __init__(self, url):
		self.url = url
		self.recipient_list = list()
		self.changed_list = list()

	def add_recipient(self, site_name, recipient_email, xpath):
		Recipient_Site_Info = namedtuple('Recipient_Site_Info', 'site_name recipient_email xpath')

		self.recipient_list.append(Recipient_Site_Info(
			site_name, 
			recipient_email, 
			xpath))
		self.changed_list.append(False)

	def set_changed(self):
		self.content_changed = True
