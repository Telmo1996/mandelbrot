import pygame
import time
import cmath
import numpy as np
import json


def EnCardioide(x, y):
    p = complex(x, y)
    i = complex(0, 1)
    phi = cmath.phase(p)
    c = cmath.exp(i*phi)/2-cmath.exp(2*i*phi)/4
    return abs(p) < abs(c)


def EnCirculo(x, y):
    # 1/16 = 0.0625
    y2 = 0.0625 - (x + 1) * (x + 1)
    return y2 > 0 and (y2 > y > (-y2))


def Colorear(iter, maxIter, mode='default'):
    if mode == 'azulBlanco':
        magia = iter % 255
        return 255 - magia, 255 - magia, 255
    elif mode == 'verdeNegro':
        magia = iter % 255
        return 0, magia, 0
    elif mode == 'azulVerde':
        magia = iter % 255
        return int(20+magia*0.2), 255 - magia, int(magia * 0.8)
    elif mode == 'byn':
        magia = iter % 255
        return magia, magia, magia
    else:   # default
        magia = iter % 255
        return 255 - magia, 255 - magia, 255


##############################################################
# ################### Configuraciones ###################### #
##############################################################

enableInteractive = False

enableView = False
colorMandelbrot = 255, 0, 0
colorMode = 'byn'

multiplicador = 1
width, height = int(1536*multiplicador), int(864*multiplicador)

# Full
puntoCentral = -0.75, 0.0
zoom = 1.3

maxIterations = 1000

zoomMulti = 2

enableSave = False
fileName = 'testSingle'
imageExtension = '.png'

#################################################################

saveDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\imagenes'
saveDirectoryMatrices = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\MatricesIter'

#################################################################

mandelbrotList = [0] * width
for i in range(0, width):
    mandelbrotList[i] = [0] * height

saveFile = saveDirectory + '\\' + fileName + imageExtension
saveFileMatrices = saveDirectoryMatrices + '\\' + fileName + '.json'

# Iniciar la pantalla
print("Tamaño: {0}x{1}".format(width, height))
if enableView or enableInteractive:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    bg = 50, 25, 25
    screen.fill(bg)
    pygame.display.set_caption('Mandelbrot')

recalcular = True
while recalcular:
    recalcular = enableInteractive      # Si enableInteractive == False no recalcula

    # Calcular Mandelbrot
    xyRatio = width/height
    xScope = puntoCentral[0]-zoom*xyRatio, puntoCentral[0]+zoom*xyRatio
    yScope = puntoCentral[1]-zoom, puntoCentral[1]+zoom

    star_time = time.time()

    for Px in range(0, width):
        if not enableInteractive:
            print("Vamos por el {0}%".format(100*Px/width))
        if enableView or enableInteractive:
            pygame.display.flip()
        for Py in range(0, height):
            # Traducir el pixel en la pantalla al punto correspondiente
            x0 = (xScope[1] - xScope[0]) * (Px / width) + xScope[0]
            y0 = (yScope[1] - yScope[0]) * (Py / height) + yScope[0]

            z0 = complex(0, 0)
            c = complex(x0, y0)

            iteration = 0
            if (not EnCardioide(x0, y0)) and (not EnCirculo(x0, y0)):
                while abs(z0) <= 2 and iteration < maxIterations:
                    z1 = z0 * z0 + c
                    z0 = z1
                    iteration += 1

                if enableView or enableInteractive:
                    if iteration == maxIterations:
                        color = colorMandelbrot
                    else:
                        color = Colorear(iteration, maxIterations, colorMode)
                else:
                    color = 0, 0, 0
            else:
                color = colorMandelbrot
                iteration = maxIterations

            if enableView or enableInteractive:
                screen.set_at((Px, height-Py), color)
            mandelbrotList[Px][height-Py-1] = int(iteration)

    end_time = time.time() - star_time

    if not enableInteractive:
        print("Vamos por el 100.0%")
    print("Hecho! Ha tardado " + str(end_time) + ' s')

    # Guardar la matriz de iteraciones a disco
    if enableSave:
        mandelbrotJson = {"info": {"tamano": {"x": width, "y": height}, "maxIter":  maxIterations, "puntoCentral": {"x": puntoCentral[0], "y": puntoCentral[1]}, "zoom": zoom}, "data": mandelbrotList}
        with open(saveFileMatrices, 'w') as outfile:
            json.dump(mandelbrotJson, outfile)
            print("Matriz guardada en: " + saveFileMatrices)

    if enableView or enableInteractive:
        # Mostrar el resultado por pantalla y guardarlo
        pygame.display.flip()
        if enableSave:
            pygame.image.save(screen, saveFile)
            print("Imagen guardada en: " + saveFile)

        # Esperar al SPACE para salir
        esperando = True
        while esperando:
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    recalcular = False
                if event.type == pygame.KEYDOWN:
                    pulsados = pygame.key.get_pressed()
                    if pulsados[pygame.K_SPACE]:
                        esperando = False
                        recalcular = False
                    if pulsados[pygame.K_c]:    # Pintar Cruz central
                        pygame.draw.line(screen, (0, 255, 0), (width/2+10, height/2), (width/2-10, height/2), 1)
                        pygame.draw.line(screen, (0, 255, 0), (width/2, height/2+10), (width/2, height/2-10), 1)
                        pygame.display.flip()
                    if pulsados[pygame.K_RIGHT]:
                        esperando = False
                        zoom /= zoomMulti
                        print()
                        print("Zoom: {0}".format(zoom))
                    if pulsados[pygame.K_LEFT]:
                        esperando = False
                        zoom *= zoomMulti
                        print()
                        print("Zoom: {0}".format(zoom))
                mouseClick = pygame.mouse.get_pressed()
                if sum(mouseClick) > 0:
                    esperando = False
                    posX, posY = pygame.mouse.get_pos()
                    hx = posX - width/2
                    hy = - (posY - height/2)
                    x = puntoCentral[0] + xyRatio * (zoom * hx/(width/2))
                    y = puntoCentral[1] + (zoom * hy/(height/2))
                    puntoCentral = x, y
                    print()
                    print("hx, hy: {0}, {1}".format(hx, hy))
                    print("x, y: {0}, {1}".format(x, y))

if enableInteractive:
    print()
    print("Posición final")
    print("puntoCentral = {0}, {1}".format(puntoCentral[0], puntoCentral[1]))
    print("zoom = {0}".format(zoom))
