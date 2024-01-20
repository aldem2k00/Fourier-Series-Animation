# Программа для обведения кривых
# 
# С помощью этой программы можно отметить много точек на какой-нибудь
# картинке и записать в json-файл координаты этих точек.
#
# Инструкция:
# 1) При запуске программы она предложит открыть картинку, с которой будем
#    работать. По умолчанию показаны файлы типа jpg, png, bmp, gif. Если нужна
#    картинка другого формата, можно в правом нижнем углу выбрать "Any type"
#    вместо "Images".
# 2) Точки ставим левой кнопкой мыши. Нажатие на правую кнопку мыши удаляет 
#    последнюю точку.
# 3) Чтобы сохранить результат, нажимаем Enter. Должно появиться уведомление о
#    том, что координаты сохранены успешно. Там же будет написано название 
#    файла. Файл с координатами записывается в ту же папку, где лежит картинка.


import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showinfo, showerror
import PIL
from PIL import Image, ImageTk
import json
import os
import time


# Цвет точек на картинке
POINT_COLOR = '#FF0000'


def setpoint(event):
    """Ставим точку и запоминаем её координаты"""
    left = hbar.get()[0] * img.size[0]
    top = vbar.get()[0] * img.size[1]
    ovals.append(canvas.create_oval(
        left + event.x-2, 
        top + event.y-2, 
        left + event.x+2, 
        top + event.y+2, 
        fill=POINT_COLOR, 
        width=0))
    points.append((left + event.x, top + event.y))


def removepoint(event):
    """Удаляем точку и забываем её координаты"""
    if len(points):
        canvas.delete(ovals[-1])
        del ovals[-1]
        del points[-1]


def scroll(event):
    """Скроллим холст мышкой"""
    canvas.yview_scroll(-1*(event.delta//120), "units")


def saveresults(event):
    """Сохраняем результаты"""
    if len(points) == 0:
        return
    fp = open(filename, 'w')
    json.dump(points, fp)
    fp.close()
    showinfo('Coordinates saved!', 'Coordinates saved to ' + filename)


# Создаём окно
root = tk.Tk()
root.title('Image Points')
root.withdraw() # скрываем окно

root.update() # без этого не работает привязка клавиши Enter

opensuccess = False
while not opensuccess:
    # Выбираем картинку
    imgpath = tk.filedialog.askopenfilename(
        title='Choose image',
        filetypes=[
            ('Images', '*.jpg;*.jpeg;*.png;*.bmp;*.gif'),
            ('Any type', '*.*')
        ]
    )

    # Если пользователь не захотел ничего выбирать, то завершаем работу
    if not imgpath:
        root.destroy()
        exit()

    # Открываем картинку
    try:
        img = Image.open(imgpath)
        img.verify()              #  Картинку ужно открыть второй раз после
        img = Image.open(imgpath) #  вызова verify, иначе будет ошибка!
        opensuccess = True
    except:
        showerror('Error', 'Image is either broken or not an image at all')

root.update() # без этого не работает привязка клавиши Enter

root.deiconify() # показываем главное окно

# Папка, в которой лежит картинка
cd = os.path.dirname(imgpath)

# Имя файла, в который будем сохранять результат
filename = cd + '/coordinates' + str(int(time.time()*1000)) + '.json'

# Создаём и размещаем в главном окне фрейм
frame = tk.Frame(root, width=img.size[0], height=img.size[1])
frame.pack()

# Создаём холст и скроллбары
canvas = tk.Canvas(frame,
                   width=img.size[0], 
                   height=img.size[1],
                   scrollregion=(2, 2, #  Двойки подобраны эмпирически
                   img.size[0] + 2,    #  так, чтобы точки появлялись
                   img.size[1] + 2))   #  ровно под курсором.

hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
hbar.config(command=canvas.xview)
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
vbar.config(command=canvas.yview)

# Привязываем скроллбары к холсту
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Размещаем холст на фрейме
canvas.pack()

# Отображаем картинку на холсте
tkimg = ImageTk.PhotoImage(img)
canvas.create_image(img.size[0]//2, 
                    img.size[1]//2, 
                    image=tkimg)

# Список для запоминания идентификаторов кружочков на холсте
ovals = []

# Список для запоминания координат точек
points = []

# Привязываем функции событий к холсту
canvas.bind('<Button-1>', setpoint)
canvas.bind('<Button-3>', removepoint)
root.bind("<MouseWheel>", scroll)
root.bind("<Return>", saveresults) # <Return> это клавиша Enter

root.mainloop()
