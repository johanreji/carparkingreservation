import threading
import time
import logging
import random
import queue
import cv2
import pytz
from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow import keras
#from tf.keras import backend as K
import matplotlib.pyplot as plt
import glob
from PIL import Image 
import requests
import json

keras.backend.clear_session()
import mysql.connector

CAMID = 1
url="http://127.0.0.1:8000/getdata/"
MODEL_NAME ='newmaycnn'
WEIGHTS = 'newmaycnn_checkpoint.h5'
DIMS = (1,64,64,3)
globcount = 0
flag = False
imglist2={}


class CNN:
    def __init__(self, model_json):

        self.cnn_model = keras.models.model_from_json(model_json)
        self.cnn_model.load_weights(WEIGHTS)
        self.cnn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.cnn_model.predict(np.zeros(DIMS)) # warmup
        self.session = keras.backend.get_session()
        self.graph = tf.get_default_graph()
        self.graph.finalize() # finalize

    def preproccesing(self, data):
        # dummy
        return data

    def query_cnn(self, data):
        X = self.preproccesing(data)
        with self.session.as_default():
            with self.graph.as_default():
                prediction = self.cnn_model.predict(X)
        #print(prediction)
        return prediction


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 1
q = queue.Queue(BUF_SIZE)
vidcap = cv2.VideoCapture(CAMID)
height=150
width=150
piccount=0


json_file = open(MODEL_NAME, 'r')
loaded_model_json = json_file.read()
json_file.close()

cnn = CNN(loaded_model_json)


def sendSlotImage(img):
    url = 'http://127.0.0.1:8000/master/addarea/program/'
    files = {'media': img}
    status = requests.post(url=url, files=files)
    return status

def getSlotDims():
    url2 = 'http://127.0.0.1:8000/master/getslots/'
    r = requests.get(url = url2, params = None) 
    if r.status_code == 200:
      res = r.json()
      slotdims=res["data"]
      reslist=[]
      reslistids=[]
      #print("slotdims ", slotdims)
      for i in slotdims:
        top=i["y_left"]
        if not top:
          top=0
        top = int(float(top))
        bottom=int(float(i["height"])) + top
        left=i["x_left"]
        if not left:
            left=0
        left = int(float(left))
        right=int(float(i["width"])) + left 
        reslist.append((top, bottom, left, right))
        reslistids.append(i["slot_id"])

      return reslist, reslistids, True
    else:
      return None, None, False
            

def getImage():
	steps = 5
	next = time.time() + steps
	while True:
		success,image = vidcap.read()
		now = time.time()
		if(now >= next and success):
			t = time.strftime("%Y-%m-%d-%H-%M-%S")
			#cv2.imwrite("frames/frame%d.jpg" % now, image)
			#next = time.time() + steps
			return image, datetime.utcnow()

def createTestMatrix(imglist):
    n=len(imglist)
    X_test=np.zeros((n, DIMS[1],DIMS[2],3), dtype=np.uint8)
    s=(DIMS[1],DIMS[2],3)
    count=0;
    for i in range(n):
        temp=imglist[i]
        #temp=temp.resize((32,32), Image.ANTIALIAS)
        if(temp.shape==s):
            X_test[i, :, :, :]=temp
            count+=1
    return X_test[:count, :, :, :]  

       
def sendData(pred, ts, idlist):
    l=len(pred)
    global imglist2
    global globcount 
    slot_dict={}
    for i in range(l):
        slot_dict[idlist[i]]=str((pred[i][1] > pred[i][0]))
        print("free %f occupied %f".format(pred[i][0], pred[i][1]))
        # if(pred[i][0]>0.25 and pred[i][0]<0.75):
        # 	cv2.imwrite("tested/" + str(globcount)  + ".jpg", imglist2[i]) 
        	

    slot_json=json.dumps(slot_dict)
    print(slot_json)
    try:
   		status=requests.post(url = url, data={"val":slot_json, "ts":ts})  
    except Exception as err:
    	print(err)
    	print("error while sending data")   
    else:
        print("data send succesfully")

        

def cropSlices(img, seglist):
    ymax=img.shape[0]
    global piccount
    xmax=img.shape[1]
    print("ymax: ", ymax)
    global imglist2
    print("xmax: ", xmax)
    seglen = len(seglist)
    #cv2.imshow("img crop", img)
    #y1_prev=0
    piccount+=1
    if(piccount==10):
        piccount=0
    imglist=[]
    count=0
    for i in range(0, seglen):
        count+=1
        dim=seglist[i]
        top=max(0, dim[0])
        bottom=min(ymax, dim[1])
        left=max(0, dim[2])
        right=min(xmax, dim[3])
        roi=img[top:bottom, left:right]
        imglist2[count-1]=roi
        # cv2.imwrite("/" + str(piccount) + "." + str(count) + ".jpg", roi) 

        #roi=Image(roi)
        roi=cv2.resize(roi, dsize=(DIMS[1], DIMS[2]), interpolation=cv2.INTER_CUBIC)
        #center=(roi.shape[0]/2, roi.shape[1]/2)
        #M=cv2.getRotationMatrix2D(center, 90, 1)
            # rotated_roi=cv2.warpAffine(roi, M, (roi.shape[0], roi.shape[1]))
        imglist.append(roi)
        timeval=str(time.time())
        cv2.imwrite("segments/" + str(piccount) + str(count) + ".jpeg", roi) 
        #y1_prev=y1
    return imglist, count   

class CameraThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(CameraThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # slotimg, ts=getImage()
        # status1 = sendSlotImage(slotimg)
        # print(status1)
        while True:
            if not q.full():
                item, ts= getImage()
                q.put((item, ts))
                logging.debug('Putting '  
                              + ' : ' + str(q.qsize()) + ' items in queue')
                #time.sleep(5)
        return

class SegmentThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(SegmentThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        global globcount
        global imglist2
        seglist, seglistids, status=getSlotDims()
        print("seglist", seglist)
        while True and status:
            if not q.empty():
                item, ts = q.get()
                imglist, count=cropSlices(item, seglist)
                logging.debug('Getting ' + str(count) 
                              + ' : ' + str(q.qsize()) + ' items in queue')
                X_test=createTestMatrix(imglist)
                print("X_test shape: ", X_test.shape)
                
                pred=cnn.query_cnn(X_test/255)
                print("pcount : ", piccount)
                print("pred shape: ", pred.shape)
                print("ts: ", ts)
                print("pred ", pred)
                sendData(pred, ts, seglistids)
                imglist2={}
                ++globcount
#                sample0=X_test[0, :, :, :]
#                img0=Image.fromarray(sample0, 'RGB')
#                img0.show()
#                
#                sample1=X_test[1, :, :, :]
#                img1=Image.fromarray(sample1, 'RGB')
#                img1.show()
#                
#                sample2=X_test[2, :, :, :]
#                img2=Image.fromarray(sample2, 'RGB')
#                img2.show()
                
                #time.sleep(6)
        return

if __name__ == '__main__':
    
    p = CameraThread(name='camin')
    c = SegmentThread(name='segmenter')

    p.start()
    time.sleep(2)
    c.start()
    #time.sleep(2)
