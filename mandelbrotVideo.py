from mandelbrotCommon import *
import pygame
import json
import math
import cv2
import os
from os.path import isfile, join
import errno


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

# azulBlanco verdeNegro azulVerde
# chocolate rainbow camelia
colorMode = 'rainbow'

initialOffset = math.pi
offsetIncrement = math.pi / (64*16)

shift = 0

scaleFactor = 1/4

fps = 24
numFrames = 60*20

generarSoloVideo = True    # No volver a generar las imagenes

# Read from
loadDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\Json'
fileName = 'Caracolas4k.json'

# Write to
videoName = 'Caracolas4k_inRainbowsV2_longV2'  # Sin extension
saveDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\Videos\\'

#################################################################

try:
    os.mkdir(saveDirectory + '\\' + videoName)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

if scaleFactor > 1:
    scaleFactor = 1

loadFile = loadDirectory + '\\' + fileName

# Cargar el JSON
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
if not generarSoloVideo:
    pygame.init()
    screen = pygame.display.set_mode((scaledWidth, scaledHeight))
    bg = 50, 25, 25
    screen.fill(bg)
    pygame.display.flip()

# Calcular pixeles escalados
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

print()

# Main
esperando = not generarSoloVideo
i = 0
while esperando:
    i += 1
    pintarSet()
    initialOffset += offsetIncrement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esperando = False
        if event.type == pygame.KEYDOWN:
            pulsados = pygame.key.get_pressed()
            if pulsados[pygame.K_SPACE]:
                esperando = False
    saveFile = saveDirectory + '\\' + videoName + '\\{:06d}'.format(i) + '.png'
    pygame.image.save(screen, saveFile)
    if i == numFrames:
        esperando = False
    print("Llevamos {0}/{1} frames".format(i, numFrames))


# Crear el video
pathIn = saveDirectory + '\\' + videoName + '\\'
pathOut = saveDirectory + '\\' + videoName + '.avi'
# fps = 30
frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
for i in range(len(files)):
    filename = pathIn + files[i]
    # reading each files
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)

    # inserting the frames into an image array
    frame_array.append(img)
out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()
