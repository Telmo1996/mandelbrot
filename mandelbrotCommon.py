import math

def Colorear(iter, maxIter, desfase=0, shift=0, mode='verdeNegro'):

    r, g, b = 0, 0, 0

    if mode == 'azulBlanco':
        if iter == maxIter:
            r, g, b = 255, 255, 255
        else:
            magia = (iter + shift) % 255
            r, g, b = 255 - magia, 255 - magia, 255

    elif mode == 'verdeNegro':
        if iter == maxIter:
            r, g, b = 0, 0, 0
        else:
            magia = (iter + shift) % 255
            r, g, b = 0, magia, 0

    elif mode == 'azulVerde':
        if iter == maxIter:
            r, g, b = 0, 0, 0
        else:
            magia = (iter + shift) % 255
            r, g, b = int(20+magia*0.2), 255 - magia, int(magia * 0.8)

    elif mode == 'chocolate':
        if iter == maxIter:
            r, g, b = 217, 167, 139
        else:
            magia = (iter + shift) % 255
            magiaRad = magia * math.pi * 2 / 255    # [0, 2pi]
            r = 150 + (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 3
            g = 100 + (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 3
            b = 80 + (math.sin(magiaRad + math.pi * 1/16 + desfase) + 1) / 2 * 255 / 3

    elif mode == 'rainbow':
        if iter == maxIter:
            r, g, b = 0, 0, 0
        else:
            magia = iter / maxIter
            magiaRad = magia * math.pi * 2
            r = (math.sin(magiaRad + desfase) + 1) / 2 * 255
            g = (math.sin(magiaRad + desfase * math.pi) + 1) / 2 * 255
            b = (math.sin(magiaRad + desfase * (math.pi / 2)) + 1) / 2 * 255

    elif mode == 'camelia':
        if iter == maxIter:
            r, g, b = 255, 255, 255
        else:
            magia = (iter + shift) % 255
            magiaRad = magia * math.pi * 2 / 255  # [0, 2pi]
            r = 180 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 5
            g = (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 1.3
            b = 150 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 3

    elif mode == 'bnw_stripes':
        if iter % 2 == 0:
            r, g, b = 255, 255, 255
        else:
            r, g, b = 0, 0, 0

    elif mode == 'night':
        if iter == maxIter:
            r, g, b = 0, 0, 0
        else:
            modulo = 300
            magia = (iter + shift) % modulo
            magiaRad = magia * math.pi * 2 / modulo  # [0, 2pi]
            temp = (math.sin(magiaRad + desfase) + 1)
            rg = 0 + ((temp*temp) / 4 * 255) / 1.2
            b = 30 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 1.2
            r = rg
            g = rg

    elif mode == 'nightCrawler':
        if iter == maxIter:
            r, g, b = 0, 0, 0
        else:
            modulo = 255*3/2
            magia = (iter + shift) % modulo
            magiaRad = magia * math.pi * 2 / modulo  # [0, 2pi]
            temp = (math.cos(magiaRad + desfase) + 1)
            tempR = (math.cos(magiaRad + desfase + math.pi) + 1)
            drop = (temp/2)**8 * 255
            r = 255 - ((tempR**2) / 4 * 255)
            g = 0 + ((temp**2) / 4 * 255) / 1.2 - drop/1.2
            b = 30 + (temp / 2 * 255) / 1 - drop*1.12

    if r < 0:
        r = 0
    if r > 255:
        r = 255
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    if b < 0:
        b = 0
    if b > 255:
        b = 255

    return r, g, b
