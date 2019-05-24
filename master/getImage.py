import cv2
def getImage(filepath, camid=0):
  vidcap = cv2.VideoCapture(camid)
  flag, image = vidcap.read()
  print("flag is ", flag)
  if(flag):
    cv2.imwrite(filepath, image)
  return flag   
        

# getImage("frame.jpg", 0)

# print(cv2.__version__)
# vidcap = cv2.VideoCapture(0)
# #vidcap.set(CV_CAP_PROP_BUFFERSIZE, 1);
# #success,image = vidcap.read()
# count = 0
# success = True
# steps=5

# next = time.time() + steps
# while success:
    
#   success,image = vidcap.read() 
#   now = time.time()
#   if now>= next:
#       cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
#       t = time.strftime("%Y-%m-%d-%H-%M-%S")
#       print ('Read a new frame: ', success, "time: ", t)
#       next = time.time() + steps
#   #cv2.waitKey(5000)
#       count += 1
#   if count==20:
#    success=False
#    vidcap.release()
