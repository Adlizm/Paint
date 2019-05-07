import pygame
import math

width,height = 640,500
run = True;

nextPoints = []
nClick = 0 
nPontC = 0
clicked = 0
Pxs = []

black = (0,0,0)
white = (255,255,255)

colorSelected = black

typeTool = {
	'line': False,
	'rect': False,
	'circle': False,
	'polygon': False,
	'curve': False,
	'square': False,
	'fill': False 
}

btWidth = 40
btHeight = 30

mouseX = None
mouseY = None

def Fill(x,y,color,getcolor):
	global imgScreen
	pilha = []
	if getcolor != color:
		screen.set_at((x,y),color)
		pilha.append((x,y))
		while len(pilha) > 0:
			index = len(pilha)-1
			x = pilha[index][0]
			y = pilha[index][1]
			ok = False		
			if x-1 >= 0 and screen.get_at((x-1,y)) == getcolor:
				pilha.append((x-1,y))
				screen.set_at((x-1,y),color)
				ok = True
			elif x+1 < width and screen.get_at((x+1,y)) == getcolor:
				pilha.append((x+1,y))
				screen.set_at((x+1,y),color)
				ok = True
			elif y-1 > btHeight and screen.get_at((x,y-1)) == getcolor:
				pilha.append((x,y-1))
				screen.set_at((x,y-1),color)
				ok = True
			elif y+1 < height and screen.get_at((x,y+1)) == getcolor:
				pilha.append((x,y+1))
				screen.set_at((x,y+1),color)
				ok = True
			else:
				pilha.pop(len(pilha)-1)

	pygame.image.save(screen,'screen.png')

def Line(x0, y0, x1, y1,color):
	dx = math.fabs(x1 - x0)
	dy = math.fabs(y1 - y0)

	if x0 < x1:
		sx = 1
	else:
		sx = -1
	if y0 < y1:
		sy = 1
	else:
		sy = -1
	if dx > dy:
		err = dx/2
	else:
		err = -dy/2

	while True:
		screen.set_at((x0,y0),color)
		if x0 == x1 and y0 == y1:
			break
		e2 = err
		if e2 > -dx:
			err = err - dy
			x0 = x0 + sx
		if e2 < dy:
			err = err + dx
			y0 = y0 + sy
			
def Circle(cx,cy,r,color):
	x = r
	y = 0
	e = 0
	while y <= x:
		for i in range(4):
			screen.set_at(( x + cx, y + cy),color)
			screen.set_at(( y + cx, x + cy),color)
			if i%2 == 0:
				x = -x
			else:
				y = -y
		e = e + 2*y + 1
		y = y + 1
		if (2*e) > (2*x -1):
			x = x - 1
			e = e - 2*x + 1

def Rect(x1,y1,x2,y2,color):
	Line(x1,y1,x1,y2,color)
	Line(x1,y1,x2,y1,color)
	Line(x2,y2,x2,y1,color)
	Line(x2,y2,x1,y2,color)

def Polygon(pt,color):
	length = len(pt)
	for i in range(0,length - 2,2):
		Line(pt[i],pt[i + 1],pt[i + 2],pt[i + 3],color)
	Line(pt[0],pt[1],pt[length - 2],pt[length - 1],color)


def Curve(x1,y1,x2,y2,x3,y3,x4,y4,color):
	p = 100
	increment = 1/p
	t = 0;
	x0 = x1
	y0 = y1
	for i in range(p):
		t2 = t*t
		t3 = t2 * t

		x = (-t3 + 3*t2 - 3*t + 1)*x1 + (3*t3 - 6*t2 + 3*t)*x2 + (-3*t3 + 3*t2)*x3+ t3*x4
		y = (-t3 + 3*t2 - 3*t + 1)*y1 + (3*t3 - 6*t2 + 3*t)*y2 + (-3*t3 + 3*t2)*y3+ t3*y4
		x = round(x)
		y = round(y)

		Line(x0,y0,x,y,color) 
		x0 = x
		y0 = y
		t = t + increment

def Square(x1,y1,x2,y2,color):
	dx = x1 - x2
	dy = y1 - y2
	
	w = math.ceil(math.sqrt(dx*dx + dy*dy)/math.sqrt(2))
	if x1 > x2:
		if y1 > y2:
			Rect(x1,y1,x1 - w,y1 - w,color)
		else:
			Rect(x1,y1,x1 - w,y1 + w,color)
	else:
		if y1 > y2:
			Rect(x1,y1,x1 + w,y1 - w,color)
		else:
			Rect(x1,y1,x1 + w,y1 + w,color)

def mouseDown(pos,button):
	global clicked,colorSelected
	if pos[1] <= btHeight:
		if typeTool['polygon']:
			pygame.image.save(screen,'screen.png')
			nextPoints.clear()
		
		if pos[0] < btWidth:
			select('l')
		elif pos[0] < btWidth*2:
			select('r')
		elif pos[0] < btWidth*3:
			select('c')
		elif pos[0] < btWidth*4:
			select('p')
		elif pos[0] < btWidth*5:
			select('s')
		elif pos[0] < btWidth*6:
			select('q')
		elif pos[0] < btWidth*7:
			select('f')
		elif pos[0] > 370 and pos[0] < 630:
			x = math.ceil((pos[0] - 370)/32.5) - 1
			if pos[1] <= btHeight/2:
				y = 0
			else:
				y = 1
			x = 380 + x*32
			y = y*15 + 10

			colorSelected = screen.get_at((x,y))
			print(colorSelected)
		clicked = 0
	else:
		if button == 1:
			if typeTool['fill']:
				getcolor = screen.get_at((pos[0],pos[1]))
				Fill(pos[0],pos[1],colorSelected,getcolor)
			else:
				clicked = clicked + 1
				nextPoints.append(pos[0]);
				nextPoints.append(pos[1]);
				if clicked == 4 and typeTool['curve'] :
					pygame.image.save(screen,'screen.png')					
					clicked = 0
					nextPoints.clear()
		else:
			if typeTool['polygon']:
				pygame.image.save(screen,'screen.png')	
				nextPoints.clear()
				clicked = 0
			
def mouseUp(pos,button):
	global clicked
	global nextPoints
	global nPontC

	if (nPontC == 2 and len(nextPoints) > 0 and button == 1):
		pygame.image.save(screen,'screen.png')
		nextPoints.clear()
		clicked = 0

def select(t):
	global nPontC

	typeTool['line'] = False
	typeTool['rect'] = False
	typeTool['square'] = False
	typeTool['circle'] = False
	typeTool['polygon'] = False
	typeTool['curve'] = False
	typeTool['fill'] = False
	if t == 'r':
		typeTool['rect'] = True
		nPontC = 2
	elif t == 'p':
		typeTool['polygon'] = True
		nPontC = None
	elif t == 'c':
		typeTool['circle'] = True
		nPontC = 2
	elif t == 'l':
		typeTool['line'] = True
		nPontC = 2
	elif t == 's':
		typeTool['curve'] = True
		nPontC = 4
	elif t == 'q':
		typeTool['square'] = True
		nPontC = 2
	elif t == 'f':
		typeTool['fill'] = True
		nPontC = 1

def mouseMove(pos):
	global mouseX
	global mouseY

	mouseX = pos[0]
	mouseY = pos[1]

def drawFigureInDev():
	global mouseX
	global mouseY
	global clicked
	global nextPoints
	global nPontC

	if len(nextPoints) >= 2:
		if len(nextPoints) == 2 and nPontC == 2:
			if typeTool['line']:
				Line(mouseX,mouseY,nextPoints[0],nextPoints[1],colorSelected)
			elif typeTool['rect']:
				Rect(mouseX,mouseY,nextPoints[0],nextPoints[1],colorSelected)
			elif typeTool['circle']:
				dx = mouseX - nextPoints[0]
				dy = mouseY - nextPoints[1]
				r = int(math.sqrt(dx*dx + dy*dy))
				Circle(nextPoints[0],nextPoints[1],r,colorSelected)
			elif typeTool['square']:
				Square(nextPoints[0],nextPoints[1],mouseX,mouseY,colorSelected)
		elif typeTool['curve']:
			pt = []
			length = len(nextPoints)
			for index in range(nPontC*2):
				if index >= length - 1 and index%2 == 0:
					pt.append(mouseX)
					pt.append(mouseY)
				elif index < length:
					pt.append(nextPoints[index])
			Curve(pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],colorSelected)
		elif typeTool['polygon']:
			if clicked == 1:
				Line(nextPoints[0],nextPoints[1],mouseX,mouseY,colorSelected)
			else:
				pt = []
				for index in range(len(nextPoints)):
					pt.append(nextPoints[index])
				pt.append(mouseX)
				pt.append(mouseY)
				Polygon(pt,colorSelected)


pygame.init()
pygame.display.set_caption("Trabalho Computacao Grafica")
screen = pygame.display.set_mode((width,height))
screen.fill(white)
pygame.image.save(screen,'screen.png')


clock = pygame.time.Clock();
imgScreen = None
imgTools = pygame.image.load ('mainPaint.jpg')

while run: 
	imgScreen = pygame.image.load('screen.png')
	screen.blit(imgScreen,(0,0))

	drawFigureInDev()
	screen.blit(imgTools,(0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEMOTION:
			mouseMove(event.pos)
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown(event.pos,event.button)
		if event.type == pygame.MOUSEBUTTONUP:
			mouseUp(event.pos,event.button)
	
	pygame.display.flip()
	clock.tick(30)	