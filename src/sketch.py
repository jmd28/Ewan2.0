import cv2 
import numpy as np 
import urllib.request
import requests

path = "sickwickeddrawin.png"

def draw_img(url):
    resp = requests.get(url, stream=True).raw
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    
    # Edges 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.medianBlur(gray, 5) 
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  
                                                cv2.THRESH_BINARY, 9, 9) 
    # Cartoonization 
    color = cv2.bilateralFilter(img, 9, 250, 250) 
    cartoon = cv2.bitwise_and(color, color, mask=edges) 

    cv2.imwrite(path, edges)
    return path

