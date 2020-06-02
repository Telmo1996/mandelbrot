import json
import pygame


def Pintar():
    # Pintar

    # Zonas claras
    pygame.draw.rect(screen, (100, 80, 80), ((0, 0), (posFirstNonZero, height)))
    pygame.draw.rect(screen, (100, 80, 80), ((posLastNonZero, 0), (width, height)))

    # Lineas 10%
    for i in range(1, 10):
        pos10V = width / 10 * i
        pos10H = height / 10 * i
        if i == 5:
            colorLin = 100, 50, 50
        else:
            colorLin = 50, 50, 50
        pygame.draw.line(screen, colorLin, (pos10V, 0), (pos10V, height))  # Verticales
        pygame.draw.line(screen, colorLin, (0, pos10H), (width, pos10H))  # Horizontales

    # Curva azul
    pygame.draw.lines(screen, (0, 0, 255), False, puntos, 1)

    pygame.display.flip()


##############################################################
# ################### Configuraciones ###################### #
##############################################################

height, width = 700, 1200

significantPixels = 0      # Number of pixels to ignore in determining the band

fileName = 'Caracolas4k'      # Sin .json

loadDirectory = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\Json'

##############################################################

loadFile = loadDirectory + '\\' + fileName + '.json'

with open(loadFile) as json_file:
    json = json.load(json_file)

tamanoX = json["info"]["tamano"]["x"]
tamanoY = json["info"]["tamano"]["y"]
maxIter = json["info"]["maxIter"]

# TODO REWORK TIME
arrayIter = [0] * width

trueMaxIter = 1
for x in range(0, tamanoX):
    for y in range(0, tamanoY):
        curIter = json["data"][x][y]
        if curIter > trueMaxIter and curIter != maxIter:
            trueMaxIter = curIter
        arrayIter[int(curIter/maxIter*width) - 1] += 1

print()
print("Nombre: {0}".format(fileName))
print("Tamaño: {0} x {1}".format(tamanoX, tamanoY))
print("maxIter: {0}, trueMaxIter: {1}".format(maxIter, trueMaxIter))
print("Punto central: {0}, {1}".format(json["info"]["puntoCentral"]["x"], json["info"]["puntoCentral"]["y"]))
print("Zoom: {0}".format(json["info"]["zoom"]))
print()


# Iniciar la pantalla
pygame.init()
screen = pygame.display.set_mode((width, height))
bg = 50, 25, 25
screen.fill(bg)
pygame.display.flip()
pygame.display.set_caption('Json Analyser: {0}'.format(fileName))

puntos = []     # TODO REWORK TIME
posHighestIter = 0
posFirstNonZero = 0
posLastNonZero = width - 2
onlyZerosFirst = True
onlyZerosLast = True
for i in range(0, width):
    if arrayIter[i] > arrayIter[posHighestIter]:
        posHighestIter = i

    if arrayIter[i] <= significantPixels and onlyZerosFirst:
        posFirstNonZero = i + 1
    elif arrayIter[i] > significantPixels:
        onlyZerosFirst = False

for i in range(width - 2, 0, -1):
    if arrayIter[i] <= significantPixels and onlyZerosLast:
        posLastNonZero = i + 1
    elif arrayIter[i] > significantPixels:
        onlyZerosLast = False

# print(posFirstNonZero, posLastNonZero, arrayIter[posLastNonZero])

for i in range(0, width):
    puntos.append((i, height - (height * arrayIter[i] / arrayIter[posHighestIter]) - 1))


Pintar()


# print(arrayIter)

# Esperar al SPACE para salir
esperando = True
while esperando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esperando = False
        if event.type == pygame.KEYDOWN:
            pulsados = pygame.key.get_pressed()

            if pulsados[pygame.K_SPACE]:
                esperando = False
