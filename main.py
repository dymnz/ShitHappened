import lxml.html
from urllib.request import urlopen

url = 'file:///Users/wangshunxing/Documents/ETH/ShitHappened/index.html'
path = '//table/tr/td'

response = urlopen(url)
htmlContent = response.read()

root = lxml.html.fromstring(htmlContent)
content = root.xpath(path)

for td in content:
	print(td.text);



