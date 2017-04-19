from urllib.request import urlopen
import lxml.html, lxml.etree
import hashlib

class Change_checker: 
	url = None
	response = None
	html_content = None

	def check_xpath(self, storage, xpath_list):
		changed_list = [False] * len(xpath_list)

		for index, xpath in enumerate(xpath_list):
			changed_list[index] = self._check_url_change(storage, xpath)

		return changed_list

	def open_site(self, url):
		self.url = url
		# Open and read from url
		try:
			self.response = urlopen(self.url)
			self.html_content = response.read()
			return True
		except Exception as e:
			print('Error connecting to {}'.format(self.url))
		return False

	def _check_url_change(self, storage, xpath):
		print('--Checking: {}'.format(self.url))

		# Parse html and locate element using XPath
		root = lxml.html.fromstring(self.html_content)
		content = root.xpath(xpath)

		# Stringify the content tree
		str_content_tree = lxml.etree.tostring(content[0]);

		# Hash of content tree
		hash_content = hashlib.md5(str_content_tree).hexdigest()

		# Hash of database entry = cat( md5(url), md5(xpath) )
		hash_key = (hashlib.md5(url.encode('utf-8')).hexdigest() 
				+ hashlib.md5(xpath.encode('utf-8')).hexdigest())

		# Check if the hash changed comparing to the last test
		try: 
			old_hash_content = storage[hash_url]
			#print('Last hash: \t' + oldHashContent + '\nCurrent hash: \t' + hashContent)
			if old_hash_content != hash_content:
				#print('Content changed, update DB')
				storage[hash_key] = hash_content
				return True
		except:
			#print('URL not found in DB, update DB')
			storage[hash_key] = hash_content

		return False