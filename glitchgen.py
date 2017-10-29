import numpy as np
import cv2
import datetime
import imageio
import sys
from random import randint

urlstring = ''
if len(sys.argv) > 1:
    urlstring = sys.argv[1]
else:
    urlstring = 'gobwah.mp4'

cap = cv2.VideoCapture(urlstring)
fps = cap.get(cv2.CAP_PROP_FPS)

def applyFilter(num,img):
    #Python doesn't have switch so we have to do this instead
    if num == 0:
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        out = img - magnitude_spectrum
    elif num == 1:
        out = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, np.ones((20,20),np.uint8))
    elif num == 2:
        out = cv2.dilate(img, np.ones((randint(10,100), randint(10,100)),np.uint8))
    elif num == 3:
        out = img*img/2
    elif num == 4:
        out = img*3/2
    return out
   
namestringcounter = 1
length = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #Randomly assigns filter type and duration
        if length == 0:
            length = randint((int)(fps/2),(int)(fps*3))
            filt = randint(0,4)
            filt1 = randint(0,4)
            filt2 = randint(0,4)
            #determines how many filters to apply at once
            stack = randint(0,100)
            
        #Applies a filter to the frame and sets it as output
        output = applyFilter(filt,frame)
        if stack >= 50:
            output = applyFilter(filt1,output)
        if stack >= 80:
            output = applyFilter(filt2,output)
        
        imagestring = "temp/videoFrame" + str(namestringcounter) + ".png"
        cv2.imwrite(imagestring, output)

        cv2.imshow('frame', output)

        namestringcounter += 1

        length -= 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


################
## CREATE GIF ##
################

imagearr = []
for namestringcount in range(1, namestringcounter):
    imagestring = "temp/videoFrame" + str(namestringcount) + ".png"
    imagearr.append(imageio.imread(imagestring))
output_file = "output/outputgif-%s.gif" % datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
if fps != 0:
    imageio.mimsave(output_file, imagearr, duration=(1/fps))
    print "Gif has been generated."
else:
    print "Invalid file. No gif for you."
