"""
Для тренировки YOLOv3 необходима папка obj, содержащая следующее
1) Файл 000001.jpg (изображение)
2) Файл 000001.txt (файл с текстовыми данными координат размеченного бокса на фото)

Зачастую возникают проблемы с созданием этой папки, которые сложно заметить, но они прерывают
процесс тренировки, что очесь сильно раздражает.
Поэтому я создал эту программу, которая устраняет все (наверное) проблемы за вас!

"""
import os
import time

# Функция меняет расширение всех изображений на .jpg
def rename_to_jpg(path):
    invalid_files = []# список файлов, который стоит удалить
    for file in os.listdir(path):
        if (file[-4:] == ".png") or (file[-4:] == ".gif"):
            if file[:-4] + ".jpg" in os.listdir(path): # если нашли, например, 144.png но уже есть 144.jpg, то удаляем первый
                invalid_files.append(file)
            else:
                os.rename(path+ "/" + file, path + "/" + file[:-4] + ".jpg")
    return invalid_files # далее этот массив используется во всех других функциях


# функция проверяет, существует ли для каждого .jpg файла .txt файл и не пуст ли этот .txt файл
def check_if_txt_exists(path, invalid_files):
    i = 0
    for file in os.listdir(path):
        if (file[-4:] == ".jpg") and (i % 2 == 0):  # если позиция файла четная (счет с НУЛЯ) и он - фотка, то проверяем наличие соответствующего текстового файла
            if file[:6]+".txt" not in os.listdir(path):  # если для картинки нет текстового файла - онаа не была размечена
                print("Изображение {} не было размечено!".format(file))
                invalid_files.append(file)
                i += 1
            else:
                txt = file[:6]+".txt" # если для картинки есть текстовый файл, то проверяем его на пустоту
                with open(path + "/" + txt, "r") as f:
                    lines = f.readlines()
                    if lines != []:
                        pass
                    else:
                        invalid_files.append(file)  # если текстовый файл пуст, то удаляется И он, И картинка
                        invalid_files.append(txt)
                        print(txt + " ПУСТ!")
                i += 1
        elif (file[-4:] == ".txt") and (i % 2 == 0):  # если позиция четная (счет с НУЛЯ), а на ней текстовый файл - его следует удалить
            print("Файл " + file + " не на своём месте!")
            invalid_files.append(file)
            i += 2 # здесь перескакиваем через один файл для правильности работы
        elif (file[-4:] == ".txt") and (i % 2 != 0):  # если позиция НЕчетная (счет с НУЛЯ), то текстовый файл на своем месте
            i += 1
    return invalid_files


# функция удаляет все файлы, которые не были размечены (у которых пустые .txt файлы)
def delete_invalid_files(invalid_files, path):
    if invalid_files != []:
        time.sleep(2)
        print("\n\nВот все некорректные файлы:\n")
        for file in invalid_files:
            print(file)
        choice = str(input("\nХотите ли вы удалить эти файлы, так как они бессмысленны?(y/n):\n"))
        if choice == "y":
            for file in invalid_files:
                if file in os.listdir(path):
                    print("Удаляю файл: " + path + r"\\" + file)
                    os.remove(path + r"\\" + file)
        else:
            print("Пока!")
    else:
        print("Всё в порядке!")


# функция нумерует все оставшиеся файлы в формате 000001 в порядке возрастания
def set_numbers(path):
    choice = str(input("\nХотите ли вы пронумеровать все файлы в порядке возрастания?(y/n)\n"))
    if choice == "y":
        start = int(input("С какого числа начать нумерацию?\n"))
        j = start
        for i, file in enumerate(os.listdir(path)):
            extention = file[-4:]
            #print(path + r"\\" + file, "rename to" , path + r"\\" + "{:06}".format(j) + extention)
            try:
                os.rename(path + r"\\" + file, path + r"\\" + "{:06}".format(j) + extention)
                if i % 2 != 0:
                    j += 1
            except FileExistsError:
                continue
        print("Файлы были пронумерованы в порядке возрастания!")
    else:
        print("Ну ладно, пока!")

############################################################################
path = str(input("Введите путь к папке с фотографиями и .txt файлами: \n"))
invalid_files = rename_to_jpg(path)
check_if_txt_exists(path, invalid_files)
delete_invalid_files(invalid_files, path)
set_numbers(path)

