import shelve
from notification import Notification
import change_check
import json

profile_name = 'profile1.json'
setting_name = 'setting.json'
with open(profile_name) as data_file:    
    profile = json.load(data_file)
with open(setting_name) as data_file:    
    setting = json.load(data_file)

# Setting
notification = Notification()
notification.email_config(setting['email_sender']['username'], 
	setting['email_sender']['password'],
	setting['email_sender']['stmp']['url'],
	setting['email_sender']['stmp']['port'])
storage_name = setting['storage_name']

# Profile
site_name = profile['sites'][0]['name']
url = profile['sites'][0]['url']
xpath = profile['sites'][0]['xpath']

email_recipient = profile['email_recipient']['username']
email_sender_name = profile['email_recipient']['sender_name']
subject = profile['email_recipient']['subject']

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




