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
            print("Ну ладно")
    else:
        print("Всё в порядке!")


# функция нумерует все оставшиеся файлы в формате 000001 в порядке возрастания
def set_numbers(path):
    choice = str(input("\nХотите ли вы пронумеровать все файлы в порядке возрастания?(y/n)\n"))
    if choice == "y":
        start = int(input("С какого числа начать нумерацию?\n"))
        j = start
        files = os.listsdir(path)
        print("files:")
        for file in files: print(file)
        for i, file in enumerate(files):
            extention = file[-4:]
            new_name = "{:06}".format(j) + extention
            print("new name = ", new_name)
            if new_name in os.listdir(path):
                differense = files.index("{:06}".format(j) + extention) - files.index(file)  # считаем разницу индексов между тем, на котором возникла ошибка и тем, который уже существует
                print(new_name + " is in " + str(os.listdir(path)))
                # Если файл с только что созданным именем существует, то мы его переименовываем через разность индексов
                print( path + r'\\'+ new_name, " rename to ", path + r"\\" + "{:06}".format(j + differense) + extention)
                os.rename(path + r'\\'+ new_name, path + r"\\" + "{:06}".format(j + differense) + extention)
                # А затем переименовываем наш исходный файл
                print(path + r"\\" + file, " rename to ", new_name)
                os.rename(path + r"\\" + file, new_name)
            else:
                # Если все в порядке, то просто переименовываем исходный файл и все
                os.rename(path + r"\\" + file, new_name)




                '''
                print()
                print(file, "1rename to", "{:06}".format(j) + extention)
                os.rename(path + r"\\" + file, path + r"\\" + "{:06}".format(j) + extention)
                if i % 2 != 0:
                    j += 1
            # Если в папке, например 300 фото, начиная с 000001.jpg, а надо пронумеровать их с 200 и больше.
            # то он попробует перименовать 0000001 в 000221, которая уже есть - это нарушает работу
            except FileExistsError:
                print("last index = ", files.index("{:06}".format(j) + extention))
                print("first index = ", files.index(file))
                differense = files.index("{:06}".format(j) + extention) - files.index(file) # считаем разницу индексов между тем, на котором возникла ошибка и тем, который уже существует
                print("DIF = ", differense)
                # прибавляем эту разницу к существующему файлу.
                print("{:06}".format(j) + extention, " rename to ", "{:06}".format(j + differense) + extention)
                os.rename(path + r"\\" + "{:06}".format(j) + extention, path + r"\\" + "{:06}".format(j + differense) + extention)
            except FileNotFoundError:
                # Если мы существующий файл перенумеровали, то он все еще остался в старом os.listdir(), поэтому его надо игнорировать там
                continue
                '''
        print("Файлы были пронумерованы в порядке возрастания!")
    else:
        print("Ну ладно, пока!")

############################################################################
path = str(input("Введите путь к папке с фотографиями и .txt файлами: \n"))
invalid_files = rename_to_jpg(path)
check_if_txt_exists(path, invalid_files)
delete_invalid_files(invalid_files, path)
set_numbers(path)

