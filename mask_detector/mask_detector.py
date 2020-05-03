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

# Функция рисует бокс вокруг объекта
def drawPred(frame, classId, conf, x, y, width, height):


    label = '%.2f' % conf

    # Получаем название класса и "уверенность"
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Рисуем бокс и название класса
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    y = max(y, labelSize[1])
    cv.rectangle(frame, (x,y),(width,height), (0,255,0), 2)
    cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

# Функция создает массив координат точек боксов
def postprocess(frame, outs):
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
            if confidence > confThreshold:
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
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

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
        drawPred(frame, classIDs[i], confidences[i], x, y, x + width, y + height)


######### ОСНОВНОЕ ТЕЛО ПРОГРАММЫ #########


# Объявляем некоторые полезные переменные
# минимальная уверенность = 1 процент
confThreshold = 0.01
nmsThreshold = 0.1

# Количество кадров, через которое будет производится распознавание маски
step = 10

# Размеры входного изображения
inpWidth = 608
inpHeight = 608

# Файл с названиями классов
classesFile = "classes.names"

# Файл конфига для yolov3
modelConf = "yolov3.cfg"
# Файл с весами для yolov3
modelWeights = 'yolo-obj_last.weights'

# Считываем названия классов
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Считываются все данные для сетки
net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)

# Она настраивается
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

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
        blob = cv.dnn.blobFromImage(resized, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
        #blob = cv.dnn.blobFromImage(resized,  size=(inpWidth, inpHeight), mean=[0, 0, 0], crop=False)
        net.setInput(blob)

        # Получаем выходные данные
        outs = net.forward(getOutputsNames(net))

        # Эти данные обрабатываются в функции
        postprocess(resized, outs)

    # Завершаем отсчёт времени работы для вычисления FPS
    end = time()
    fps = 1 / (end - start)
    cv.putText(resized, 'fps:{:.2f}'.format(fps + 3), (5, 25),cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Кадр со всеми нарисованными боксами показывается
    cv.imshow(winName, resized)


    # При нажатии на "q" все окна закрываются
    if cv.waitKey(14) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

