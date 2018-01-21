from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys

def download(w):
	command_tokens = [
	    'youtube-dl',
	    '--extract-audio',
	    '--audio-format mp3',
	    '--audio-quality 0',
	    '--output \'%(title)s.%(ext)s\'',
	    w]

	command = ' '.join(command_tokens)
	os.system(command)

def downloadv(w):
	command_tokens = [
	    'youtube-dl',
	    '-f best',
	    '-ciw',
	    '--output \'%(title)s.%(ext)s\'',
	    w]

	command = ' '.join(command_tokens)
	os.system(command)
	
def downloadp(w):
	command_tokens = [
		'youtube-dl',
		'-cit',
		w]
	command = ' '.join(command_tokens)
	os.system(command)


def get_url(driver, a):
	url = 'https://www.youtube.com/results?search_query=' + a
	driver.get(url)
	w = WebDriverWait(driver, 20).until(lambda driver : driver.find_element_by_xpath('//*[@id="video-title"]').get_attribute("href"))
	return w

def get_channel_url(driver, a):
	url = 'https://www.youtube.com/results?search_query=' + a
	driver.get(url)
	w = WebDriverWait(driver, 20).until(lambda driver : driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[3]/ytd-item-section-renderer/div[2]/ytd-channel-renderer/a').get_attribute("href"))
	return w

def get_playlist_url(driver, a):
	url = 'https://www.youtube.com/results?search_query=' + a
	driver.get(url)
	w = WebDriverWait(driver, 20).until(lambda driver : driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[3]/ytd-item-section-renderer/div[2]/ytd-playlist-renderer[1]/div/a').get_attribute("href"))
	w = w.split('=')
	print(w[2])
	p = 'https://www.youtube.com/playlist?list=' + w[2]
	return p

def get_play_url(driver, a) :
	url = 'https://www.youtube.com/results?search_query=' + a
	driver.get(url)
	
	SongList = []
	try:
		for i in range(1, 6):
			s = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[3]/ytd-item-section-renderer/div[2]/ytd-playlist-renderer["+ str(i) +"]/div/a"
			w = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(s).get_attribute("href"))
			w = w.split('=')
			p = 'https://www.youtube.com/playlist?list=' + w[2]
			s = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[3]/ytd-item-section-renderer/div[2]/ytd-playlist-renderer["+ str(i) +"]/div/a/h3/span"
			SongName = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(s).get_attribute("title"))
			print "[" + str(i) + "] " + SongName
			SongList.append(p)
		k = raw_input('Selection --> ')
		url = SongList[int(k)-1]
		return url
	except:
		pass


def getlist(driver, a) :
	url = 'https://www.youtube.com/results?search_query=' + a
	driver.get(url)
	
	SongList = []
	for i in range(1, 11):
		s = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[3]/ytd-item-section-renderer/div[2]/ytd-video-renderer[" + str(i) + "]/div[1]/div/div[1]/div/h3/a"
		w = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(s).get_attribute("href"))
		SongName = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(s).get_attribute("title"))
		print "[" + str(i) + "] " + SongName
		SongList.append(w)
	k = raw_input('Selection --> ')
	url = SongList[int(k)-1]
	return url

def main():
	driver = webdriver.Firefox()
	
	if '-f' in sys.argv[1:]:
		with open(sys.argv[2], 'r') as f:
                	songs = f.readlines()
                	print(songs)
                	songs = map(lambda s: s.strip().split(" "), songs)
                	songs = map(lambda s:"+".join(s), songs)
                	for i in songs:
                		url = get_url(driver, i)
                		download(url)

	elif '-fv' in sys.argv[1:]:
		with open(sys.argv[2], 'r') as f:
                	songs = f.readlines()
                	print(songs)
                	songs = map(lambda s: s.strip().split(" "), songs)
                	songs = map(lambda s:"+".join(s), songs)
                	for i in songs:
                		url = get_url(driver, i)
                		downloadv(url)

	else:
		if '-c' in sys.argv[1:]:
			a = raw_input('Channel Name --> ').strip().split(" ")
			a = "+".join(a)
			url = get_channel_url(driver, a)
			print(url)
			
		elif '-p' in sys.argv[1:]:
			a = raw_input('Playlist Name --> ').strip().split(" ")
			a = "+".join(a)
			url = get_playlist_url(driver, a)
			print(url)
		
		elif '-pl' in sys.argv[1:]:
			a = raw_input('Playlist Name --> ').strip().split(" ")
			a = "+".join(a)
			url = get_play_url(driver, a)
			print(url)
			
		elif '-l' in sys.argv[1:]:
			a = raw_input('Song/Video Name --> ').strip().split(" ")
			a = "+".join(a)
			url = getlist(driver, a)
			print(url)
		
		else:
			a = raw_input('Song/Video Name --> ').strip().split(" ")
			a = "+".join(a)
			url = get_url(driver, a)
			print(url)
		
		if '-v' in sys.argv[1:]:
			downloadv(url)
		elif '-p' or '-pl' in sys.argv[1:]:
			downloadp(url)
		else:
			download(url)
		
	driver.close()
	
if __name__ == '__main__':
    main()
