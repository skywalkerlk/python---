#!/usr/bin/python
#coding:utf-8


#2016年9月6日14:05:21
#用sprite的知识来改写snake游戏,注意有关snake的坐标都是y在前，x在后
#修改了初始界面，点击可变色按钮再进入游戏
#修改了点击按钮Restart游戏的界面，删除了is_over标志



import pygame
import sys
from pygame.locals import *
from random import randrange
import time


def print_text(text_surface,x,y):
	screen.blit(text_surface,(x,y))

class Button(object):
	"""按钮类，点击按钮之后执行相应的操作"""
	def __init__(self,position,up_image_file,down_image_file=None):
		self.position = position
		self.image = pygame.image.load(up_image_file)
		if down_image_file == None:
			pass
		else:
			self.down_image_file = pygame.image.load(down_image_file)
		self.game_start = False
		self.game_restart = False

	def render(self,surface):
		"""绘制按钮"""
		x, y = self.position
		w, h = self.image.get_size()
		x -= w/2
		y -= h/2 
		surface.blit(self.image,(x,y))

	def is_push(self):
		"""如果点击的范围在按钮自身的范围内，返回True"""
		point_x, point_y = pygame.mouse.get_pos()
		x, y = self.position
		w, h = self.image.get_size()
		x -= w/2
		y -= h/2
		if_in_x = point_x >= x and point_x < x+w 
		if_in_y = point_y >= y and point_y < y+h
		return if_in_x and if_in_y

	def is_start(self):
		if self.is_push():
			b1,b2,b3 = pygame.mouse.get_pressed()
			if b1 == True:
				self.game_start = True
	
	def is_restart(self):
		if self.is_push():
			b1,b2,b3 = pygame.mouse.get_pressed()
			if b1 == True:
				self.game_restart = True

	def render2(self,surface):
		x,y = self.position
		w,h = self.image.get_size()
		x -= w/2
		y -= h/2 
		if self.is_push(): #调用自己的函数，self.函数名
			surface.blit(self.down_image_file,(x,y))
		else:
			surface.blit(self.image,(x,y))


	def get_image_size(self):
		return self.image.get_size()



#精灵类————食物
class Food(pygame.sprite.Sprite):
	def __init__(self,color,position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20,20])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.topleft = position

	def getFoodPosition(self):
		return self.rect.y//20,self.rect.x//20 #y坐标在前


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
init_s = s
d = up

#food = randrange(0,30),randrange(0,40) #原来的“食物代码”,后面要乘以20
#创建精灵类————食物
food_position = randrange(0,40)*20,randrange(0,30)*20 #这里乘以20，getFoodPosition中除以20
food = Food((0,255,0),food_position)
food_group = pygame.sprite.Group()
food_group.add(food)


FPSCLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_mode((800,600))
pygame.mouse.set_visible(0)
screen = pygame.display.get_surface()
screen.fill((255,255,255))
times = 0.0

#游戏标志
is_over = False

#游戏初始界面文字：点击鼠标游戏开始
welcome_font = pygame.font.SysFont("arial",64)
welcome_text = welcome_font.render("Welcome To Play The Snake!",True,(0,255,0),(255,255,255))
button_x = 400
button_y = 400
up_image_file = "game_start_up.png"
down_image_file = "game_start_down.png"
buttons = {}
buttons["Start"] = Button((button_x,button_y),up_image_file,down_image_file)


#贪食蛇死亡时出现文字：贪食蛇碰到四周时显示GAME OVER字样
gameover_font = pygame.font.SysFont("arial",64)
gameover_text = gameover_font.render("GAME OVER!",True,(255,0,0),(255,255,255))

#在GAME OVER时，增加一个Restart的按钮
button_x = 400
button_y = 400
button_width = 30

buttons["Restart"] = Button((button_x,button_y),"Restart.png",None)
my_font = pygame.font.SysFont("arial",24)
restart_text = my_font.render("Restart",True,(0,0,0),(255,255,255))
w, h =buttons["Restart"].get_image_size() 
restart_font_x = button_x + button_width - w/2
restart_font_y = button_y - h/2



while True:
	flag = False
	restart_game = False
	screen.fill((255,255,255)) 
	time_passed = FPSCLOCK.tick(30)
	#修改这个条件判断中的数值可以控制蛇移动的快慢/绘图的反应速度？
	if times>100:
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
    
	pygame.mouse.set_visible(True)
	x = screen.get_width()/2-welcome_text.get_width()/2
	y = screen.get_height()/2-welcome_text.get_height()/2
	print_text(welcome_text,x,y)
	buttons["Start"].render2(screen)
	is_start = buttons["Start"].is_start()
	if buttons["Start"].game_start == True:
		if is_over:
			screen.fill((255,255,255)) #这句话不错，可以有“清屏”的效果
			x = screen.get_width()/2-gameover_text.get_width()/2
			y = screen.get_height()/2-gameover_text.get_height()/2
			print_text(gameover_text,x,y)
			pygame.mouse.set_visible(True)
			buttons["Restart"].render(screen)
			print_text(restart_text,restart_font_x,restart_font_y)
			s = init_s #初始化蛇的位置
			
			buttons["Restart"].is_restart()
			if buttons["Restart"].game_restart == True:
			    s = init_s #初始化蛇的位置
			    is_over = False
			    buttons["Restart"].game_restart = False #需要重置成False
		else:
			screen.fill((255,255,255))
			if s[0] == food.getFoodPosition():
				s = grow(s,d)
				food_group.remove(food)
				food_position = randrange(0,40)*20,randrange(0,30)*20 #食物被吃掉之后才重新刷新
				food = Food((0,255,0),food_position)
				food_group.add(food)
			if s[0] in s[1:] or s[0][0]<0 or s[0][0] >= 30 or s[0][1]<0 or s[0][1]>=40:
				is_over = True 
			for r,c in s: 
				pygame.draw.rect(screen,(255,0,0),(c*20,r*20,20,20))  
			food_group.draw(screen)

	pygame.display.update() 
