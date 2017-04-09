class Profile: 
	site_name_list = []
	url_list = []
	xpath_list = []

	email = None
	email_sender_name = None
	email_subject = None

	def __init__(self, profile_json):
		for node in profile_json['sites']:
			self.site_name_list.append(node['name'])
			self.url_list.append(node['url'])
			self.xpath_list.append(node['xpath'])

		self.email_recipient = profile_json['email_recipient']['email']
		self.email_sender_name = profile_json['email_recipient']['sender_name']
		self.subject = profile_json['email_recipient']['subject']


		