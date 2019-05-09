import cv2
import time
 
        

print(cv2.__version__)
vidcap = cv2.VideoCapture(1)
#vidcap.set(CV_CAP_PROP_BUFFERSIZE, 1);
#success,image = vidcap.read()
count = 0
success = True
steps=5

next = time.time() + steps
while success:
    
  success,image = vidcap.read() 
  now = time.time()
  if now>= next:
      cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
      t = time.strftime("%Y-%m-%d-%H-%M-%S")
      print ('Read a new frame: ', success, "time: ", t)
      next = time.time() + steps
  #cv2.waitKey(5000)
      count += 1
  if count==20:
   success=False
   vidcap.release()
