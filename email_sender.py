import smtplib 
from util import *

class EmailSender:
	_user = 'user'
	_password = 'password'
	_stmp_url = 'smtp.gmail.com'
	_stmp_port = 465

	def __init__(self, user, password, stmpURL, stmpPort):
		self._user = user
		self._password = password
		self._stmp_url = stmpURL
		self._stmp_port = stmpPort

	# https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
	def send_email(self, recipient, message):
		# SMTP_SSL Example
		server_ssl = smtplib.SMTP_SSL(self._stmp_url, self._stmp_port)
		server_ssl.ehlo() # optional, called by login()
		server_ssl.login(self._user, self._password)  
		# ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
		server_ssl.sendmail(self._user, recipient, message.as_string())
		#server_ssl.quit()
		server_ssl.close()
		logging.info("Email sent to {}".format(recipient))

