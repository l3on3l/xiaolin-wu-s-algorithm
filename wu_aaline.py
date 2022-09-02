import pygame, sys
from pygame.locals import *
from sys import argv
import time

#set up windows
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
FPS = 60

# set up pixel
MIN_PIXEL_SIZE = 1
MAX_PIXEL_SIZE = 10

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
        # pygame.draw.aaline(canvas, RED, p1, p2)
        draw_line(p1, p2)
        p1 = p2

def put_pixel(point, color):
    """dibuja un pixel en la ventana"""
    global pixel_size
    x, y = point
    rect = pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size)
    pygame.draw.rect(DISPLAYSURF, color, rect)

def reset_window():
    """re-dibuja todos los pixeles de la ventana"""
    global grid
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            put_pixel((x,y), BG_COLOR)

def fill_colour(point, alpha=1):
    """pinta el pixel en (x, y) con transparencia alpha (donde 0≤ alpha ≤ 1)"""
    global color
    def rgba_color(bg, fg): return round(alpha * fg + (1-alpha) * bg)
    colour = tuple(map(rgba_color, DISPLAYSURF.get_at(point)[:3], color))
    put_pixel(point, colour)

def fpart(x):
    """retorna parte fraccional de x"""
    return x - int(x)

def rfpart(x):
    """retorna 1 - la parte fraccional de x"""
    return 1 - fpart(x)

# para ahorrar lineas de codigo
def calc_point(x, y, steep):
    "retorna la coordenada (x,y) a dibuja, es una funcion XOR"
    if steep:
        return(y, x)
    else:
        return(x, y)

# para dibujar el primer y segundo endpoint de una linea
def draw_endpoint(point, gradient, steep):
    "dibuja el endpoint (x,y) de acuerdo al valor de la pendiente, retorna el punto a dibujar calculado"
    x, y = point
    xend = round(x)
    yend = y + gradient * (xend - x)
    xgap = rfpart(x + 0.5)
    xpxl, ypxl = int(xend), int(yend)
    fill_colour(calc_point(xpxl, ypxl, steep), rfpart(yend) * xgap)
    fill_colour(calc_point(xpxl, ypxl+1, steep), fpart(yend) * xgap)
    return xpxl

def draw_line(point1:tuple, point2:tuple, animated:bool=False):
    """Dibuja una linea anti-aliased desde point1 a point2 con el algoritmo xiaolin wu's."""
    x1, y1 = point1
    x2, y2 = point2
    dx, dy = x2-x1, y2-y1
    # se dibuja la linea a lo largo del eje-y, sino linea a lo largo del eje-x
    steep = abs(dy) > abs(dx)

    # intercambiamos las coordenadas si steep>1 (dibujamos de forma inversa) 
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    # calculamos la gradiente para el dibujo de la linea
    gradient = dy/dx

    # primera interseccion con el eje-y(steep<1 con el eje-x) para el main loop
    intery = y1 + rfpart(x1) * gradient

    # verificamos si la linea a dibujar es a lo largo del eje-y
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # calculamos y dibujamos los endpoints
    xstart = draw_endpoint(calc_point(x1, y1, steep), gradient, steep) + 1
    xend = draw_endpoint(calc_point(x2, y2, steep), gradient, steep)
    
    # si es true debemos dibujar de forma vertical (eje-y)
    if(xstart > xend):
        xstart, xend = xend, xstart
    
    # main loop, dibujamos los pixeles restantes de acuerdo a la parte fraccionaria de las coordenadas
    for x in range(xstart, xend):
        y = int(intery)
        fill_colour(calc_point(x, y, steep), rfpart(intery))
        fill_colour(calc_point(x, y+1, steep), fpart(intery))
        intery += gradient
        # solo para animacion con pygame
        if animated:
            pygame.display.update()
            time.sleep(1)

def window_simple_line(point1, point2):
    "dibuja una linea simple desde el point1 a point2 con pygame"
    global pixel_size

    print("\n\tZoom config:")
    print("\t\tzoom (+): space")
    print("\t\tzoom (-): backspace")

    while True:        
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        if (pixel_size < MAX_PIXEL_SIZE):
                            pixel_size += 1
                    if event.key == K_BACKSPACE:
                        if (pixel_size != MIN_PIXEL_SIZE):
                            pixel_size -= 1
                    reset_window()
            draw_line(point1, point2)
            pygame.display.update()

def window_draw_polygon(file):
    "dibuja un poligono con el algoritmo de wu's de acuerdo a la serie de puntos del file"
    while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        poligono(leer_puntos(archivo=file))
        pygame.display.update()

def window_animated_line():
    "dibuja una linea con animacion"
    global pixel_size
    pixel_size = 15
    
    while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.draw.aaline(DISPLAYSURF, WHITE, (5*pixel_size, 10*pixel_size), (20*pixel_size,20*pixel_size))
        draw_line((5, 10), (20, 20), True)
        reset_window()
        
if __name__ == '__main__':
    global FPSCLOCK, grid, pixel_size
    
    if (len(argv) < 1 or len(argv) > 4):
        print(f"Usage: {argv[0]} [-p | --point] <x1-y1> <x2-y2>  dibuja una linea desde el punto <x1-y1> al <x2-y2>")
        print(f"Usage: {argv[0]} [-f | --file] <path>            dibuja un poligono con los puntos del archivo <path>")
        print(f"Usage: {argv[0]} [-a | --animated]               dibuja una linea animada para la demostracion del algortimo")
        sys.exit()

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('aaline')

    color = RED
    pixel_size = 1

    if (len(argv) == 1):
        window_simple_line((10, 10), (200, 300))
        sys.exit()

    if '-p' in argv or '--point' in argv:
        if len(argv) == 4:
            point1 = tuple(map(int, argv[2].split('-')))
            point2 = tuple(map(int, argv[3].split('-')))
            window_simple_line(point1, (point2))
        else:
            print(f"Usage: {argv[0]} [-p | --point] <x1-y1> <x2-y2>")
    elif '-f' in argv or '--file' in argv:
        if len(argv) == 3:
           window_draw_polygon(argv[2])
        else:
            print(f"Usage: {argv[0]} [-f | --file] <path>")
    elif '-a' in argv or '--animated' in argv:
        if len(argv) == 2:
            window_animated_line()
        else:
            print(f"Usage: {argv[0]} [-a | --animated]")
    else:
        print(f"Usage: {argv[0]} [-p | --point] <x1-y1> <x2-y2>  dibuja una linea desde el punto <x1-y1> al <x2-y2>")
        print(f"Usage: {argv[0]} [-f | --file] <path>            dibuja un poligono con los puntos del archivo <path>")
        print(f"Usage: {argv[0]} [-a | --animated]               dibuja una linea animada para la demostracion del algortimo")

