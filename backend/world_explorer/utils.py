import os
import math
import numpy as np
C_VAL = 17
CENTRAL = (C_VAL, C_VAL)
kernel = 4
direct_angle = 56
precission = 2

from timeit import default_timer as timer

def calc_vect_angle(p1, p2, center=CENTRAL):
    ax, ay = center
    xi, yi = p1
    # vi = ax - xi, ay - yi
    vi = xi - ax, yi - ax

    xj, yj = p2
    # vj = ax - xj, ay - yj
    vj = xj - ax, yj - ay

    # print('vi vj', vi, vj)

    vij = vi[0]*vj[0] + vi[1]*vj[1]
    # print('vij', vij)

    # mod_i = round(math.sqrt(vi[0]**2 + vi[1]**2))
    # mod_j = round(math.sqrt(vj[0]**2 + vj[1]**2))
    mod_i = vi[0]**2 + vi[1]**2
    mod_j = vj[0]**2 + vj[1]**2

    # print('mod_i, mod_j', mod_i, mod_j)
    # print('math.sqrt(mod_i) * math.sqrt(mod_j)', math.sqrt(mod_i) * math.sqrt(mod_j))
    mod_ij = float(math.sqrt(mod_i) * math.sqrt(mod_j))
    if mod_ij == 0:
        return 0, mod_ij
    cosa = float(vij) / mod_ij
    # print('cosa', cosa, math.degrees(cosa))
    return cosa, mod_ij

def line_length(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

def cm_triangle(img, corners, absolute=(0,0)):
    # import numpy as np
    # import cv2
    srt = set(sorted(corners, key= lambda x: (x[1], x[0])))

    ax, ay = CENTRAL

    angle_direction = lambda angle, pos: angle / pos * direct_angle > direct_angle - precission and angle / pos * direct_angle < direct_angle + precission
    candidates = set()
    minx, _ = min(srt, key= lambda x: x[0])
    maxx, _ = max(srt, key= lambda x: x[0])
    _, miny = min(srt, key= lambda x: x[1])
    _, maxy = max(srt, key= lambda x: x[1])

    def is_border(point):
        x,y = point
        xp_min = x >= minx and x <= minx + kernel
        xp_max = x <= maxx and x >= maxx - kernel

        yp_min = y >= miny and y <= miny + kernel
        yp_max = y <= maxy and y >= maxy - kernel
        
        return (xp_min or xp_max) and (yp_min or yp_max)

    for c in srt:
        if is_border(c):
            candidates.add(c)

    # print(len(candidates))
    # print(candidates)
    _candidates = []
    for i in candidates:
        angle = -1
        for j in candidates:
            # TODO try to find triangles square define etalon trigangle and draw it.
            cosa, mod_ij = calc_vect_angle(i, j)
            angle = math.degrees(cosa)
            il = line_length(i, CENTRAL)
            jl = line_length(j, CENTRAL)
            ijl = line_length(i, j)
            p = il + jl + ijl

            # print('cosa, s', int(math.degrees(cosa)), i, j, p, ijl)

            # if p > 45 and ijl > 19:
            if il > 15 and jl > 15 and abs(il -jl) < 4 and p > 45:
                # print('sides', il, jl)
                _candidates.append((i, j, p, ijl))
                break
    
    # print(len(candidates), len(_candidates))
    _candidates = sorted(_candidates, key = lambda x: x[2] + x[3], reverse=True)
    slicer = len(_candidates)
    _candidates = [_candidates[0] if slicer else []]

    # print(_candidates)
    try:
        return _candidates[0], img
    except:
        return [(0, 0), (0, 0), 0 , 0], img
    # for i in _candidates:
    #     if not len(i):
    #         continue
    #     p1, p2, _, _ = i
    #     # dx, dy = absolute
    #     cv2.line(img, p1, p2, (255, 100, 10), 1)
    #     cv2.line(img, CENTRAL, p1, (255, 100, 10), 1)
    #     cv2.line(img, CENTRAL, p2, (255, 100, 10), 1)

        # cv2.circle(img, p1, 1, (0, 255, 0), 1)
        # cv2.circle(img, p2, 1, (0, 255, 0), 1)
    # for j in candidates:
    #     # print(j)
    #     cv2.circle(img, j, 1, (0, 255, 0), 1)

    # cv2.circle(img, CENTRAL, 2, (0, 0, 255), 1)  
    # cv2.rectangle(img, (0,0), (34, 34), (100, 255, 20), 1)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)

def angle_from_triangle(data, img):
    import cv2
    if not len(data):
        return 0, img
    p1, p2, p, l = data

    bisec = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))

    bx, by = bisec
    vb = bx - C_VAL, by - C_VAL
    va = C_VAL * 2 - C_VAL, C_VAL - C_VAL

    vbx, vby =  vb
    vax, vay = va
    ab = vax*vbx + vay*vby
    ma = math.sqrt(vax**2 + vay**2)
    mb = math.sqrt(vbx**2 + vby**2)
    cosa = ab / (ma * mb)
    # angle = math.degrees(cosa)
    angle = math.acos(cosa) * 180 / math.pi
    if by < C_VAL:
        angle = 360 - angle

    # print(ab, ma, mb, cosa, angle)

    cv2.line(img, CENTRAL, bisec, (10, 240, 150), 1)
    cv2.line(img, CENTRAL, (C_VAL * 2, C_VAL), (10, 290, 150), 1)

    cv2.putText(img, str(round(angle, 2)), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [250, 190, 200], 1)
    return angle, img


def frames(path):
    frames = 0
    files = os.listdir(path)

    for f in files:
        f = f.split('.')[0]
        f = int(f)
        if f > frames:
            frames = f
    return frames

def window_center(whandle):
    from win32 import win32gui as w
    rect = w.GetWindowRect(whandle)
    l,t, r,b = rect
    x = int((r-l)/2)
    y = int((b-t)/2)
    return x, y

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])
    
if __name__ == '__main__':
    # calc_cm_angle(None, corners)
    calc_vect_angle((17, 33), (33, 33))
