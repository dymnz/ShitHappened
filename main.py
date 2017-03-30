import lxml.html, lxml.etree
import shelve
import hashlib
from urllib.request import urlopen

storageFileName = 'storage'
url = 'file:///Users/wangshunxing/Documents/ETH/ShitHappened/index.html'
path = '//table'


# Checking 
print('Checking: {}'.format(url));



# Open hash database
storage = shelve.open(storageFileName) 

# Open and read from url
response = urlopen(url)
htmlContent = response.read()

# Parse html and locate element using XPath
root = lxml.html.fromstring(htmlContent)
content = root.xpath(path)

# Stringify the content tree
strContentTree = lxml.etree.tostring(content[0]);

# Hash of content tree
hashContent = hashlib.md5(strContentTree).hexdigest()

# Hash of url
hashURL = hashlib.md5(url.encode('utf-8')).hexdigest()

# Check if the hash changed comparing to the last test
try: 
	oldHashContent = storage[hashURL]
	print('Last hash:' + oldHashContent)
	if oldHashContent != hashContent:
		print('Content changed, update DB')
		storage[hashURL] = hashContent
	else:
		print('No change in content')
	# Send notification
except:
	print('URL not found in DB, update DB')
	storage[hashURL] = hashContent

storage.close()



