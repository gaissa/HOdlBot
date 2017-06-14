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

threads = []

class HOdlBot():
	"""
	HOdlBot main class.
	"""

	# set irc connection via socket
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def main(self):
		"""
		Get the user inputs, run the bot
		and fire up the other functions as well.
		"""

		# set and print bot title
		title = 'HOdlBot'
		print '\n\n' + title
		print '=' * len(title), '\n'

		# make default port (6667)
		network = raw_input(':SET NETWORK = ')
		port = input(':SET PORT = ')
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

		# join the channel and say hello
		self.irc.send('JOIN ' + chan + '\r\n')
		self.hello('PRIVMSG ', chan, './dict/greet')

		# while true, run the bot
		while True:
			data = self.irc.recv(4096)
			print data

			self.connection(data)

			self.join(chan, data)
			self.reconnect(chan, data)
			self.quitbot(chan, data)

	def hello(self, action, chan, msgpath):
		"""
		Say the greeting message.

		:param action : Action to send to IRC.
		:param chan   : Any string, the IRC channel
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

		:param chan: any string, the IRC channel
		:param data: COMMENT
		"""
		if data.find('JOIN') != -1:
			time.sleep(1)
			self.hello('PRIVMSG ', chan, './dict/greet')

	def connection(self, data):
		"""
		Keep the connection alive.

		:param data: COMMENT
		"""
		if data.find('PING') != -1:
			self.irc.send('PONG ' + data.split() [1] + '\r\n')

	def reconnect(self, chan, data):
		"""
		Reconnect the bot if kicked.

		:param chan: any string, the IRC channel
		:param data: COMMENT
		"""
		if data.find('KICK') != -1:
			self.irc.send('JOIN ' + chan + '\r\n')

	def quitbot(self, chan, data):
		"""
		Quit the bot.

		:param chan: any string, the IRC channel
		:param data: COMMENT
		"""
		if data.find('PRIVMSG ' + chan + ' :!bot quit') != -1:

			# say quit message
			path = './dict/quit'
			self.hello('QUIT :', chan, path)
			print '\n:DISCONNECTING\n\n'
			time.sleep(1)
			sys.exit(0)

# run HodlBot!
if __name__ == "__main__":
	HOdlBot().main()
