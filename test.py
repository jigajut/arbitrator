import btcelib
import coinone
import exmo

import time
#import Tkinter as tk
#import tkMessageBox
import datetime
import ssl
import json
import urllib
import requests
from requests.auth import HTTPDigestAuth
import httplib
import urllib2
import socket
import inspect

response = urllib.urlopen("http://api.fixer.io/latest")
result = json.loads(response.read())

response2 = urllib.urlopen("http://api.fixer.io/latest?base=USD")
result2 = json.loads(response2.read())

gay = coinone.PublicAPIv3()
exmo = exmo.PublicAPIv3()


#currency = gay.call('currency')
rate = result2["rates"]['KRW']
#print rate
rate = float(rate) * 1.0175
#rate = 1158.42

euro = result['rates']['KRW']
euro = float(euro) * 1.02






while 1:
	now = datetime.datetime.now()
	try:
#		data = papi.call('depth', 'btc_usd', limit=1)
##		ethdata = papi.call('depth', 'eth_usd', limit=1)
#		eurodata = papi.call('depth', 'btc_eur', limit=1)
#		euroethdata = papi.call('depth', 'eth_eur', limit=1)
		exmoethus = exmo.call('ETH_USD','ETH_USD')
		exmoeuro = exmo.call('ETH_EUR', 'ETH_EUR')
		exmobtcus = exmo.call('BTC_USD', 'BTC_USD')
		exmobchus = exmo.call('BCH_USD', 'BCH_USD')
		exmoltcus = exmo.call('LTC_USD', 'LTC_USD')
		cexdollar = requests.get("https://cex.io/api/order_book/BTC/USD/?depth=20")
		cexresult = cexdollar.json()
		cexeuro = requests.get("https://cex.io/api/order_book/BTC/EUR/?depth=20")
		cexeuroresult = cexeuro.json()
		cexethdollar = requests.get("https://cex.io/api/order_book/ETH/USD/?depth=20")
		cexethresult = cexethdollar.json()
		cexetheuro = requests.get("https://cex.io/api/order_book/ETH/EUR/?depth=20")
		cexetheuroresult = cexetheuro.json()


	except ssl.SSLError:
		continue
#	btceprice = data['btc_usd']['asks'][0][0]
#	btceethprice = ethdata['eth_usd']['asks'][0][0]
#	btceeuroprice = eurodata['btc_eur']['asks'][0][0]
#	btceeuroethprice = euroethdata['eth_eur']['asks'][0][0]
	

	satisfyVolume = 0
	i = 0
	while satisfyVolume < 3000:
		satisfyVolume += float(cexresult['asks'][i][1]) * float(cexresult['asks'][i][0])
		i = i + 1
	cexdollarprice = cexresult['asks'][i][0]
	
	satisfyVolume = 0
	i = 0
	while satisfyVolume < 3000:
		satisfyVolume += float(cexeuroresult['asks'][i][1]) * float(cexeuroresult['asks'][i][0])
		i = i + 1
	cexeuroprice = cexeuroresult['asks'][i][0]
	
	satisfyVolume = 0
	i = 0
	while satisfyVolume < 3000:
		satisfyVolume += float(cexethresult['asks'][i][1]) * float(cexethresult['asks'][i][0])
		i = i + 1
	cexethprice = cexethresult['asks'][i][0]

	satisfyVolume = 0
	i = 0
	while satisfyVolume < 3000:
		satisfyVolume += float(cexetheuroresult['asks'][i][1]) * float(cexetheuroresult['asks'][i][0])
		i = i + 1
	cexetheuroprice = cexetheuroresult['asks'][i][0]



	satisfyVolume = 0
	i = 0

	while satisfyVolume < 2000:
		satisfyVolume += float(exmoethus['ETH_USD']['ask'][i][2])
		i = i + 1

	exmoethprice = exmoethus['ETH_USD']['ask'][i-1][0]	

	satisfyVolume = 0
	i = 0
	while satisfyVolume < 2000:
		satisfyVolume += float(exmobtcus['BTC_USD']['ask'][i][2])
		i = i + 1

	exmobtcprice = exmobtcus['BTC_USD']['ask'][i-1][0]
	
	satisfyVolume = 0
	i = 0
	while satisfyVolume < 2000:
		satisfyVolume += float(exmobchus['BCH_USD']['ask'][i][2])
		i = i + 1
	exmobchprice = exmobchus['BCH_USD']['ask'][i-1][0]

	
	satisfyVolume = 0
	i = 0
	while satisfyVolume < 2000:
		satisfyVolume += float(exmoeuro['ETH_EUR']['ask'][i][2])
		i = i + 1
	exmoeuroprice = exmoeuro['ETH_EUR']['ask'][i-1][0]

	satisfyVolume = 0
	i = 0
	while satisfyVolume < 2000:
		satisfyVolume += float(exmoltcus['LTC_USD']['ask'][i][2])
		i = i + 1
	exmoltcprice = exmoltcus['LTC_USD']['ask'][i-1][0]

	try:
		data2 = gay.call('orderbook', 'bid')
		ethdata2 = gay.call('orderbook','bid',currency='eth')
		bchdata2 = gay.call('orderbook','bid',currency='bch')
		ltcdata2 = gay.call('orderbook','bid',currency='ltc')
	except ssl.SSLError:
		continue
	coinoneprice = float(data2["bid"][0]['price'])/float(rate)
	coinoneethprice = float(ethdata2["bid"][0]['price'])/float(rate)
	coinonebchprice = float(bchdata2["bid"][0]['price'])/float(rate)
	coinoneltcprice = float(ltcdata2["bid"][0]['price'])/float(rate)

	coinoneeuroprice = float(data2["bid"][0]['price'])/float(euro)
	coinoneeuroethprice = float(ethdata2["bid"][0]['price'])/float(euro)	
	
#	stats = (coinoneprice/float(btceprice)-1)*100
#	ethstats = (coinoneethprice/float(btceethprice)-1)*100
#	eurostats = (coinoneeuroprice/float(btceeuroprice)-1)*100
#	euroethstats = (coinoneeuroethprice/float(btceeuroethprice)-1)*100
	exmoethstats = (coinoneethprice/float(exmoethprice)-1)*100
	exmoeurostats = (coinoneeuroethprice/float(exmoeuroprice)-1)*100
	exmobtcstats = (coinoneprice/float(exmobtcprice)-1)*100
	exmobchstats = (coinonebchprice/float(exmobchprice)-1)*100
	exmoltcstats = (coinoneltcprice/float(exmoltcprice)-1)*100
	cexusdstats = (coinoneprice/float(cexdollarprice)-1)*100
	cexeurostats = (coinoneeuroprice/float(cexeuroprice)-1)*100
	cexethusdstats = (coinoneethprice/float(cexethprice)-1)*100
	cexetheurostats = (coinoneeuroethprice/float(cexetheuroprice)-1)*100

#	print "     BTC:", now.replace(microsecond=0), '%.2f'%(stats) + "%",'W' + data2["bid"][0]['price'], '$' + '%.2f'%(coinoneprice), '$' + '%.2f'%(btceprice), 'cur=' + '%.2f'%(rate)
#	print "EURO-BTC:", now.replace(microsecond=0), '%.2f'%(eurostats) + "%",'W' + data2["bid"][0]['price'], 'E' + '%.2f'%(coinoneeuroprice), 'E' + '%.2f'%(btceeuroprice), 'cur=' + '%.2f'%(euro)
#	print "     ETH:", now.replace(microsecond=0), '%.2f'%(ethstats) + "%",'W' + ethdata2["bid"][0]['price'], '$' + '%.2f'%(coinoneethprice), '$' + '%.2f'%(btceethprice), 'cur=' + '%.2f'%(rate)
#	print "EURO-ETH:", now.replace(microsecond=0), '%.2f'%(euroethstats) + "%",'W' + ethdata2["bid"][0]['price'], 'E' + '%.2f'%(coinoneeuroethprice), 'E' + '%.2f'%(btceeuroethprice), 'cur=' + '%.2f'%(euro)

	print "CEXX-BTC-USD:", now.replace(microsecond=0), '%.2f'%(cexusdstats) + "%",'W' + data2["bid"][0]['price'], '$' + '%.2f'%(coinoneprice), '$' + '%.2f'%(float(cexdollarprice)), 'cur=' + '%.2f'%(rate)
	print "CEXX-BTC-EUR:", now.replace(microsecond=0), '%.2f'%(cexeurostats) + "%",'W' + data2["bid"][0]['price'], 'E' + '%.2f'%(coinoneeuroprice), 'E' + '%.2f'%(float(cexeuroprice)), 'cur=' + '%.2f'%(euro)
	print "CEXX-ETH-USD:", now.replace(microsecond=0), '%.2f'%(cexethusdstats) + "%",'W' + ethdata2["bid"][0]['price'], '$' + '%.2f'%(coinoneethprice), '$' + '%.2f'%(float(cexethprice)), 'cur=' + '%.2f'%(rate)
	print "CEXX-ETH-EUR:", now.replace(microsecond=0), '%.2f'%(cexetheurostats) + "%",'W' + ethdata2["bid"][0]['price'], 'E' + '%.2f'%(coinoneeuroethprice), 'E' + '%.2f'%(float(cexetheuroprice)), 'cur=' + '%.2f'%(euro)
	print "EXMO-ETH-USD:", now.replace(microsecond=0), '%.2f'%(exmoethstats) + "%",'W' + data2["bid"][0]['price'], '$' + '%.2f'%(coinoneethprice), '$' + '%.2f'%(float(exmoethprice)), 'cur=' + '%.2f'%(rate)
	print "EXMO-ETH-EUR:", now.replace(microsecond=0), '%.2f'%(exmoeurostats) + "%",'W' + ethdata2["bid"][0]['price'], 'E' + '%.2f'%(coinoneeuroethprice), 'E' + '%.2f'%(float(exmoeuroprice)), 'cur=' + '%.2f'%(euro)
	print "EXMO-BTC-USD:", now.replace(microsecond=0), '%.2f'%(exmobtcstats) + "%",'W' + data2["bid"][0]['price'], '$' + '%.2f'%(coinoneprice), '$' + '%.2f'%(float(exmobtcprice)), 'cur=' + '%.2f'%(rate)

	print "EXMO-BCH-USD:", now.replace(microsecond=0), '%.2f'%(exmobchstats) + "%",'W' + bchdata2["bid"][0]['price'], '$' + '%.2f'%(coinonebchprice), '$' + '%.2f'%(float(exmobchprice)), 'cur=' + '%.2f'%(rate)
	print "EXMO-LTC-USD:", now.replace(microsecond=0), '%.2f'%(exmoltcstats) + "%",'W' + ltcdata2["bid"][0]['price'], '$' + '%.2f'%(coinoneltcprice), '$' + '%.2f'%(float(exmoltcprice)), 'cur=' + '%.2f'%(rate)
	print ""
#	if stats > 11 or ethstats > 11:
#		tkMessageBox.showwarning('lol',str( (coinoneprice/float(btceprice)-1)*100), str((coinoneethprice/float(btceethprice)-1)*100))
	time.sleep(10)



