from multiprocessing import Pool


def EnCardioide(x, y):
    p = complex(x, y)
    i = complex(0, 1)
    phi = cmath.phase(p)
    c = cmath.exp(i * phi) / 2 - cmath.exp(2 * i * phi) / 4
    return abs(p) < abs(c)


def EnCirculo(x, y):
    # 1/16 = 0.0625
    y2 = 0.0625 - (x + 1) * (x + 1)
    return y2 > 0 and (y2 > y > (-y2))


def Colorear(curIter, maxIter, mode='default'):
    if mode == 'azulBlanco':
        magia = curIter % 255
        return 255 - magia, 255 - magia, 255
    elif mode == 'verdeNegro':
        magia = curIter % 255
        return 0, magia, 0
    elif mode == 'azulVerde':
        magia = curIter % 255
        return int(20 + magia * 0.2), 255 - magia, int(magia * 0.8)
    elif mode == 'byn':
        if curIter == maxIter:
            return 255, 0, 0
        else:
            magia = curIter % 255
            return magia, magia, magia
    else:  # default
        magia = curIter % 255
        return 255 - magia, 255 - magia, 255


def iterMandelbrot(coord, maxIterations):
    z0 = complex(0, 0)
    c = complex(coord[0], coord[1])

    iteration = 0

    while abs(z0) <= 2 and iteration < maxIterations:
        z1 = z0 * z0 + c
        z0 = z1
        iteration += 1

    return iteration


if __name__ == '__main__':
    import pygame
    import cmath

    ##############################################################
    # ################### Configuraciones ###################### #
    ##############################################################

    colorMandelbrot = 255, 0, 0
    colorMode = 'byn'

    multiplicadorFake = 4

    multiplicador = 1 / 4
    # width, height = int(1536 * multiplicador), int(864 * multiplicador)       # portatil
    width, height = int(360 * multiplicador), int(640 * multiplicador)      # movil

    puntoCentral = -0.749964095004616, 0.009633765472374324
    zoom = 6.275581773916279e-05

    maxIterations = 100000

    zoomGrande = 2
    zoomPeque = 1.1

    multiproc = False

    #################################################################

    zoomMulti = zoomGrande

    # Iniciar la pantalla
    print("Tamaño: {0}x{1}".format(width, height))
    pygame.init()
    screen = pygame.display.set_mode((width * multiplicadorFake, height * multiplicadorFake))
    bg = 50, 25, 25
    screen.fill(bg)
    pygame.display.set_caption('Mandelbrot Explorer')

    recalcular = True
    cortar = False
    while recalcular:

        # Calcular Mandelbrot
        xyRatio = width / height
        xScope = puntoCentral[0] - zoom * xyRatio, puntoCentral[0] + zoom * xyRatio
        yScope = puntoCentral[1] - zoom, puntoCentral[1] + zoom

        cortar = False
        for Px in range(0, width):
            fila = []
            for Py in range(0, height):

                if not (cortar or (not recalcular)):
                    # Traducir el pixel en la pantalla al punto correspondiente
                    x0 = (xScope[1] - xScope[0]) * (Px / width) + xScope[0]
                    y0 = (yScope[1] - yScope[0]) * (Py / height) + yScope[0]

                    if multiproc:
                        fila.append(((x0, y0), maxIterations))
                    else:
                        z0 = complex(0, 0)
                        c = complex(x0, y0)

                        iteration = 0
                        if (not EnCardioide(x0, y0)) and (not EnCirculo(x0, y0)):
                            while abs(z0) <= 2 and iteration < maxIterations:
                                z1 = z0 * z0 + c
                                z0 = z1
                                iteration += 1

                            if iteration == maxIterations:
                                color = colorMandelbrot
                            else:
                                color = Colorear(iteration, maxIterations, colorMode)

                        else:
                            color = colorMandelbrot
                            iteration = maxIterations

                        pygame.draw.rect(screen, color,
                                         pygame.Rect(Px * multiplicadorFake, (height - Py) * multiplicadorFake,
                                                     multiplicadorFake, multiplicadorFake))

            if not (cortar or (not recalcular)):
                # Linea verde
                pygame.draw.line(screen, (0, 255, 0), ((Px + 1) * multiplicadorFake, 0),
                                 ((Px + 1) * multiplicadorFake, height * multiplicadorFake))

                if multiproc:
                    pool = Pool(8)
                    result = pool.starmap(iterMandelbrot, fila, 1)
                    pool.close()
                    pool.join()

                    py = 1
                    for p in result:
                        pygame.draw.rect(screen, Colorear(p, maxIterations, colorMode),
                                         pygame.Rect(Px * multiplicadorFake, (height - py) * multiplicadorFake,
                                                     multiplicadorFake, multiplicadorFake))
                        py += 1

            pygame.display.flip()

            # Control con las teclas
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    recalcular = False
                    cortar = True
                if event.type == pygame.KEYDOWN:
                    pulsados = pygame.key.get_pressed()

                    if pulsados[pygame.K_SPACE]:
                        cortar = True
                        recalcular = False

                    if pulsados[pygame.K_c]:  # Pintar Cruz central
                        pygame.draw.line(screen, (0, 255, 0),
                                         (width * multiplicadorFake / 2 + 10, height * multiplicadorFake / 2),
                                         (width * multiplicadorFake / 2 - 10, height * multiplicadorFake / 2), 1)
                        pygame.draw.line(screen, (0, 255, 0),
                                         (width * multiplicadorFake / 2, height * multiplicadorFake / 2 + 10),
                                         (width * multiplicadorFake / 2, height * multiplicadorFake / 2 - 10), 1)
                        pygame.display.flip()

                    if pulsados[pygame.K_RIGHT] or pulsados[pygame.K_d]:
                        cortar = True
                        zoom /= zoomMulti
                        print()
                        print("Zoom: {0}".format(zoom))
                    if pulsados[pygame.K_LEFT] or pulsados[pygame.K_a]:
                        cortar = True
                        zoom *= zoomMulti
                        print()
                        print("Zoom: {0}".format(zoom))

                    if pulsados[pygame.K_UP] or pulsados[pygame.K_w]:
                        maxIterations += 100
                        print()
                        print("MaxIterations: {0}".format(maxIterations))
                    if pulsados[pygame.K_DOWN] or pulsados[pygame.K_s]:
                        maxIterations -= 100
                        if maxIterations <= 1:
                            maxIterations = 100
                        print()
                        print("MaxIterations: {0}".format(maxIterations))

                    if pulsados[pygame.K_m]:
                        multiproc = not multiproc
                        if multiproc:
                            print("Utilizando multiproccesing")
                        else:
                            print("Utilizando un solo core :(")

                    if pulsados[pygame.K_z]:
                        if zoomMulti == zoomGrande:
                            zoomMulti = zoomPeque
                            print("Zoom peque: {0}".format(zoomMulti))
                        else:
                            zoomMulti = zoomGrande
                            print("Zoom grande: {0}".format(zoomMulti))

                mouseClick = pygame.mouse.get_pressed()
                if sum(mouseClick) > 0:
                    cortar = True
                    posX, posY = pygame.mouse.get_pos()
                    posX /= multiplicadorFake
                    posY /= multiplicadorFake
                    hx = posX - width / 2
                    hy = - (posY - height / 2)
                    x = puntoCentral[0] + xyRatio * (zoom * hx / (width / 2))
                    y = puntoCentral[1] + (zoom * hy / (height / 2))
                    puntoCentral = x, y
                    print()
                    print("x, y: {0}, {1}".format(x, y))

    print()
    print("Posición final:")
    print("puntoCentral = {0}, {1}".format(puntoCentral[0], puntoCentral[1]))
    print("zoom = {0}".format(zoom))
    print()
    print("maxIterations = {0}".format(maxIterations))
