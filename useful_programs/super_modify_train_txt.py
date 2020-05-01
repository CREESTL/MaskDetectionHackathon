"""
Проверяет, есть ли .txt файл для каждой фотки и НЕ ПУСТ ЛИ ОН

"""
import os
import time

# функция проверяет, существует ли для каждого .jpg файла .txt файл и не пуст ли этот .txt файл
def check_if_txt_exists(path):
    invalid_files = [] # список файлов, который стоит удалить
    files = os.listdir(path)
    for i in range(1, len(files)-1, 2):
        jpg = files[i]
        if jpg[:6]+".txt" not in files:
            print("File {} hasn't been labeled!".format(jpg))
        else:
            txt = jpg[:6]+".txt"
            with open(path + "/" + txt, "r") as f:
                lines = f.readlines()
                if lines != []:
                    pass
                else:
                    invalid_files.append(jpg)
                    print(txt + " HAS NO DATA!")
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
            for txt_file in invalid_files:
                jpg_file = txt_file[:6] + ".jpg" # это название уже не картинки а .txt файла
                if jpg_file in os.listdir(path):
                    os.remove(path + r"\\" + jpg_file)
                if txt_file in os.listdir(path):
                    os.remove(path + r"\\" + txt_file)
        else:
            print("Пока!")
    else:
        print("Всё в порядке.Пока!")


# функция нумерует все оставшиеся файлы в формате 000001 в порядке возрастания
def set_numbers(path):
    choice = str(input("Хотите ли вы пронумеровать все файлы в порядке возрастания?(y/n)"))
    if choice == "y":
    j = 1
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


path = str(input("Введите путь к папке с фотографиями и .txt файлами: \n"))
invalid_files = check_if_txt_exists(path)
delete_invalid_files(invalid_files, path)
set_numbers(path)

