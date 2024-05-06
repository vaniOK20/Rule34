import requests
from bs4 import BeautifulSoup
import random as ran

def print_html(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
		return response.text
	except requests.RequestException as e:
		print("Error fetching URL:", e)
		return None

def MaxPage(tag):
	html=BeautifulSoup(print_html(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}').strip(),'html.parser')
	page=html.find('a', alt="last page")
	if page is None:
		page=0
	else:
		page=str(page)[str(page).find('d=')+2:]
		page=str(page)[:str(page).find('"')]
		if int(page)>200000: page=200000
	return int(page)

def ShowRanUrl(page, tag):
	html=BeautifulSoup(print_html(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={page}').strip(),'html.parser')
	try:
		spans=html.find('div', class_="image-list").find_all('span')
	except Exception as e:
		return 'None'
	span=ran.choice(spans).find('a').get('href')# span=spans[i].find('img').get('src')
	try:
		imgV=BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('img', id="image").get('src')
	except Exception as e:
		imgV=BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('video', id="gelcomVideoPlayer").find('source').get('src')
	return imgV

def ShowUrl(page, tag, img):
	html=BeautifulSoup(print_html(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={page}').strip(),'html.parser')
	try:
		spans=html.find('div', class_="image-list").find_all('span')
	except Exception as e:
		return 'None'
	if len(spans)>=img:
		span=spans[img].find('a').get('href')
	else:
		return 'None'
	try:
		imgV=BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('img', id="image").get('src')
	except Exception as e:
		imgV=BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('video', id="gelcomVideoPlayer").find('source').get('src')
	return imgV

def GetTags(id_):
	html=BeautifulSoup(print_html(f'https://rule34.xxx/index.php?page=history&type=tag_history&id={id_}').strip(),'html.parser')
	html=html.find('div', id="content")
	try:
		html=html.find_all('tr')[1].find_all('a')
	except Exception as e:
		return 'None'
	text=''
	for i in range(len(html)-3):
		text=text+str(html[i+2].text+' ')
	text=text.replace('+', ' ').replace('-', ' ')
	return text

def ShowRanUrlMore(page, tag, count):
	tag=tag.replace(' ', '+')
	html=BeautifulSoup(print_html(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={page}').strip(),'html.parser')
	try:
		spans=html.find('div', class_="image-list").find_all('span')
	except Exception as e:
		return ['None']
	array=[]
	for i in range(count):
		span=ran.choice(spans).find('a').get('href')
		try:
			array.append(BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('img', id="image").get('src'))
		except Exception as e:
			array.append(BeautifulSoup(print_html('https://rule34.xxx'+span).strip(), 'html.parser').find('video', id="gelcomVideoPlayer").find('source').get('src'))
	return array