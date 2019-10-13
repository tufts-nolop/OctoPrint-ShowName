# coding=utf-8
from __future__ import absolute_import
import time
import socket

import octoprint.plugin
import octoprint.util
from octoprint.events import Events

class ShowNamePlugin(octoprint.plugin.EventHandlerPlugin,
                     octoprint.plugin.SettingsPlugin):
	_printname = ''
	_ownername = ''
	_username = ''
	def on_event(self, event, payload):
		if event == Events.PRINT_STARTED:
			_printname = payload['name']
			_ownername = payload['owner']
			_username = payload['user']
			self._printer.commands('M117 User: {}'.format(_username))
		elif event == Events.PRINT_DONE:
			self._printer.commands('M117 [{}] Print Done'.format(_username))
		elif event == Events.PRINT_FAILED:
			self._printer.commands('M117 [{}] Print Failed'.format(_username))
		elif event == Events.PRINT_CANCELLED:
			self._printer.commands('M117 [{}] Print Cancelled'.format(_username))
		elif event == Events.CONNECTED:
			ip = self._get_host_ip()
			if not ip:
				return
			self._printer.commands("M117 IP {}".format(ip))

	def do_work(self):
		if not self._printer.is_printing():
			# Don't do things.
			return

	def _get_host_ip(self):
		return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			detailedprogress=dict(
				displayName="ShowName Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Nolop",
				repo="OctoPrint-DetailedProgress",
				current=self._plugin_version,

			)
		)

__plugin_name__ = "Show Name Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ShowNamePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
	}

