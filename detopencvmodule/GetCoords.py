def getcoords():
    x1 = 401
    y1 = 52
    width = 32
    height = 18
    xstep = (width - 2)/3
    xb = [0,0,0]
    xe = [0,0,0]
    for idx in range(3):
        xb[idx] = int(x1 + idx + idx*xstep)
        xe[idx] = int(x1 + idx + (idx + 1)*xstep)
    return y1, y1 + height, xb[0], xe[0], xb[1], xe[1], xb[2], xe[2]


