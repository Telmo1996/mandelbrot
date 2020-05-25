import math

def Colorear(iter, maxIter, desfase=0, shift=0, mode='verdeNegro'):
    if mode == 'azulBlanco':
        if iter == maxIter:
            return 255, 255, 255
        else:
            magia = (iter + shift) % 255
            return 255 - magia, 255 - magia, 255

    elif mode == 'verdeNegro':
        if iter == maxIter:
            return 0, 0, 0
        else:
            magia = (iter + shift) % 255
            return 0, magia, 0

    elif mode == 'azulVerde':
        if iter == maxIter:
            return 0, 0, 0
        else:
            magia = (iter + shift) % 255
            return int(20+magia*0.2), 255 - magia, int(magia * 0.8)

    elif mode == 'chocolate':
        if iter == maxIter:
            return 217, 167, 139
        else:
            magia = (iter + shift) % 255
            magiaRad = magia * math.pi * 2 / 255    # [0, 2pi]
            r = 150 + (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 3
            g = 100 + (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 3
            b = 80 + (math.sin(magiaRad + math.pi * 1/16 + desfase) + 1) / 2 * 255 / 3
            return r, g, b

    elif mode == 'rainbow':
        if iter == maxIter:
            return 0, 0, 0
        else:
            magia = iter / maxIter
            magiaRad = magia * math.pi * 2
            r = (math.sin(magiaRad + desfase) + 1) / 2 * 255
            g = (math.sin(magiaRad + desfase * math.pi) + 1) / 2 * 255
            b = (math.sin(magiaRad + desfase * (math.pi / 2)) + 1) / 2 * 255
            return r, g, b

    elif mode == 'camelia':
        if iter == maxIter:
            return 255, 255, 255
        else:
            magia = (iter + shift) % 255
            magiaRad = magia * math.pi * 2 / 255  # [0, 2pi]
            r = 180 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 5
            g = (math.sin(magiaRad + desfase) + 1) / 2 * 255 / 1.3
            b = 150 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 3
            return r, g, b

    elif mode == 'bnw_stripes':
        if iter % 2 == 0:
            return 255, 255, 255
        else:
            return 0, 0, 0

    elif mode == 'night':
        if iter == maxIter:
            return 0, 0, 0
        else:
            modulo = 300
            magia = (iter + shift) % modulo
            magiaRad = magia * math.pi * 2 / modulo  # [0, 2pi]
            temp = (math.sin(magiaRad + desfase) + 1)
            rg = 0 + ((temp*temp) / 4 * 255) / 1.2
            b = 30 + ((math.sin(magiaRad + desfase) + 1) / 2 * 255) / 1.2
            return rg, rg, b

    else:
        return 0, 0, 0
