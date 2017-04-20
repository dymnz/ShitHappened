from collections import namedtuple

class Profile: 
	site_list = []	# (name, url, xpath)

	name = None
	email = None
	email_sender_name = None
	email_subject = None

	def __init__(self, profile_json):
		Profile_Site_Info = namedtuple('Profile_Site_Info', 'site_name url xpath')

		for node in profile_json['sites']:
			self.site_list.append( Profile_Site_Info(node['name'], node['url'], node['xpath'])  )

		self.email = profile_json['email_recipient']['email']
		self.email_sender_name = profile_json['email_recipient']['sender_name']
		self.subject = profile_json['email_recipient']['subject']
		self.name = profile_json['name']

		print('Parsed profile: {}:{}'.format(self.name, self.email))


class Site:
	url = None
	content_changed = False
	recipient_list = []	# (site_name, recipient_email, xpath)

	def __init__(self, url):
		self.url = url

	def add_recipient(self, site_name, recipient_email, xpath):
		Recipient_Site_Info = namedtuple('Recipient_Site_Info', 'site_name recipient_email xpath')
		'''
		self.recipient_list.append(Recipient_Site_Info(
			site_name, 
			recipient_email, 
			xpath))'''

		self.recipient_list.append(xpath)

		print('{}:{} add_recipient for {} '.format(self, self.url, xpath))
		print(self.recipient_list)


	def set_changed(self):
		self.content_changed = True
