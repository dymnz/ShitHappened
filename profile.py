class Profile: 
	site_list = []
	xpath_list = []

	name = None
	email = None
	email_sender_name = None
	email_subject = None

	def __init__(self, profile_json):
		for node in profile_json['sites']:
			self.site_list.append( (node['name'],node['url']) )
			self.xpath_list.append(node['xpath'])

		self.email = profile_json['email_recipient']['email']
		self.email_sender_name = profile_json['email_recipient']['sender_name']
		self.subject = profile_json['email_recipient']['subject']
		self.name = profile_json['name']

		print('Parsed profile: {}'.format(self.name))


class Site:
	name = None
	url = None
	content_changed = False
	recipient_email_list = []

	def __init__(self, name, url):
		self.name = name
		self.url = url

	def add_recipient(self, recipient_email):
		self.recipient_email_list.append(recipient_email)

	def set_changed(self):
		self.content_changed = True
