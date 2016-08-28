#!/usr/bin/python
#coding:utf-8

#在贪食蛇游戏中加入简单的文字

import pygame
import sys
from pygame.locals import *
from random import randrange
import time


up = lambda x:(x[0]-1,x[1])
down = lambda x:(x[0]+1,x[1])
left = lambda x:(x[0],x[1]-1)
right = lambda x:(x[0],x[1]+1)

turn_up = 0
turn_down = 0 
turn_left = lambda x:x<3 and x+1 or 0
turn_right = lambda x:x==0 and 3 or x-1
dire = [up,left,down,right]
move = lambda x,y:[y(x[0])]+x[:-1] #移动一格，list拼接，舍弃原来list的最后一个元素
grow = lambda x,y:[y(x[0])]+x #长度增加一格，list拼接，把增长的一格加在头部

s = [(5,5),(5,6),(5,7)]
d = up

food = randrange(0,30),randrange(0,40)

FPSCLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_mode((800,600))
pygame.mouse.set_visible(0)
screen = pygame.display.get_surface()
screen.fill((255,255,255))
times = 0.0

my_font = pygame.font.SysFont("arial",64)
text_surface = my_font.render("GAME OVER!",True,(255,0,0),(0,0,0))

while True:
	screen.fill((0,0,0)) 
	time_passed = FPSCLOCK.tick(30)
	#修改这个条件判断中的数值可以控制蛇移动的快慢/绘图的反应速度？
	if times>200:
		times = 0.0
		s = move(s,d)
	else:
		times += time_passed

	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		if event.type == KEYDOWN and event.key == K_UP:
			d = up
		if event.type == KEYDOWN and event.key == K_LEFT:
			#d = dire[turn_left(dire.index(d))]
			d = left
		if event.type == KEYDOWN and event.key == K_RIGHT:
			#d =dire[turn_right(dire.index(d))]
			d =right
		if event.type == KEYDOWN and event.key == K_DOWN:
			d = down
	if s[0] == food:
		s = grow(s,d)
		food = randrange(0,30),randrange(0,40)
	if s[0] in s[1:] or s[0][0]<0 or s[0][0] >= 30 or s[0][1]<0 or s[0][1]>=40: 
		x = screen.get_width()/2-text_surface.get_width()/2
		y = screen.get_height()/2-text_surface.get_height()/2
		screen.blit(text_surface,(x,y))
		pygame.display.update()
		time.sleep(2)
		break 

	
	for r,c in s: 
		pygame.draw.rect(screen,(255,0,0),(c*20,r*20,20,20)) 
	pygame.draw.rect(screen,(0,255,0),(food[1]*20,food[0]*20,20,20)) 
	pygame.display.update() 