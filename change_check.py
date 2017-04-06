from urllib.request import urlopen
import lxml.html, lxml.etree
import hashlib

def check_url_change(storage, url, xpath):
	print('--Checking: {}'.format(url))

	# Open and read from url
	try:
		response = urlopen(url)
	except:
		print('Error connecting to {}'.format(url))
		return False

	html_content = response.read()

	# Parse html and locate element using XPath
	root = lxml.html.fromstring(html_content)
	content = root.xpath(xpath)

	# Stringify the content tree
	str_content_tree = lxml.etree.tostring(content[0]);

	# Hash of content tree
	hash_content = hashlib.md5(str_content_tree).hexdigest()

	# Hash of url
	hash_url = hashlib.md5(url.encode('utf-8')).hexdigest()

	# Check if the hash changed comparing to the last test
	try: 
		old_hash_content = storage[hash_url]
		#print('Last hash: \t' + oldHashContent + '\nCurrent hash: \t' + hashContent)
		if old_hash_content != hash_content:
			#print('Content changed, update DB')
			storage[hash_url] = hash_content
			return True
	except:
		#print('URL not found in DB, update DB')
		storage[hash_url] = hash_content

	return False