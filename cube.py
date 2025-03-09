import math
import time
import os
import itertools

PAUSE_AMOUNT = 0.1
WIDTH, HEIGHT = 80, 24
SCALEX = (WIDTH - 4) // 8
SCALEY = (HEIGHT - 4) // 8 * 2
TRANSLATEX = (WIDTH - 4) // 2
TRANSLATEY = (HEIGHT - 4) // 2
LETTERS = ['X', 'A', 'Y', 'B', '5', '6'] 
X_ROTATE_SPEED = 0.03
Y_ROTATE_SPEED = 0.08
Z_ROTATE_SPEED = 0.13

CUBE_CORNERS = [
    [-1, -1, -1], [1, -1, -1], [-1, -1, 1], [1, -1, 1],
    [-1, 1, -1], [1, 1, -1], [-1, 1, 1], [1, 1, 1]]

def line(x1, y1, x2, y2):
    points = []
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx, sy = 1 if x1 < x2 else -1, 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points

def rotatePoint(x, y, z, ax, ay, az):
    x, y, z = (
        x,
        (y * math.cos(ax)) - (z * math.sin(ax)),
        (y * math.sin(ax)) + (z * math.cos(ax)))
    x, y, z = (
        (z * math.sin(ay)) + (x * math.cos(ay)),
        y,
        (z * math.cos(ay)) - (x * math.sin(ay)))
    x, y, z = (
        (x * math.cos(az)) - (y * math.sin(az)),
        (x * math.sin(az)) + (y * math.cos(az)), z)
    return x, y, z

def adjustPoint(point):
    return (
        int(point[0] * SCALEX + TRANSLATEX),
        int(point[1] * SCALEY + TRANSLATEY))

def main():
    xRotation = yRotation = zRotation = 0.0
    letter_cycle = itertools.cycle(LETTERS) 
    
    while True:
        xRotation += X_ROTATE_SPEED
        yRotation += Y_ROTATE_SPEED
        zRotation += Z_ROTATE_SPEED

        rotatedCorners = [
            rotatePoint(x, y, z, xRotation, yRotation, zRotation)
            for x, y, z in CUBE_CORNERS]
        
        cubePoints = []
        for fromCornerIndex, toCornerIndex in [
            (0, 1), (1, 3), (3, 2), (2, 0),
            (0, 4), (1, 5), (2, 6), (3, 7),
            (4, 5), (5, 7), (7, 6), (6, 4)]:
            
            fromX, fromY = adjustPoint(rotatedCorners[fromCornerIndex])
            toX, toY = adjustPoint(rotatedCorners[toCornerIndex])
            cubePoints.extend(line(fromX, fromY, toX, toY))

        cubePoints = set(cubePoints)

        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) in cubePoints:
                    print(next(letter_cycle), end='') 
                else:
                    print(' ', end='')
            print()

        time.sleep(PAUSE_AMOUNT)

if __name__ == "__main__":
    main()
