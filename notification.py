from email_sender import EmailSender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Notification: 
	_email_sender = None

	def _email_config(self, sender, password, stmp_url, stmp_port):
		self._email_sender = EmailSender(sender, password, stmp_url, stmp_port)

	def email_config(self, email_sender_json):
		self._email_sender = EmailSender(email_sender_json['email'],
										email_sender_json['password'],
										email_sender_json['stmp']['url'],
										email_sender_json['stmp']['port'])

	def send_email(self, sender_name, recipient, subject, changed_sites):
		message = self._construct_message(changed_sites)

		message['From'] = sender_name
		message['To'] = recipient
		message['Subject'] = subject

		self._email_sender.send_email(recipient, message)


	# https://stackoverflow.com/questions/882712/sending-html-email-using-python
	def _construct_message(self, changed_sites):
		msg = MIMEMultipart('alternative')

		stringSites = []
		for info in changed_sites:
			stringSites.append( '{}: {}'.format(info[0], info[1]))

		text = '\n'.join(stringSites)

		stringSites = []
		for info in changed_sites:
			stringSites.append( """\
				<tr>
					<td style="width:20%; font-size: 16px; text-align: center; padding-top:20px">{}</td>
					<td style="white-space: nowrap; overflow: hidden; text-overflow:ellipsis; width:80%; padding-top:20px">{}</td>
				</tr>""".format(info[0], info[1]))

		bodyString = '\n'.join(stringSites)

		html = ("<html><head></head><body><table>"	
			+ bodyString
			+"</table></body></html>")

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		msg.attach(part1)
		msg.attach(part2)

		return msg


