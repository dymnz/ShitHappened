from util import *

class Profile: 
	
	def __init__(self, profile_json):		
		self.site_list = list()		

		for node in profile_json['sites']:
			# [Profile_Site_Info, ToNotify]
			self.site_list.append( [Profile_Site_Info(node['name'], node['url'], node['xpath']), False] )

		self.site_state_list = [Site_State.No_Change] * len(self.site_list)

		self.email = profile_json['email_recipient']['email']
		self.email_sender_name = profile_json['email_recipient']['sender_name']
		self.subject = profile_json['email_recipient']['subject']
		self.name = profile_json['name']

		logging.debug('Parsed profile: {}:{}'.format(self.name, self.email))


class Site:

	def __init__(self, url):
		self.url = url
		self.recipient_list = list()

	def add_recipient(self, profile_site_info):
		self.recipient_list.append(profile_site_info)