import cv2
from time import time

net = cv2.dnn.readNet('face-detection-retail-0005/FP32/face-detection-retail-0005.xml',
                        'face-detection-retail-0005/FP32/face-detection-retail-0005.bin')
netsize = (300, 300)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

croped_face = []
trigger = 0.9

cap = cv2.VideoCapture("1.mp4")
grab, frame = cap.read()
while  True:
    start = time()
    grab, frame = cap.read()
    #if not grab:
    #    raise Exception('Image not found!')
    #___________________________________________________________________________
    #_____________Taking blob___________________________________________________
    blob = cv2.dnn.blobFromImage(frame, size=netsize, ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()

    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])

        if confidence > trigger:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            croped_face = frame[ymin:ymax, xmin:xmax]       
            
    end = time()
    fps = 1 / (end - start)     

    cv2.putText(frame, 'fps:{:.2f}'.format(fps+3), (5, 25),
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
    cv2.imshow("Window", frame)

    if cv2.waitKey(10) == 27: 
        break
    

cap.release()
cv2.destroyAllWindows()