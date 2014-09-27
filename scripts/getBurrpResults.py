# This Python file uses the following encoding: utf-8
import cgi, httplib, urllib, re
from datetime import datetime

fs = cgi.FieldStorage()

print 'HTTP/1.1 200 OK'
print 'Content-type: text/html'
print
print
print '<HTML><HEAD><TITLE>Results from Burrp</TITLE></HEAD>'
print '<BODY>'
print '<h1> Results from Burrp </h1>'

statistics = {}		# Will store all time-related statistics here

try:
	statistics['start_conn'] = datetime.now()
	conn = httplib.HTTPConnection('www.burrp.com')
	conn.request("GET", "/" + str.lower(fs['inputRestaurantCity'].value) + "/search.html?" + urllib.urlencode({"q":fs['inputRestaurantName'].value}))
	httpresponse = conn.getresponse()
	statistics['conn_resp'] = datetime.now()
	statistics['resp_time'] = statistics['conn_resp'] - statistics['start_conn']
	
	respString = httpresponse.read()

	statistics['parse_start'] = datetime.now()
	# To make the regex parsing easy, I'll consolidate everything into a single line 
	respString = respString.replace("\n","")
	respString = respString.replace("\r","")

	regExp = re.search(r'<section class="listing PR">.*</section>', respString)
	if regExp:

		# Parse only the list of results, and not the list of page-links
		olistResults = re.search(r'<ul class="item_listing">\s*?<li>.*?</ul>', regExp.group(0))
		if olistResults:
			for listing in re.findall(r"<li>.*?</li>", olistResults.group(0)):
				nameLine 		= ''
				addrLine 		= ''
				featuresLine 	= ''
				costLine 		= ''
				voteLine 		= ''
				cuisineLine  	= ''
				
				# Extract the Name
				nameMatch = re.search(r'<p class="UC"><a.*?>(.*?)</a></p>', listing)
				if nameMatch:
					nameLine = '<h3>'+nameMatch.group(1)+'</h3>'
				
				# Extract the Address
				addrMatch = re.search(r'<p class="MT5">(.*?)</p>',listing)
				if addrMatch:
					for anchor in re.finditer(r'<a.*?><strong>(.*?)</strong></a>', addrMatch.group(1)):
						addrLine = addrLine + '<i>'+anchor.group(1) + " " + '</i>' + '<br/>'
						
				# Extract the value-added features and services
				featureMatch = re.search(r'<p class="MT7 gd10ll UC">(.*?)</p>', listing)
				if featureMatch:
					featuresLine = "<strong>"+featureMatch.group(1)+"</strong>" + "<br/>"
				
				# Extract Cuisine
				cuisineMatch = re.search(r'<p class="gd13lr MT5">(.*?)</p>', listing)
				if cuisineMatch:
					for anchor in re.finditer(r'<a.*?>(.*?)</a>', cuisineMatch.group(1)):
						cuisineLine = cuisineLine + " " + anchor.group(1)
				if len(cuisineLine) > 0 :
					cuisineLine = "<i>"+ cuisineLine+ "</i>"+"<br/>"
				# Extract the Cost
				costMatch = re.search(r'<p class="FR lg_col hotel_rate">(.*?)</p>', listing)
				if costMatch:
					label = re.search(r'(.*?)<br>', costMatch.group(1))
					costLine = label.group(1) + ": "
					costSpan = re.search(r'<span style=".*?">(.*?)</span>', costMatch.group(1))
					if costSpan:
						costLine = costLine + "Rs. " + costSpan.group(1)
					else:
						costLine = costLine + 'NA'
					costLine = '<h4>'+costLine+'</h4>'
				
				# Extract ratings and votes
				voteMatch = re.search(r'<div class="lg_col MT5">(.*?)</div>',listing)
				if voteMatch:
					for paragraph in re.finditer(r'<p.*?>(.*?)</p>', voteMatch.group(1)):
						voteLine = voteLine + paragraph.group(1)+'<br/>'
				
				print nameLine
				print addrLine
				print costLine
				print voteLine
				print cuisineLine
				print featuresLine
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
print "<i>Total time to get a response from Burrp.com</i> : " + str(statistics['resp_time'].total_seconds()) + " seconds. <br/>"
print "<i>Total time to parse the response</i>            : " + str(statistics['parse_time'].total_seconds()) + " seconds."
print '</BODY>'
