import math
import cv2
import numpy as np
from sklearn.cluster import KMeans

CM_POINTER = 'assets/cam_pointer.png'


CM_X1 = 128 - 40 - 2
CM_X2 = 128 + 40 + 2
CM_Y1 = 128 - 40 - 2
CM_Y2 = 128 + 40 + 2
CENTER = 42
ANGLE_BASE_LINE = [(CENTER, CENTER), (CENTER + 20, CENTER)]

def vector(a, b):
    ax, ay = a
    bx, by = b
    return bx - ax, by - ay

def dot_product(a, b):
    ax, ay = a
    bx, by = b
    return ax*bx + ay*by

def magnitude(a):
    x, y = a
    return math.sqrt(x**2 + y**2)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def calc_angle(a, b):
    a1, a2 = a
    b1, b2 = b
    vec_a = vector(a1, a2)
    vec_b = vector(b1, b2)
    dotprod = dot_product(vec_a, vec_b)
    mag_a = magnitude(vec_a)
    mag_b = magnitude(vec_b)
    rad = float(dotprod) / float(mag_a * mag_b)
    rad = math.acos(rad)
    _, a2y = a2
    if a2y > CENTER:
        angle = math.degrees(2 * math.pi - rad)
    else:
        angle = math.degrees(rad)
    return rad, angle

def correct_sight(sights):
    start, end = sights
    sx, sy = start
    ex, ey = end
    delta = 13
    dsx = sx - CENTER
    dsy = sy - CENTER
    
    if abs(dsx) < delta and abs(dsy) < delta:
        return [CENTER, CENTER], end
    else:
        return [CENTER, CENTER], start
def extrude_color(img, upper, lower):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array(lower)   # Lower bound of blue in HSV
    upper_blue = np.array(upper) # Upper bound of blue in HSV
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    extracted = cv2.bitwise_and(img, img, mask=mask)
    return extracted

def sight_points(img):
    red_extracted = extrude_color(img, [10, 255, 255], [0, 120, 70])
    gray_image = cv2.cvtColor(red_extracted, cv2.COLOR_BGR2GRAY)

    # Parameters for Shi-Tomasi corner detection
    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=2, qualityLevel=0.01, minDistance=10)
    corners = np.int0(corners)

    # Draw the corners on the original image 
    sights = []
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), 1)
        sights.append((x, y))
    # Show the result

    sight_start, sight_end = correct_sight(sights)
    return sight_start, sight_end

def camera_angle(img):
    img = img[CM_Y1:CM_Y2, CM_X1:CM_X2]
    sight_start, sight_end = sight_points(img)
    rad, angle = calc_angle([sight_start, sight_end], ANGLE_BASE_LINE)
    # print('Angle', rad, angle)
    return (rad, sight_end), angle

def idk(img):
    img = img[CM_Y1:CM_Y2, CM_X1:CM_X2]
    # get green
    # get erode to points
    # get corners
    path_img = extrude_color(img, [80, 255, 255], [40, 40, 40])
    gray = cv2.cvtColor(path_img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary image (optional)
    _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Define the erosion kernel (a 3x3 matrix of ones)
    kernel = np.ones((3, 3), np.uint8)  # Adjust the kernel size for stronger/weaker erosion

    # Apply the erosion operation
    eroded_image = cv2.erode(binary_image, kernel, iterations=1)  # Change iterations for stronger erosion
    points = cv2.findNonZero(binary_image)
    points = points.reshape(points.shape[0], -1)

    k = 2

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points)

    # Get the cluster centers and labels for each point
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    # print('sklearn', centers)
    # Display the original and eroded images
    # cv2.imshow('Original Image', binary_image)
    # cv2.imshow('Eroded Image', eroded_image)
    # Calculate the Euclidean distance between the given point and each point in the array
    distances = np.linalg.norm(centers - np.array([42, 42]), axis=1)

    # Find the index of the closest point
    closest_point_index = np.argmin(distances)

    # Get the closest point
    closest_point = centers[closest_point_index]
    print(closest_point, tuple(closest_point))
    x,y = closest_point
    cv2.circle(img, (int(x), int(y)), radius=4, color=(0, 0, 255), thickness=2)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
