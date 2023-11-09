import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Pedro', '87654321')

import urequests
r = urequests.get("http://www.google.com")
print(r.content)
r.close()