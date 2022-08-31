import pygame, sys
from pygame.locals import *

#set up windows
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
FPS = 60

#set up colors
BG_COLOR = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

def leer_puntos(archivo='./dino.txt'):
    # Toma el archivo y crea una lista de puntos.
    puntos = []
    datos = open(archivo)
    try:
        for linea in datos:
            x, y = linea.split(',')
            puntos.append((int(x), int(y)))
    except:
        print(f'Error al abrir el archivo {archivo}')
    finally:
        datos.close()
    return puntos

def poligono(lista_puntos):
    puntos = lista_puntos
    p1 = puntos[0]
    linea = 0
    for p2 in puntos[1:]:        
        #pygame.draw.aaline(canvas, (200, 200, 255), p1, p2)        
        draw_line(p1, p2)
        p1 = p2

def putPixel(point, color):
    """dibuja un pixel en la ventana"""
    global pixel_size
    x, y = point
    rect = pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size)
    pygame.draw.rect(DISPLAYSURF, color, rect)

def resetWindow():
    """re-dibuja todos los pixeles de la ventana"""
    global grid
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            putPixel((x,y), BG_COLOR)

def fill_colour(point, alpha=1):
    """dibuja el pixel en (x, y) con transparencia alpha (donde 0≤ alpha ≤ 1)"""
    global color
    def rgba_color(bg, fg): return round(alpha * fg + (1-alpha) * bg)
    colour = tuple(map(rgba_color, BG_COLOR, color))
    putPixel(point, colour)

def fPart(x):
    """retorna parte fraccional de x"""
    return x - int(x)

def rfPart(x):
    """retorna 1 - la parte fraccional de x"""
    return 1 - fPart(x)
    
def draw_line(point1, point2):
    """dibuja una linea anti-aliased con el algoritmo xiaolin wu"""
    x1, y1 = point1
    x2, y2 = point2
    dx, dy = x2 - x1, y2 - y1
    
    if(abs(dx) > abs(dy)):
    # linea sobre el eje-x
        if(x2 < x1):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        gradient = dy/dx
        # primer endpoint
        xend = float(round(x1))
        yend = y1 + gradient * (xend - x1)
        xgap = rfPart(x1 + 0.5)
        xpxl1 = int(xend)
        ypxl1 = int(yend)
        fill_colour((xpxl1, ypxl1), rfPart(yend) * xgap)
        fill_colour((xpxl1, ypxl1+1), rfPart(yend) * xgap)

        # primera interseccion con el eje-y (para el main loop)
        intery = yend + gradient

        # segundo endpoint
        xend = float(round(x2))
        yend = y2 + gradient * (xend - x2)
        xgap = rfPart(x2 + 0.5)
        xpxl2 = int(xend)
        ypxl2 = int(yend)
        fill_colour((xpxl2, ypxl2), rfPart(yend) * xgap)
        fill_colour((xpxl2, ypxl2+1), rfPart(yend) * xgap)
        
        # main loop
        for x in range(xpxl1+1, xpxl2):
            fill_colour((x, int(intery)), rfPart(intery))
            fill_colour((x, int(intery)+1), fPart(intery))
            intery += gradient
    else:
    # linea sobre el eje-y
        if(y2 < y1):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        gradient = dx/dy
        # primer endpoint
        yend = float(round(y1))
        xend = x1 + gradient * (yend - y1)
        ygap = rfPart(y1 + 0.5)
        ypxl1 = int(yend)
        xpxl1 = int(xend)
        fill_colour((xpxl1, ypxl1), rfPart(xend) * ygap)
        fill_colour((xpxl1, ypxl1+1), rfPart(xend) * ygap)

        # primera interseccion con el eje-x (para el main loop)
        interx = xend + gradient

        # segundo endpoint
        yend = float(round(y2))
        xend = x2 + gradient * (yend - y2)
        ygap = rfPart(y2 + 0.5)
        ypxl2 = int(yend)
        xpxl2 = int(xend)
        fill_colour((xpxl2, ypxl2), rfPart(xend) * ygap)
        fill_colour((xpxl2, ypxl2+1), rfPart(xend) * ygap)

        # main loop
        for y in range(ypxl1+1, ypxl2):
            fill_colour((int(interx), y), rfPart(interx))
            fill_colour((int(interx)+1, y), rfPart(interx))
            interx += gradient

if __name__ == '__main__':
    global FPSCLOCK, grid, pixel_size

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('aaline')

    color = RED
    pixel_size = 1
    
    print("\n\tZoom config:")
    print("\t\tzoom (+): space")
    print("\t\tzoom (-): backspace")

    # game loop
    while True:        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if (pixel_size < 8):
                        pixel_size += 1
                if event.key == K_BACKSPACE:
                    if (pixel_size != 1):
                        pixel_size -= 1
                resetWindow()

        # draw_line((1, 100), (90, 100))
        # draw_line((200, 100), (200, 150))
        # draw_line((5, 5), (130, 122))
        #pygame.draw.aaline(DISPLAYSURF, color, (5, 20), (120, 152))
        poligono(leer_puntos(archivo='./dino.txt'))
        pygame.display.update()
