import pygame
from mandelbrotCommon import Colorear
import math
import time


def pintar():
    screen.fill(bg)
    puntosB = []
    puntosG = []
    puntosR = []
    for i in range(0, width):
        color = Colorear(i, maxIterations, initialOffset, shift, colorMode)
        pygame.draw.line(screen, color, (i, 0), (i, height/2), 1)

        puntosB.append((i, (height / 2 + height / 2 * (1 - color[2] / 255))-1))
        puntosG.append((i, (height / 2 + height / 2 * (1 - color[1] / 255))-1))
        puntosR.append((i, (height / 2 + height / 2 * (1 - color[0] / 255))-1))

    pygame.draw.lines(screen, (0, 0, 255), False, puntosB, 2)
    pygame.draw.lines(screen, (0, 255, 0), False, puntosG, 2)
    pygame.draw.lines(screen, (255, 0, 0), False, puntosR, 2)

    texto = font.render('Offset: {:05.2f}'.format(initialOffset), True, (0, 0, 0), (255, 255, 255))
    screen.blit(texto, textRect)
    pygame.display.update()


##############################################################
# ################### Configuraciones ###################### #
##############################################################

# azulBlanco 0  verdeNegro 1  azulVerde 2
# chocolate 3  rainbow 4  camelia 5  bnw_stripes 6  night 7
# nightCrawler 8
colorModeNames = [
    'azulBlanco', 'verdeNegro', 'azulVerde', 'chocolate', 'rainbow', 'camelia', 'bnw_stripes', 'night', 'nightCrawler'
]
colorModeNumber = 4
colorMode = colorModeNames[colorModeNumber]

width, height = 255*3, 300
maxIterations = width - 1
initialOffset = math.pi * 0
shift = 0

offsetIncrement = math.pi/64

animar = False

##############################################################

pygame.init()

screen = pygame.display.set_mode((width, height))
# screen = pygame.display.set_mode((width, height))
bg = 50, 25, 25
screen.fill(bg)
pygame.display.set_caption('Color Viewer')

# Texto
font = pygame.font.Font('freesansbold.ttf', 14)
text = font.render('Offset: {0}'.format(initialOffset), True, (0, 0, 0), (255, 255, 255))
textRect = text.get_rect()
textRect.center = (width/2, height/2 - 10)
screen.blit(text, textRect)

pygame.display.update()

pintar()

# Esperar al SPACE para salir
esperando = True
while esperando:
    if animar:
        initialOffset += offsetIncrement
        pintar()
    time.sleep(0.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esperando = False
        if event.type == pygame.KEYDOWN:
            pulsados = pygame.key.get_pressed()
            if pulsados[pygame.K_SPACE]:
                esperando = False
            if pulsados[pygame.K_a]:
                animar = not animar
            if pulsados[pygame.K_RIGHT]:
                initialOffset += offsetIncrement
                animar = False
                pintar()
            if pulsados[pygame.K_LEFT]:
                initialOffset -= offsetIncrement
                animar = False
                pintar()
            if pulsados[pygame.K_w]:
                colorModeNumber += 1
                if colorModeNumber >= len(colorModeNames):
                    colorModeNumber = 0
                colorMode = colorModeNames[colorModeNumber]
                pintar()
                print("Color Mode: {0}".format(colorMode))
            if pulsados[pygame.K_s]:
                colorModeNumber -= 1
                if colorModeNumber < 0:
                    colorModeNumber = len(colorModeNames) - 1
                colorMode = colorModeNames[colorModeNumber]
                pintar()
                print("Color Mode: {0}".format(colorMode))

print()
print("Offset: {0}".format(initialOffset))
print("Shift: {0}".format(shift))
