from urllib.request import urlopen
import lxml.html, lxml.etree
import hashlib
from util import *

class Change_checker: 
	url = None
	response = None
	html_content = None

	def check_xpath(self, storage, xpath_list):
		changed_list = [False] * len(xpath_list)

		for index, xpath in enumerate(xpath_list):
			changed_list[index] = self._check_url_change(storage, xpath)

		# Update the storage for all updated sites
		for index, site_state in enumerate(changed_list):
			if site_state == Site_State.Changed or site_state == Site_State.No_Record:
				logging.debug('update {}:{}:{}'.format(self.url, xpath_list[index], site_state))
				self._update_storage(storage, xpath_list[index])

		return changed_list

	def open_site(self, url):
		self.url = url
		try:
			self.response = urlopen(self.url)
			self.html_content = self.response.read()
			return True
		except Exception as e:
			logging.error('[Error] cannot connect to {}'.format(self.url))
		return False

	def _check_url_change(self, storage, xpath):
		logging.debug('Checking: {}:{}'.format(self.url, xpath))
		# Parse html and locate element using XPath
		root = lxml.html.fromstring(self.html_content)
		content = root.xpath(xpath)

		if len(content) == 0:
			logging.error('[Error] xpath not found: {}:{}'.format(self.url, xpath))
			return False

		# Stringify the content tree
		str_content_tree = lxml.etree.tostring(content[0]);

		# Hash of content tree
		hash_content = hashlib.md5(str_content_tree).hexdigest()

		# Hash of database entry = md5(cat( url, xpath ))
		hash_key = hashlib.md5(self.url.encode('utf-8') + xpath.encode('utf-8')).hexdigest()

		# Check if the hash changed comparing to the last test
		try: 
			old_hash_content = storage[hash_key]

			logging.debug('Last hash: \t\t' + old_hash_content)
			logging.debug('Current hash: \t' + hash_content)
			if old_hash_content != hash_content:
				logging.debug('Content changed, update DB')
				return Site_State.Changed
		except Exception as e:			
			logging.info('URL not found in DB, update DB')
			storage[hash_key] = hash_content
			return Site_State.No_Record

		return Site_State.No_Change

	def _update_storage(self, storage, xpath):
		# Parse html and locate element using XPath
		root = lxml.html.fromstring(self.html_content)
		content = root.xpath(xpath)

		# Stringify the content tree
		str_content_tree = lxml.etree.tostring(content[0]);

		# Hash of content tree
		hash_content = hashlib.md5(str_content_tree).hexdigest()

		# Hash of database entry = md5(cat( url, xpath ))
		hash_key = hashlib.md5(self.url.encode('utf-8')+xpath.encode('utf-8')).hexdigest() 

		# Check if the hash changed comparing to the last test
		storage[hash_key] = hash_content


