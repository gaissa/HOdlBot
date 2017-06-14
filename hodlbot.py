#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HOdlBot
Version: 2017-06-14
gaissa <https://github.com/gaissa>
"""

from threading import Thread
import json
import os
import random
import socket
import sys
import time
import urllib2

threads = []

class CoinMarketCap():
	"""
	A Class for fetching the data from CoinMarketCap API.
	"""

	def __init__(self, chan, data, irc):
		"""
		Init.

		:param chan: Any string, the IRC channel.
		:param data: COMMENT.
		:param irc : COMMENT.
		"""

		self.chan = chan
		self.data = data
		self.irc = irc
		self.main()

	def main(self):
		"""
		COMMENT.
		"""

		if self.data.find('PRIVMSG ' + self.chan + ' :!cap') != -1:
			
			temp = self.data.split(':!cap')
			cointemp = temp[1].strip()

			print cointemp			
			self.fetch(cointemp)

	def fetch(self, cointemp):
		"""
		COMMENT.
		
		:param cointemp: The coin input from the user.
		"""

		base = 'https://api.coinmarketcap.com/v1/ticker/'
		coin = cointemp
		convert = '/?convert=EUR'		
		url = base + coin + convert
		f = urllib2.urlopen(url)
		json_string = f.read()
		parsed_json = json.loads(json_string)
		self.irc.send('PRIVMSG ' + self.chan + ' :' + \
						parsed_json[0]['name'] + \
						' | ' + \
						'RANK: ' + parsed_json[0]['rank'] + \
						' | ' + \
						'BTC: ' + parsed_json[0]['price_btc'] + \
						' | ' + \
						'EUR: ' + parsed_json[0]['price_eur'] + \
						' | ' + '1h: ' + \
						parsed_json[0]['percent_change_1h'] + '%' + \
						' | ' + '24h: ' + \
						parsed_json[0]['percent_change_24h'] + '%' + \
						' | ' + '7d: ' + \
						parsed_json[0]['percent_change_7d'] + '%' + \
						'\r\n')

class HOdlBot():
	"""
	HOdlBot main class.
	"""

	# set IRC connection via socket
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def main(self):
		"""
		Get the user inputs, run the bot
		and fire up the other functions as well.
		"""

		title = 'HOdlBot'
		print '\n\n' + title
		print '=' * len(title), '\n'
		network = raw_input(':SET NETWORK = ')
		port = input(':SET PORT = ') # make default port (6667)!
		print
		chan = raw_input(':SET CHANNEL = ')

		# bot setup
		admins = ''
		bot_nick = 'HOdlBot'
		bot_names = 'HOdlBot HOdlBot HOdlBot :HOdlBot'

		# connect
		try:
			print '\n:CONNECTING = ' + network, port, chan + '\n'
			self.irc.connect((network, port))
		except:
			print ':NETWORK ERROR', '\n'
			sys.exit(0)

		# default output encoding
		reload(sys)
		sys.setdefaultencoding('utf-8')

		# set (send) names for the bot
		self.irc.send('NICK ' + bot_nick + '\r\n')
		self.irc.send('USER ' + bot_names + '\r\n')

		# join the channel
		self.irc.send('JOIN ' + chan + '\r\n')

		# while true, run the bot
		while True:
			data = self.irc.recv(4096)
			print data

			self.connection(data)
			self.join(chan, data)
			self.reconnect(chan, data)
			self.quitbot(chan, data)

			# fetch the data from CoinMarketCap
			CoinMarketCap(chan, data, self.irc)

	def hello(self, action, chan, msgpath):
		"""
		Say the greeting message.

		:param action : Action to send to IRC.
		:param chan   : Any string, the IRC channel.
		:param msgpath: The path to the message file.
		"""

		with open (msgpath, 'r') as w:
			wordlist = w.readlines()
		hello = random.choice(wordlist)
		time.sleep(1)
		self.irc.send(action + chan + ' :' + hello + '\r\n')

	def join(self, chan, data):
		"""
		Say hello when someone joins the channel.

		:param chan: any string, the IRC channel.
		:param data: COMMENT.
		"""

		if data.find('JOIN') != -1:
			time.sleep(1)
			self.hello('PRIVMSG ', chan, './dict/greet')

	def connection(self, data):
		"""
		Keep the connection alive.

		:param data: COMMENT.
		"""

		if data.find('PING') != -1:
			self.irc.send('PONG ' + data.split() [1] + '\r\n')

	def reconnect(self, chan, data):
		"""
		Reconnect the bot if kicked.

		:param chan: any string, the IRC channel.
		:param data: COMMENT.
		"""

		if data.find('KICK') != -1:
			self.irc.send('JOIN ' + chan + '\r\n')

	def quitbot(self, chan, data):
		"""
		Quit the bot.

		:param chan: any string, the IRC channel.
		:param data: COMMENT
		"""

		if data.find('PRIVMSG ' + chan + ' :!bot quit') != -1:
			path = './dict/quit'
			self.hello('QUIT :', chan, path)
			print '\n:DISCONNECTING\n\n'
			time.sleep(1)
			sys.exit(0)

# run HodlBot!
if __name__ == "__main__":
	HOdlBot().main()
