import time
import cmath
import json
from multiprocessing import Pool


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


def iterMandelbrot(listaCoord, maxIterations):
    iters = []
    # Traducir el pixel en la pantalla al punto correspondiente

    for punto in listaCoord:
        z0 = complex(0, 0)
        c = complex(punto[0], punto[1])

        iteration = 0

        while abs(z0) <= 2 and iteration < maxIterations:
            z1 = z0 * z0 + c
            z0 = z1
            iteration += 1

        iters.append(iteration)

    return iters


if __name__ == '__main__':

    ##############################################################
    # ################### Configuraciones ###################### #
    ##############################################################

    multiplicador = 4
    width, height = int(360 * multiplicador), int(640 * multiplicador)

    puntoCentral = -0.7746806106269039, -0.1374168856037867
    zoom = 1.506043553756164E-12

    maxIterations = 3000

    numProcesadores = 8

    fileName = 'Isla_m4k'

    #################################################################

    saveDirectoryMatrices = 'C:\\Users\\tferc\\Desktop\\Mandelbrot\\MatricesIterMulti'

    #################################################################

    saveFileMatrices = saveDirectoryMatrices + '\\' + fileName + '.json'

    star_time = time.time()

    mandelbrotList = [0] * width
    for j in range(0, width):
        mandelbrotList[j] = [0] * height

    # Calcular Mandelbrot
    xyRatio = width/height
    xScope = puntoCentral[0]-zoom*xyRatio, puntoCentral[0]+zoom*xyRatio
    yScope = puntoCentral[1]-zoom, puntoCentral[1]+zoom

    # Crear la lista de filas
    filas = []
    for Px in range(0, width):
        # print("Vamos por el {0}%".format(100*Px/width))

        fila = []

        for Py in range(0, height):
            # Traducir el pixel en la pantalla al punto correspondiente
            x0 = (xScope[1] - xScope[0]) * (Px / width) + xScope[0]
            y0 = (yScope[1] - yScope[0]) * ((height - Py) / height) + yScope[0]

            fila.append((x0, y0))

        filas.append((fila, maxIterations))

    pool = Pool(numProcesadores)
    result = pool.starmap(iterMandelbrot, filas, 1)

    pool.close()
    pool.join()

    end_time = time.time() - star_time

    print("Hecho! Ha tardado " + str(end_time / 60) + ' min')

    # Guardar la matriz de iteraciones a disco
    mandelbrotJson = {"info": {"tamano": {"x": width, "y": height}, "maxIter":  maxIterations, "puntoCentral": {"x": puntoCentral[0], "y": puntoCentral[1]}, "zoom": zoom}, "data": result}
    with open(saveFileMatrices, 'w') as outfile:
        json.dump(mandelbrotJson, outfile)
        print("Matriz guardada en: " + saveFileMatrices)
