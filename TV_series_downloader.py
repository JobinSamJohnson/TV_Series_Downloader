from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from time import sleep


def find_series():
	series = []
	while True:
		while True:
			s = raw_input("Enter the name of the tv show : ") + ' '
			if s == ' ':
				continue
			ans = raw_input("Do u want to continue   y/n : ")
			if ans == 'y':
				break
		source = requests.get('http://onwatchseries.to/search/' + s)

		if "Please be more specific with your search." in source.content :
			print "Please be more specific with your search"
		elif "Sorry we do not have any results for that search." in source.content:
			print "Sorry we do not have any results for that search"
		else:
			break
	soup = BeautifulSoup(source.content,'html.parser')
	for n in soup.find_all('a') :
		if '/serie/' in n['href'].encode('utf-8') and n['href'].encode('utf-8') not in series :
			series.append(n['href'].encode('utf-8'))


	for i in range(len(series)):
		print "\n----------------------------------------------------------------------------------------------------------------"
		print '%3d' % (i + 1),". ",series[i][series[i].index('serie/') + 6:].replace("_"," ").capitalize()
		for k in soup.find_all('a',href=True):
			if series[i][series[i].index('serie/') + 6:].replace('_','-').lower() in k['href'].encode('utf-8').lower() and 'tvbuzer' in k['href'].encode('utf-8'):
				soup1=BeautifulSoup(requests.get(k['href']).content,'html.parser')
				for j in soup1.find_all('span',itemprop=True):
					if j['itemprop'].encode('utf-8')=="description":
						print j.text.encode('utf-8')
						break
				break
	while True:
		while True:
			try:
				number_s = input("\nEnter the number corresponding to the serie : ") - 1
			except :
				continue
			if len(series) - 1 < number_s or number_s < 0:
				print "Enter the correct number"
			else:
				break

		ans = raw_input("Do u want to continue   y/n : ")
		if ans == 'y':
			break
	link = series[number_s]
	os.system('cls')
	return link,series[number_s][7:]


def find_episodes(link):
	episode = []
	source = requests.get(link)
	soup = BeautifulSoup(source.content,'html.parser')

	for n in soup.find_all('a',href=True) :
		if '/episode/' in n['href'].encode('utf-8') and n['href'].encode('utf-8') not in episode:
			episode.append(n['href'].encode('utf-8'))


	b = int(episode[0][::-1][episode[0][::-1].index("_") + 1:episode[0][::-1].index("s")][::-1])

	season = []
	for n in range(1,b + 1):
		lseason = []
		for i in episode:
			if "_s" + str(n) + "_" in i:
				lseason.append(i)
		season.append(lseason)

	del episode
	season = sort_seasons(season)
	for i in range(len(season)):
		print "Season :",i + 1
		for j in range(len(season[i])):
			print '%3d' % (j + 1),". ",season[i][j][season[i][j].index("episode/") + 8:season[i][j].index(".html")].replace("_"," ").upper()
	while True:
		while True:
			try:
				number_s = input("Enter the number corresponding to the season : ") - 1

			except :
				print "Sorry please enter the correct season !"
				continue
			try:
				number_e = input("Enter the number corresponding to the episode : ") - 1
			except :
				print "Sorry please enter the correct episode !"
				continue
			if len(season) - 1 < number_s or number_s < 0:
				print "Sorry please enter the correct season !"
			elif len(season[number_s]) - 1 < number_e or number_e < 0:
				print "Sorry please enter the correct episode !"
			else:
				break
		ans = raw_input("do u want to continue   y/n : ")
		if ans == 'y':
			break
	link = season[number_s][number_e]
	os.system('cls')
	return link,season[number_s][number_e][season[number_s][number_e].index("/episode/")+9:season[number_s][number_e].index(".html")]


def sort_seasons(s=[]):
	for i in range(len(s)):
		for j in range(len(s[i])):
			for k in range(j,len(s[i])):
				if int(s[i][j][s[i][j].rindex("_e") + 2:s[i][j].index(".html")]) > int(s[i][k][s[i][k].rindex("_e") + 2:s[i][k].index(".html")]):
					s[i][j],s[i][k] = s[i][k],s[i][j]
	return s

def find_season(link):
	episode = []
	source = requests.get(link)
	soup = BeautifulSoup(source.content, 'html.parser')

	for n in soup.find_all('a', href=True):
		if '/episode/' in n['href'].encode('utf-8') and n['href'].encode('utf-8') not in episode:
			episode.append(n['href'].encode('utf-8'))

	b = int(episode[0][::-1][episode[0][::-1].index("_") + 1:episode[0][::-1].index("s")])
	season = []
	for n in range(1,b + 1):
		lseason = []
		for i in episode:
			if "_s" + str(n) + "_" in i:
				lseason.append(i)
		season.append(lseason)

	del episode
	season = sort_seasons(season)
	for i in range(len(season)):
		print "Season : ",i + 1
	while True:
		try:
			number_s = input("Enter the season you want to download : ")- 1
			if len(season) - 1 < number_s or number_s < 0:
					print "Sorry please enter the correct season !"
					continue
		except:
			continue
		ans = raw_input("Do u want to continue   y/n : ")
		if ans == 'y':
			break
	os.system('cls')
	if os.path.isdir(season[number_s][0][season[number_s][0].index("/episode/")+9:season[number_s][0].rindex('_e')]) == False:
		os.mkdir(season[number_s][0][season[number_s][0].index("/episode/")+9:season[number_s][0].rindex('_e')])
	for i in range(len(season[number_s])):
		d_link, ext = find_source(season[number_s][i])
		print "Downloading episode ",i + 1,"of ",len(season[number_s])," "
		if d_link == "-1" and ext == "-1":
			print "\nSorry ",season[number_s][i][season[number_s][i].index("episode/") + 8:season[number_s][i].index(".html")].replace("_"," ")," is not out yet !"
		else:
			os.chdir(season[number_s][0][season[number_s][0].index("/episode/")+9:season[number_s][0].rindex('_e')])
			download(d_link,season[number_s][i][season[number_s][i].index("/episode/")+9:season[number_s][i].index(".html")], ext)
			os.chdir('..')


def find_source(link):
	print "Loading [||||                ]\r",
	source = requests.get(link)
	soup = BeautifulSoup(source.content,'html.parser')

	temp_link = ' '

	for n in soup.find_all('a',href=True,title=True):
		if "gorillavid.in" in n['title'].encode('utf-8') and '/cale.html' in n['href'].encode('utf-8'):
			temp_link = n['href'].encode('utf-8')
			break
	dr = webdriver.PhantomJS()
	dr.get(temp_link)

	for i in dr.find_elements_by_tag_name('a'):
		if 'gorillavid.in' in i.get_attribute('href').encode('utf-8'):
			temp_link = i.get_attribute('href').encode('utf-8')
			break

	dr.get(temp_link)
	print "Loading [||||||||            ]"+'\r',
	try:
		dr.find_element_by_id("btn_download").click()
	except NoSuchElementException:
		return "-1","-1"

	while True:
		try:
			dr.find_element_by_id("btn_download").click()
		except NoSuchElementException:
			print 'Loading [||||||||||||        ]\r',
			break
	t=[]
	t=dr.page_source.encode('utf-8').split('\n')
	for i in t:
		temp_link=i
		if '.mp4' in temp_link:
			break
	dwnld_link = temp_link[14:temp_link.index('.mp4\',')+4]

	return dwnld_link,'mp4'

def download(link,episode,ext):
	play = 0
	print "Loading [||||||||||||||||||||]\r",
	try:
		r = requests.head(link,headers={'Accept-Encoding': 'identity'})
		size = int(r.headers['content-length'])
		chunk = 0
		source = requests.get(link,stream=True)
		f = open(episode + '.' + ext,'wb')
		for p in source.iter_content(chunk_size=512):
			if p:
				f.write(p)
				print "Downloading ....",episode,"....",1+((chunk * 100) / size)," % complete \r",
			chunk+=512
			"""try:
				sleep(0.1)
			except KeyboardInterrupt:
				play = input()
				while play == 1:
					print "Download PAUSED........Enter 0 to continue download "
					play = input()"""

		f.close()
	except ConnectionError:
		print  'Sorry ',episode ,' failed to download '
	print
a = 'y'
count =0

try:
	while a == 'y':
		link_s,series = find_series()
		print "Enter : "
		print "1. To download by episode"
		print "2. To download by season"
		while True:
			try:
				ch = int(raw_input("Enter your choice : "))
			except :
				continue
			if ch == 1:
				link_e, episode = find_episodes(link_s)
				d_link, ext = find_source(link_e)
				if d_link == "-1" and ext == "-1":
					print "Sorry ",episode.replace("_"," ")," is not out yet !"
					break
				else:
					if os.path.isdir(episode[:episode.rindex('_e')]) == False:
						os.mkdir(episode[:episode.rindex('_e')])
					os.chdir(episode[:episode.rindex('_e')])
					download(d_link,episode, ext)
					os.chdir('..')
					print "Download Complete"
					break
			elif ch == 2:
				find_season(link_s)
				print "\n\nDownload Complete"
				break
		a = raw_input("Enter 'y' to continue or 'n' to exit : ")
except ConnectionError:
	print "Please check your internet connection"
