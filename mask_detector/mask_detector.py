import cv2 as cv
import numpy as np
from time import time


# Нужна ли она вообще?
def getOutputsNames(net):
    # Выводим названия всех слоёв в сетке
    layersNames = net.getLayerNames()

    # Выводим названия только слоев с несоединенными выводами (?)
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


#------------------------------------------------------------------------------------------------------------
# Функция рисует бокс вокруг маски
def yolo_draw_box(frame, classId, conf, x, y, width, height):

    # Название класса
    label = '%.2f' % conf

    # Получаем название класса и "уверенность"
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Рисуем бокс и название класса
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    y = max(y, labelSize[1])
    cv.rectangle(frame, (x,y),(x + width, y + height), (0,255,0), 2)
    cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

# Функция рисует боксы для масок на кадре
def yolo_postprocess(frame, outs):
    # Размеры кадра
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []

    confidences = []

    boxes = []

    # out - массив выходных данных из одного слоя ОДНОГО кадра(всего слоев несколько)
    for out in outs:
        # detection - это один распознанный на этом слое объект
        for detection in out:

            # извлекаем ID класса и вероятность
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # Если "уверенность" больше минимального значения, то находим координаты боксы
            if confidence > mask_threshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                x = int(centerX - width / 2)
                y = int(centerY - height / 2)

                # Обновим все три ранее созданных массива
                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])


    # сейчас имеем заполненные массивы боксов и ID для одного кадра
    # применим non-maxima suppression чтобы отфильтровать накладывающиеся ненужные боксы
    # для КАЖДОГО кадра indices обновляются
    indices = cv.dnn.NMSBoxes(boxes, confidences, mask_threshold, nms_threshold)

    for i in indices:
        # То есть мы "отфильтровали" накладывающиеся боксы и сейчас СНОВА получаем координаты уже
        # отфильтрованных боксов
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        width = box[2]
        height = box[3]
        # И рисуем каждый бокс
        yolo_draw_box(frame, classIDs[i], confidences[i], x, y, width, height)

#------------------------------------------------------------------------------------------------------------

# Функция рисует бокс вокруг лица
def vino_draw_box(frame, conf, x, y, width, height):
    # Название класса
    label = '%.2f' % conf
    label = '%s:%s' % ("face", label)

    # Рисуем бокс и название класса
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    y = max(y, labelSize[1])
    cv.rectangle(frame, (x, y), (width, height), (0, 0, 255), 2)
    cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


# Функция рисует боксы для лиц на кадре и заполняет внешний массив координат лиц
def vino_postprocess(frame, outs):

    for detection in outs.reshape(-1, 7):
        confidence = float(detection[2])
        x = int(detection[3] * frame.shape[1])
        y = int(detection[4] * frame.shape[0])
        width = int(detection[5] * frame.shape[1])
        height = int(detection[6] * frame.shape[0])

        if confidence > face_threshold:
            cropped_face = frame[y:height, x:width]
            # Координаты лица добавляются в массив
            cropped_faces.append(cropped_face)
            # Рисуется бокса и подписывается соответствующая ему вероятность
            #confidences.append(float(confidence))
            vino_draw_box(frame, confidence, x, y, width, height)


# ------------------------------------------------------------------------------------------------------------



        ######### ОСНОВНОЕ ТЕЛО ПРОГРАММЫ #########

# Объявляем некоторые полезные переменные
# Минимальная вероятность для маски - 10 процентов
mask_threshold = 0.1
nms_threshold = 0.1

# Минимальная вероятность для лица - 90 процентов
face_threshold = 0.9

# Количество кадров, через которое будет производится распознавание маски
step = 1

# Размеры входного изображения
inpWidth = 608
inpHeight = 608

# Файл с названиями классов
classesFile = "classes.names"

# Считываем названия классов
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Массив с координатами лиц на видео
cropped_faces = []

# Файл конфига для yolov3
yolo_conf = "yolov3.cfg"
# Файл с весами для yolov3
yolo_weights = 'yolo-obj_last.weights'

# Файл конфига для OpenVINO
vino_xml = "face-detection-retail-0005/FP32/face-detection-retail-0005.xml"
vino_bin = "face-detection-retail-0005/FP32/face-detection-retail-0005.bin"

# YOLOv3
# Считываются все данные для yolo
yolo_net = cv.dnn.readNetFromDarknet(yolo_conf, yolo_weights)

# Она настраивается
yolo_net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
yolo_net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# OpenVINO
# Считываются все данные для openvino
vino_net = cv.dnn.readNet(vino_xml, vino_bin)
# Настраиваем openvino
netsize = (300, 300)
vino_net.setPreferableBackend(cv.dnn.DNN_BACKEND_INFERENCE_ENGINE)
vino_net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)



# Создатеся окно с названием "frame"
winName = 'frame'
cv.namedWindow(winName, cv.WINDOW_NORMAL)
cv.resizeWindow(winName, 608, 608)

# Считывается тестовая фотка и уменьшается
#frame = cv.imread('test_imgs/me.jpg')

cap = cv.VideoCapture("test_imgs/doctor.mp4")
grab, frame = cap.read()

# Счетчик кадров
count = 0
while True:
    # Запускаем отсчёт времени работы
    start = time()
    grab, frame = cap.read()
    count += 1
    resized = cv.resize(frame, (608,608), interpolation = cv.INTER_AREA)
    # Создаем каплю(?) из кадра и передаем ее в сеть для анализа
    # Это производится НЕ каждый кадр для ускорения работы
    if count % step == 0:
        yolo_blob = cv.dnn.blobFromImage(resized, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
        vino_blob = cv.dnn.blobFromImage(frame, size=netsize, ddepth=cv.CV_8U)
        # Помещаем данные в ОБЕ сетки
        yolo_net.setInput(yolo_blob)
        vino_net.setInput(vino_blob)

        # Получаем выходные данные c yolo
        yolo_outs = yolo_net.forward(getOutputsNames(yolo_net))

        # Получаем выходные данные c openvino
        vino_outs = vino_net.forward()

        # Данные с yolo обрабатываются в функции
        yolo_postprocess(resized, yolo_outs)

        # Данные с openvino обрабатываются в функции
        vino_postprocess(resized, vino_outs)

    # Завершаем отсчёт времени работы для вычисления FPS
    end = time()
    fps = 1 / (end - start)
    cv.putText(resized, 'fps:{:.2f}'.format(fps + 3), (5, 25),cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Кадр со всеми нарисованными боксами показывается
    cv.imshow(winName, resized)

    # При нажатии на "q" все окна закрываются
    if cv.waitKey(14) & 0xFF == ord('q'):
        break

# Все окна закрываются
cv.destroyAllWindows()

