#!/usr/bin/python
# Based on:
#	http://www.acmesystems.it/python_httpd
#	https://pymotw.com/2/BaseHTTPServer/

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import wiringpi2 as wpi

PORT_NUMBER = 5050
red         = 4 # GPIO pin 4 = physical pin 23
green       = 5 # GPIO pin 5 = physical pin 24
blue        = 6 # GPIO pin 6 = physical pin 25
page = """
<!doctype html>
<html>
<head>
<title>Raspberry Pi PWM Server</title>
</head>
<body style="margin-left:2em">
<h1>PwmServer for Raspberry Pi</h1>
<form>
<table border="0" cellpadding="2">
<tr><td>Red</td><td><input type="text" name="r" size="8"></td></tr>
<tr><td>Green</td><td><input type="text" name="g" size="8"></td></tr>
<tr><td>Blue</td><td><input type="text" name="b" size="8"></td></tr>
<tr><td></td><td><input type="submit" value="Submit"></td></tr>
</table>
</form>
</body>
</html>"""

class reqHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		q = urlparse.parse_qsl(parsed_path.query)

		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		
		# Send the html message
		result = self.process_query(q)
		self.wfile.write(page)
		return
	
	# Dummy handler for processed query (list of name/value pairs)
	def process_query(self, query):
		for (name, value) in query:
			if name in ['r', 'g', 'b']:
				self.process_change(name, value)
		return str(query)

	# color will be r, g or b.  Value should be between 0 and 100
	def process_change(self, color, value):
		value = int(value)
		pin = 0
		if color == 'r':
			pin = red
		elif color == 'g':
			pin = green
		elif color == 'b':
			pin = blue
		if pin != 0 and value >= 0 and value <= 100:
			wpi.softPwmWrite(pin, value)


#Create a web server and define the handler to manage the
#incoming request
try:
	wpi.wiringPiSetup()
	wpi.softPwmCreate(red, 0, 100)
	wpi.softPwmCreate(green, 0, 100)
	wpi.softPwmCreate(blue, 0, 100)
	server = HTTPServer(('', PORT_NUMBER), reqHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	wpi.softPwmWrite(red, 0)
	wpi.softPwmWrite(green, 0)
	wpi.softPwmWrite(blue, 0)
	server.socket.close()
