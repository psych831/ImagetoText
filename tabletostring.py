import pytesseract
import numpy as np
import cv2
def tabletostring(img):
    #convert to greyscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #threshold the image
    ret, thres_val = cv2.threshold(gray,180, 255, cv2.THRESH_BINARY)
    #invert the image
    inv_image = cv2.bitwise_not(thres_val)
    sizes = inv_image.shape
    rows = sizes[0]
    columns = sizes[1]
    #label the connected Components
    rets, markers  = cv2.connectedComponents(inv_image)
    vals = []
    #find the largest
    for i in range(rets):
        count = 0
        for element in markers:
            for digit in element:
                if digit == i:
                    count = count + 1
        vals.append(count)
    index = 0
    for i in range(len(vals)):
        if vals[i]==max(vals):
            index = i
    #all other components apart from the largest one are set to 0
    for i in range(rows):
        for j in range(columns):
            if markers[i][j]!=index:
                markers[i][j]=0
            else:
                markers[i][j]=255
    markers = np.uint8(markers)
    #create image - grid
    boundary_less = inv_image - markers
    boundary_less = np.uint8(boundary_less)
    boundary_less = cv2.bitwise_not(boundary_less)
    #change tesseract address as required
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    output_below = pytesseract.image_to_string(boundary_less)
    return output_below