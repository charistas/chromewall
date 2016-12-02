#!/usr/bin/python
from urllib import urlretrieve
from os import path, system
from sys import platform, argv
from os.path import expanduser
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html

class Render(QWebPage):
	"""Handle the JavaScript rendering of the given webpage."""
	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def _loadFinished(self, result):
		self.frame = self.mainFrame()
		self.app.quit()

def get_screenshot_url():
	"""Load Chromecast homepage and get the URL of the current wallpaper."""
	url = 'https://clients3.google.com/cast/chromecast/home'
	render = Render(url)  
	source_code = render.frame.toHtml()
	formatted_source_code = str(source_code.toAscii())
	tree = html.fromstring(formatted_source_code)
	url = tree.xpath('//*[@id="picture-background"]/@src')[0]
	return url

def get_file_path():
	"""Construct the wallpaper's file path."""
	folder_path = expanduser("~/Pictures")
	file_name= "chromecast_wallpaper.jpg"
	file_path = folder_path + file_name
	if not os.path.exists(folder_path):
		raise OSError("Cannot locate Pictures folder path.")
	return file_path

def main():
	"""Set the current Chromecast wallpaper as this machine's wallpaper."""
	if not (platform == "linux" or platform == "linux2"):
		raise OSError("System is not running Linux.")
	print "1/2 Downloading wallpaper."
	fp = get_file_path()
	urllib.urlretrieve(get_screenshot_url(), fp)
	print "2/2 Updating wallpaper."
	os.system("gsettings set org.gnome.desktop.background picture-uri 'file://" +get_file_path() +"'")
	print "All done!"

if __name__ == "__main__":
    main()