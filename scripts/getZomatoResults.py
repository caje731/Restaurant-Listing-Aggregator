# This Python file uses the following encoding: utf-8
import cgi, httplib, urllib, re

fs = cgi.FieldStorage()

print 'HTTP/1.1 200 OK'
print 'Content-type: text/html'
print
print
print '<HTML><HEAD><TITLE>Results from Zomato</TITLE></HEAD>'
print '<BODY>'

try:
	conn = httplib.HTTPSConnection('www.zomato.com')
	conn.request("GET", "/" + str.lower(fs['inputRestaurantCity'].value) + "/restaurants?" + urllib.urlencode({"q":fs['inputRestaurantName'].value}))
	httpresponse = conn.getresponse()

	respString = httpresponse.read()

	# To make the regex parsing easy, I'll consolidate everything into a single line 
	respString = respString.replace("\n","")
	respString = respString.replace("\r","")

	regExp = re.search(r'<section id="search-results-container">.*</section>', respString)
	if regExp:

		# Parse only the ordered list of results, and not the unordered list of page-links
		olistResults = re.search(r'<ol>.*</ol>', regExp.group(0))
		if olistResults:
			for listing in re.findall(r"<li .*?>.*?</li>", olistResults.group(0)):
				nameLine = ''
				addrLine = ''
				costLine = ''
				voteLine = ''
				rvwLine  = ''
				
				# Extract the Name
				nameMatch = re.search(r"<h3.*?>\s*?<a.*?>(.*?)</a>\s*?</h3>", listing)
				if nameMatch:
					nameLine = '<h3>'+nameMatch.group(1)+'</h3>'
							
				# Extract the Address
				addrMatch = re.search(r'<span class="search-result-address".*?>(.*?)</span>',listing)
				if addrMatch:
					addrLine = '<i>'+addrMatch.group(1)+'</i>'
				
				# Extract the Cost
				costMatch = re.search(r'<div class="ln24">\s*?<span class="upc grey-text sml">(.*?)</span>(.*?)</div>', listing)
				if costMatch:
					costLine = '<h4>'+costMatch.group(1)+costMatch.group(2)+'</h4>'
				
				# Extract ratings, votes and offers
				voteMatch = re.search(r'<div class="right">(.*?)</div>\s*</div>\s*<div class="clear"></div>',listing)
				if voteMatch:
					voteLine = voteMatch.group(0)
				
				# Extract review
				rvwMatch = re.search(r'<div class="search_grid_9 search-matches" data-icon="Z">\s*<p.*?>\s*(.*?)</p>\s*</div>', listing)
				if rvwMatch:
					rvwLine = rvwMatch.group(1)+"<br/>"
					
				print nameLine
				print addrLine
				print costLine
				print voteLine
				print rvwLine
				print '<hr/>'
			
		else:
			print "No Results found"
	else:
		print "No Results found"
	

except Exception,e:
	print e

print '</BODY>'