#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	HOdlBot
	Version: 2017-06-14
	2017 - gaissa <https://github.com/gaissa>
"""

from threading import Thread
import json
import os
import random
import socket
import sys
import time

chan = ''
data = ''
irc = ''
threads = []

def main():
	"""
	Run the bot and handle the other functions as well.
	"""

	# set and print bot title
	title = 'HOdlBot'
	print '\n\n' + title
	print '=' * len(title), '\n'

	# set connection
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
		irc.connect((network, port))
	except:
		print ':NETWORK ERROR', '\n'
		sys.exit(0)

	# default output encoding
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# set (send) names for the bot
	irc.send('NICK ' + bot_nick + '\r\n')
	irc.send('USER ' + bot_names + '\r\n')

	# join the channel
	irc.send('JOIN ' + chan + '\r\n')

	# say hello message
	with open ('./dict/greet', 'r') as w:
		wordlist = w.readlines()
	hello = random.choice(wordlist)
	time.sleep(1)
	irc.send('PRIVMSG ' + chan + ' :' + hello + '\r\n')

	# while true, run the bot
	while True:
		data = irc.recv(4096)
		print data
		connection()
		join()
		reconnect()
		quitbot()

def send_msg(msg):
	"""
	Helper for sending to IRC.
	:param msg: any string
	"""
	irc.send('PRIVMSG ' + chan + ' :' + str(msg) + '\r\n')

def connection():
	"""
	Keep the connection alive.
	"""
	if data.find('PING') != -1:
		irc.send('PONG ' + data.split() [1] + '\r\n')

def join():
	"""
	Say hello when joining or when someone joins the channel.
	"""
	if data.find('JOIN') != -1:
		time.sleep(1)
		send_msg('Hello!')

def reconnect():
	"""
	Reconnect the bot if kicked.
	"""
	if data.find('KICK') != -1:
		irc.send('JOIN ' + chan + '\r\n')

def quitbot():
	"""
	Quit the bot.
	"""
	if data.find(' PRIVMSG ' + chan + ' :!bot quit') != -1:

		# say hello message
		with open ('./dict/quit', 'r') as w:
			wordlist = w.readlines()
			quit_message = random.choice(wordlist)
		irc.send('QUIT :' + quit_message + '\r\n')
		print '\n:DISCONNECTING\n\n'
		time.sleep(1)
		sys.exit(0)

# run HodlBot!
if __name__ == "__main__":
	main()
