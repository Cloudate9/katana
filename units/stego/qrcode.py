from unit import BaseUnit
from collections import Counter
import sys
from io import StringIO
import argparse
from pwn import *
import subprocess
import units.raw
import util

class Unit(units.raw.RawUnit):

	@classmethod
	def prepare_parser(cls, config, parser):
		pass

	def evaluate(self, target):

		try:
			p = subprocess.Popen(['zbarimg', target ], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except FileNotFoundError as e:
			if "No such file or directory: 'zbarimg'" in e.args:
				log.failure("zbarimg is not in the PATH (not installed)? Cannot run the stego.qrcode unit!")
				return None

		results = util.process_output(p)
		# "scanned 2 barcode symbols from 2 images in 0.09 seconds"
		count = int(results['stderr'][0].split(' ')[1])

		if count == 0:
			return None

		results = '\n'.join(results['stdout'])
		things = results.split(':')
		typ = things[0]
		things = ':'.join(things[1:])

		return { 'type': typ, 'content': things }