from mandelbrotCommon import *
import pygame
import json
import math
import os


def pintarSet():
    for Px in range(0, scaledWidth):
        # pygame.display.flip()
        for Py in range(0, scaledHeight):
            scaledPx = pixelsX[Px]
            scaledPy = pixelsY[Py]
            iterations = mandelbrotJson["data"][scaledPx][scaledPy]

            color = Colorear(iterations, maxIterations, initialOffset, shift, colorMode)
            screen.set_at((Px, Py), color)
    pygame.display.flip()


##############################################################
# ################### Configuraciones ###################### #
##############################################################

# azulBlanco 0  verdeNegro 1  azulVerde 2
# chocolate 3  rainbow 4  camelia 5  bnw_stripes 6  night 7
colorModeNames = ['azulBlanco', 'verdeNegro', 'azulVerde', 'chocolate', 'rainbow', 'camelia', 'bnw_stripes', 'night']
colorModeNumber = 7
colorMode = colorModeNames[colorModeNumber]

initialOffset = 0.6381360077604268
offsetIncrement = math.pi / 64

shift = 100
shiftIncrement = 20

enableVideo = False

scaleFactor = 1

fileName = '1Json4k'      # Sin .json
saveExtension = '.png'

#################################################################

# Read from
loadDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\Json'

# Write to
saveDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\imagenesJson'
saveFileName = fileName

#################################################################


if scaleFactor > 1:
    scaleFactor = 1

loadFile = loadDirectory + '\\' + fileName + '.json'
saveFile = saveDirectory + '\\' + saveFileName + saveExtension

with open(loadFile) as json_file:
    mandelbrotJson = json.load(json_file)

maxIterations = mandelbrotJson["info"]["maxIter"]

width = mandelbrotJson["info"]["tamano"]["x"]
height = mandelbrotJson["info"]["tamano"]["y"]

scaledWidth = int(width * scaleFactor)
scaledHeight = int(height * scaleFactor)

print("Tamaño original  : {0} x {1}".format(width, height))
print("Tamaño reescalado: {0} x {1}".format(scaledWidth, scaledHeight))

# Iniciar la pantalla
pygame.init()

screen = pygame.display.set_mode((scaledWidth, scaledHeight))
# screen = pygame.display.set_mode((width, height))
bg = 50, 25, 25
screen.fill(bg)
pygame.display.flip()
pygame.display.set_caption('Mandelbrot Viewer')

pixelsX = [0] * scaledWidth
pixelsY = [0] * scaledHeight
i = 0
for pix in range(0, scaledWidth):
    pixelsX[pix] = int(i * (1/scaleFactor))
    i += 1
i = 0
for pix in range(0, scaledHeight):
    pixelsY[pix] = int(i * (1/scaleFactor))
    i += 1


pintarSet()

# Esperar al SPACE para salir
esperando = True
while esperando:
    if enableVideo:
        pintarSet()
        initialOffset += offsetIncrement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esperando = False
        if event.type == pygame.KEYDOWN:
            pulsados = pygame.key.get_pressed()

            if pulsados[pygame.K_SPACE]:
                esperando = False

            if pulsados[pygame.K_c]:    # Pintar Cruz central
                pygame.draw.line(screen, (0, 255, 0), (scaledWidth / 2 + 10, scaledHeight / 2),
                                 (scaledWidth / 2 - 10, scaledHeight / 2), 1)
                pygame.draw.line(screen, (0, 255, 0), (scaledWidth / 2, scaledHeight / 2 + 10),
                                 (scaledWidth / 2, scaledHeight / 2 - 10), 1)
                pygame.display.flip()

            if pulsados[pygame.K_s]:    # Guardar imagen
                print()
                if os.path.isfile(saveFile):
                    numFile = 1
                    while os.path.isfile(
                            "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile, saveExtension)):
                        numFile += 1
                    pygame.image.save(screen,
                                      "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile, saveExtension))
                    print("Imagen guardada en: " + "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile,
                                                                              saveExtension))
                else:
                    pygame.image.save(screen, saveFile)
                    print("Imagen guardada en: " + saveFile)
                print("Offset: {0} \nShift: {1}".format(initialOffset, shift))

            if pulsados[pygame.K_RIGHT]:
                initialOffset += offsetIncrement
                pintarSet()
                print("Offset: {0}".format(initialOffset))
            if pulsados[pygame.K_LEFT]:
                initialOffset -= offsetIncrement
                pintarSet()
                print("Offset: {0}".format(initialOffset))

            if pulsados[pygame.K_UP]:
                shift += shiftIncrement
                pintarSet()
                print("Shift: {0}".format(shift))
            if pulsados[pygame.K_DOWN]:
                shift -= shiftIncrement
                pintarSet()
                print("Shift: {0}".format(shift))

            if pulsados[pygame.K_q]:
                colorModeNumber += 1
                if colorModeNumber >= len(colorModeNames):
                    colorModeNumber = 0
                colorMode = colorModeNames[colorModeNumber]
                pintarSet()
                print("Color Mode: {0}".format(colorMode))
            if pulsados[pygame.K_a]:
                colorModeNumber -= 1
                if colorModeNumber < 0:
                    colorModeNumber = len(colorModeNames) - 1
                colorMode = colorModeNames[colorModeNumber]
                pintarSet()
                print("Color Mode: {0}".format(colorMode))
