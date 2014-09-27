# This Python file uses the following encoding: utf-8
import cgi, httplib, urllib, re
from datetime import datetime

fs = cgi.FieldStorage()

print 'HTTP/1.1 200 OK'
print 'Content-type: text/html'
print
print
print '<HTML><HEAD><TITLE>Results from Zomato</TITLE></HEAD>'
print '<BODY>'
print '<h1> Results from Zomato </h1>'

statistics = {}		# Will store all time-related statistics here

try:
	statistics['start_conn'] = datetime.now()
	conn = httplib.HTTPSConnection('www.zomato.com')
	conn.request("GET", "/" + str.lower(fs['inputRestaurantCity'].value) + "/restaurants?" + urllib.urlencode({"q":fs['inputRestaurantName'].value}))
	httpresponse = conn.getresponse()
	statistics['conn_resp'] = datetime.now()
	statistics['resp_time'] = statistics['conn_resp'] - statistics['start_conn']
	
	respString = httpresponse.read()

	statistics['parse_start'] = datetime.now()
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
	
	statistics['parse_end'] = datetime.now()
	statistics['parse_time'] = statistics['parse_end'] - statistics['parse_start']

except Exception,e:
	print 'An error occured: '
	print e

print "<br/>"
print "<i>Total time to get a response from Zomato.com</i> : " + str(statistics['resp_time'].total_seconds()) + " seconds. " + "<br/>"
print "<i>Total time to parse the response</i>             : " + str(statistics['parse_time'].total_seconds())+ " seconds."
print '</BODY>'
