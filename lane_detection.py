import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


def grayscale(img):
  return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold=50, high_threshold=200):
  return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size=5):
  return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)   
    ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def slope_lines(image,lines):
    
    img = image.copy()
    poly_vertices = []
    order = [0,1,3,2]

    left_lines = [] #  / bu egimli cizgiler
    right_lines = [] #  \ bu egimli cizgiler
    for line in lines:
        for x1,y1,x2,y2 in line:

            if x1 == x2:
                pass #dikey cizgiler
            else:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1

                if m < 0:
                    left_lines.append((m,c))
                elif m >= 0:
                    right_lines.append((m,c))

    left_line = np.mean(left_lines, axis=0)
    right_line = np.mean(right_lines, axis=0)

    #print(left_line, right_line)

    for slope, intercept in [left_line, right_line]:

        rows, cols = image.shape[:2]
        y1= int(rows) #image.shape[0]

        #y2 degeri: gercek height degerinin %60 ustu ya da y1 degerinin %60 altidir
        y2= int(rows*0.6) #int(0.6*y1)

        #Dogru denklemi y=mx +c bu sekilde de ifade edebiliriz x=(y-c)/m
        x1=int((y1-intercept)/slope)
        x2=int((y2-intercept)/slope)
        poly_vertices.append((x1, y1))
        poly_vertices.append((x2, y2))
        draw_lines(img, np.array([[[x1,y1,x2,y2]]]))
    """
    (x2left,y2left)=poly_vertices[1]
    (x2right,y2right)=poly_vertices[3]
    if (x2left>x2right):
        poly_vertices[1]=((x2left+x2right)//2,y2left*0,5)
        poly_vertices[3]=((x2left+x2right)//2,y2right*0,5)
    """
    poly_vertices = [poly_vertices[i] for i in order]
    cv2.fillPoly(img, pts = np.array([poly_vertices],'int32'), color = (0,170,120))
    return cv2.addWeighted(image,0.7,img,0.4,0.)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):

    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    line_img = slope_lines(line_img,lines)
    return line_img

def weighted_img(img, initial_img, a=0.1, b=1., c=0.):
    return cv2.addWeighted(initial_img, a, img,b, c)

def get_vertices(image):
    rows, cols = image.shape[:2]
    bottom_left  = [cols*0.15, rows*0.9]
    top_left     = [cols*0.45, rows*0.58]
    bottom_right = [cols*0.95, rows*0.9]
    top_right    = [cols*0.55, rows*0.58] 
    
    ver = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return ver

def detectLines(image):
    
    #Grayscale
    gray_img = grayscale(image)
    #Gaussian Blur
    smoothed_img = gaussian_blur(img = gray_img, kernel_size = 5)
    #Canny Edge Detection
    canny_img = canny(img = smoothed_img, low_threshold = 180, high_threshold = 240)
    #Maskelenmis Resim elde et
    masked_img = region_of_interest(img = canny_img, vertices = get_vertices(image))
    #Cizgelere Hough Transform uygula
    houghed_lines = hough_lines(img = masked_img, rho = 1, theta = np.pi/180, threshold = 20, min_line_len = 20, max_line_gap = 180)
    #Kenarlara Cizgi Ciz
    output = weighted_img(img = houghed_lines, initial_img = image, a=0.8, b=1., c=0.)
    
    return output

