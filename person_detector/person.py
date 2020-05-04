import cv2
from time import time
from math import sqrt
import numpy as np 
ID = 1
distance = 0    
box = []   
times = {}
data = {}
fps = 1
trigger = 0.9
dist_trigger = 0.4   
f_trigger = 0.5

fps_k  = 1

#_______________NET___________________________________________________________
renet = cv2.dnn.readNet('person-reidentification-retail-0079/FP32/person-reidentification-retail-0079.xml',
                            'person-reidentification-retail-0079/FP32/person-reidentification-retail-0079.bin')
net = cv2.dnn.readNet('person-detection-retail-0013/FP32/person-detection-retail-0013.xml',
                          'person-detection-retail-0013/FP32/person-detection-retail-0013.bin')
netsize = (544, 320)
renetsize = (64, 160) 
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
renet.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
renet.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  



#_____________________________________________________________________________
#_____________Compare Founding Boxes__________________________________________
def compare(data, box, save=0):
    reblob = cv2.dnn.blobFromImage(box, size=renetsize, ddepth=cv2.CV_8U)
    renet.setInput(reblob)
    reout = renet.forward()
    reout = reout.reshape(256)
    reout /= sqrt(np.dot(reout, reout))
    ide = 1
    distance = -1

    if len(data) != 0:
        for x in data:
            distance = np.dot(reout, data[x])
            ide += 1
            if distance > dist_trigger:
                ide = x
                break

    if distance < dist_trigger:
        data['id{}'.format(ide)] = reout
        if save:
            cv2.imwrite('photos/id{}.jpg'.format(ide), box)

    return distance, ide

#__________________MAIN_______________________________________________________
cap = cv2.VideoCapture("2.mp4")
grab, frame = cap.read()
while True:
    #_____________________________________________________________________________
    #_____________Frame_Reading___________________________________________________

    start = time()
    #k++
    grab, frame = cap.read()
    if not grab:
        raise Exception('Image not found!')
    
    #___________________________________________________________________________
    #_____________Taking blob___________________________________________________
    blob = cv2.dnn.blobFromImage(frame, size=netsize, ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()

    objects = 0
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])
    
    #_____________________________________________________________________________
    #_____________Try to get personal ID__________________________________________
        if confidence > trigger:
            objects += 1
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            box = frame[ymin:ymax, xmin:xmax]        
            try:               
                distance, ID = compare(data, box, 1)
            except:
                continue
            if ID in times:
                times[ID] += 1 / fps_k
            else:
                times[ID] = 1 / fps_k      

            cv2.putText(frame, '{}'.format(ID), (xmin, ymax - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(frame, '{:.1f}s'.format(times[ID]), (xmin, ymax + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)



    cv2.putText(frame, 'objects:{}'.format(objects), (5, frame.shape[0]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, 'IDs:{}'.format(len(data)), (5, frame.shape[0]-45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    end = time()
    fps = 1 / (end - start)     

    cv2.putText(frame, 'fps:{:.2f}'.format(fps), (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
    cv2.imshow("Window", frame)

    if cv2.waitKey(10) == 27: 
        break
    #jpeg = cv2.imencode('.jpg',frame)[1].tostring()
    cv2.imshow("Window", frame)

cap.release()
cv2.destroyAllWindows()