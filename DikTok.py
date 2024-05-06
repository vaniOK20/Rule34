import pygame
import requests
import random
import sys
import io
from io import BytesIO
import pyperclip
import cv2
import numpy as np
import zipfile
from rule34API import *

pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((500, 700))# Window size
pygame.display.set_caption("DikTok")# Title pygame

# Variables
black=(0, 0, 0)
white=(255, 255, 255)

buttons=[(440, 325, 'load'), (440, 425, 'download'), (250, 650, 'search'), (10, 10, 'back')]
history=[]

font=pygame.font.Font(None, 36)
play_anim=False
button_presed=False
search=False
key_presed=False
video=False
y=0
y_speed=0
x=0
search_text=''
tag='all'
video_history=None

# Loading GUI textures
with zipfile.ZipFile('GUI.package', 'r') as z:
	saveIM=z.read('save.png')
	loadIM=z.read('load.png')
	searchIM=z.read('search.png')
	backIM=z.read('back2.png')

saveIM=pygame.image.load(io.BytesIO(saveIM))
saveIM=pygame.transform.scale(saveIM, (50, 50))
loadIM=pygame.image.load(io.BytesIO(loadIM))
loadIM=pygame.transform.scale(loadIM, (50, 50))
searchIM=pygame.image.load(io.BytesIO(searchIM))
searchIM=pygame.transform.scale(searchIM, (50, 50))
backIM=pygame.image.load(io.BytesIO(backIM))
backIM=pygame.transform.scale(backIM, (50, 50))

# Function for load images from url
def LoadFromUrl(url):
	headers={
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
	}
	response=requests.get(url, headers=headers)
	try:
		image=pygame.image.load(BytesIO(response.content))
	except Exception as e:
		print(response.content)
		input()
	image=pygame.transform.scale(image, (500, 650))
	image_data=BytesIO(response.content)
	return image, image_data

# Load first image
max_page=MaxPage(tag)
page=random.randint(0, max_page)
url=ShowRanUrl(page, tag)
img, data=LoadFromUrl(url)
history.append((img, url))

# Loop of pygame
while True:
	for event in pygame.event.get():
		key_presed=False
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type==pygame.KEYDOWN and search:
			chart=event.unicode
			search_text=search_text+chart
			if event.key==pygame.K_BACKSPACE:
				search_text=search_text[:len(search_text)-2]
				chart=''
			if event.key==pygame.K_RETURN or event.key==1073741912:
				search_text=search_text[:len(search_text)-1]
				tag=search_text
				search=False
			if event.key==pygame.K_v and pygame.key.get_mods()&pygame.KMOD_CTRL:
				search_text=search_text[:len(search_text)-1]
				search_text=search_text+pyperclip.paste()

	# Geting Mouse position and click
	mouseC=pygame.mouse.get_pressed()
	mouseP=pygame.mouse.get_pos()

	# Animation system
	if play_anim:
		y_speed+=1
		y-=y_speed
	if y<=-650 and play_anim:
		img=img2
		y_speed=0
		y=0
		play_anim=False

	# Other
	if not mouseC[0]: button_presed=False

	# Video player system
	if video and not play_anim:
		ret, frame=cap.read()
		if ret:
			frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			pygame_frame=pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
			image=pygame.transform.scale(pygame_frame, (500, 650))
			img=image
		else:
			cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

	# Painting
	screen.fill(black)
	if not search: screen.blit(img, (0, y))
	if play_anim and not search: screen.blit(img2, (0, y+650))

	# Search system
	if search and pygame.key.get_pressed()[x] and not key_presed: key_presed=True

	if search:
		text=font.render(search_text, True, white)
		screen.blit(text, (200, 50))

	# Load buttons
	for i in buttons:
		# Drawing
		if i[2]=='download' and not search:
			screen.blit(saveIM, (i[0], i[1]))
		elif i[2]=='load' and not search:
			screen.blit(loadIM, (i[0], i[1]))
		elif i[2]=='search':
			screen.blit(searchIM, (i[0], i[1]))
		elif i[2]=='back':
			screen.blit(backIM, (i[0], i[1]))
		#else:
		#	pygame.draw.rect(screen, black, (i[0], i[1], 50, 50))
		#	text=font.render(i[2], True, white)
		#	screen.blit(text, (i[0]-len(i[2])*5, i[1]))

		# Test for click
		if mouseP[0]>i[0] and mouseP[0]-50<i[0] and mouseP[1]>i[1] and mouseP[1]-50<i[1] and mouseC[0] and not button_presed:
			if i[2]=='load':
				if video_history is None or video_history>=len(history):
					max_page=MaxPage(tag)
					page=random.randint(0, max_page)
					url=ShowRanUrl(page, tag)
					if url.find('.mp4')!=-1:
						img2, data=LoadFromUrl('https://rule34.xxx//samples/1294/sample_360bd16f090ce9c33b261c893bd350df.jpg?9893092')
						response=requests.get(url)
						data=response.content
						cap=cv2.VideoCapture(url)
						video=True
					else:
						video=False
						img2, data=LoadFromUrl(url)
						history.append((img, url))
					play_anim=True
				else:
					video_history+=1
					img, data=LoadFromUrl(history[video_history-1][1])
			elif i[2]=='download':
				try:
					with open(f'{random.randint(0, 90000)}.jpg', 'wb') as f:
						f.write(data.getvalue())
				except Exception as e:
					with open(f'{random.randint(0, 90000)}.mp4', 'wb') as f:
						f.write(data)
			elif i[2]=='search':
				search=True
			elif i[2]=='back':
				if not search:
					if video_history is None: video_history=len(history)
					video_history-=1
					img=history[video_history][0]
				else:
					search_text=''
					search=False
			button_presed=True

	pygame.display.flip()
	clock.tick(60)
