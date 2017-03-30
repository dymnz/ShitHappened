# https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python




def sendNotification(siteName, recipient):
	message = 
	sendEmail()



user = 'user'
password = 'password'
stmpURL = 'smtp.gmail.com'
stmpPort = 465

def setParam(_user, _password, _stmpURL, _stmp)
	global user, password, stmpURL, stmpPort
	user = _user
	password = _password
	stmpURL = _stmpURL
	stmpPort = _stmpPort

def sendEmail(recipient, message):
	# SMTP_SSL Example
	server_ssl = smtplib.SMTP_SSL(stmpURL, stmpPort)
	server_ssl.ehlo() # optional, called by login()
	server_ssl.login(user, password)  
	# ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
	server_ssl.sendmail(user, recipient, message)
	#server_ssl.quit()
	server_ssl.close()
	print('successfully sent the mail')
