# Скрипт читает json-файл с точками сглаженной кривой, полученный с помощью
# скрипта closed_curve.py, и пишет новый файл с анимацией ряда Фурье.
# 
# Запускать через командную строку.
# Перед этим нужно положить json-файл с точками сглаженной кривой в одну папку 
# с этим скриптом.
# В командной строке указываем название файла с точками сглаженной кривой 
# (без полного пути), а также название файла, куда записать анимацию.
# Также можно указать максимальную частоту вращения последней стрелки.
# Если её не указать, она будет равна 200.
#
# Скрипт может рендерить анимацию достаточно долго (до нескольких минут при 
# максимальной частоте 200) и не подавать признаков жизни, но через какое-то 
# время анимация сохранится и откроется окно matplotlib с анимацией.
# 
# Можно также не сохранять анимацию, а просто показать её в окне matplotlib.
# Для этого можно просто не указать имя файла, куда записать анимацию.
#
# Если не хотим, чтобы анимация открывалась в окне matplotlib, то пишем 
# последним аргументом слово "dontshow". Эта опция доступна, только если 
# указано имя файла, куда сохранять анимацию.
#
#
#       Примеры запуска скрипта из командной строки:
#
#
# Читаем файл coordinates123456_smooth20.json и записываем анимацию в файл
# portrait.mp4.
#
# Ввод: 
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json portrait.mp4
# 
# Вывод:
# Creating animation...
# Animation saved to D:/Sasha/python/portrait.mp4
# Showing animation...
#
#
# Делаем то же самое, но указываем максимальную частоту 50.
#
# Ввод:
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json portrait.mp4 50
# 
# Вывод:
# Creating animation...
# Animation saved to D:/Sasha/python/portrait.mp4
# Showing animation...
# 
#
# Читаем файл coordinates123456_smooth20.json и не записываем анимацию, а только
# показываем её в окне matplotlib.
# 
# Ввод:
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json 
# 
# Вывод:
# Creating animation...
# Showing animation...
#
#
# Читаем файл coordinates123456_smooth20.json и не записываем анимацию, а только
# показываем её в окне matplotlib с максимальной частотой 80.
#
# Ввод:
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json 80
# 
# Вывод:
# Creating animation...
# Showing animation...
#
#
# Читаем файл coordinates123456_smooth20.json и записываем анимацию, но не
# показываем её в окне matplotlib.
#
# Ввод:
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json portrait.mp4 dontshow
# 
# Вывод:
# Creating animation...
# Animation saved to D:/Sasha/python/portrait.mp4
#
#
# Читаем файл coordinates123456_smooth20.json и записываем анимацию, но не
# показываем её в окне matplotlib, с максимальной частотой 100.
#
# Ввод:
# python D:/Sasha/python/portrait_animation3.py coordinates123456_smooth20.json portrait.mp4 100 dontshow
# 
# Вывод:
# Creating animation...
# Animation saved to D:/Sasha/python/portrait.mp4


import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


cd = os.path.dirname(os.path.abspath(__file__))

input_file_path = os.path.join(cd, sys.argv[1])

show = True

if len(sys.argv) > 2:
    arg2 = sys.argv[2]
    if arg2.isnumeric():
        q = int(arg2)
        save = False
    else:
        output_file_path = os.path.join(cd, arg2)
        save = True
else:
    q = 200
    save = False
if len(sys.argv) > 3 and save:
    arg3 = sys.argv[3]
    if arg3.isnumeric():
        q = int(arg3) 
        if len(sys.argv) > 4 and sys.argv[4] == 'dontshow':
            show = False   
    elif arg3 == 'dontshow':
        q = 200
        show = False

fp = open(input_file_path, 'r')
data = np.array(json.load(fp))
fp.close()

print('Creating animation...')

res = data[:,0]
ims = -data[:,1]
cmplxs = res + 1j*ims

phis = np.linspace(0, 2*np.pi, len(data)+1)[:-1]

def cn(n):
    exparr = np.exp(-1j*n*phis)
    return (np.sum(exparr * cmplxs)) / len(data)

cns = np.array([cn(i) for i in range(-q,q+1)])

test = np.sum(np.array(
    [cns[i+q] * np.exp(-1j*i*phis) for i in range(-q,q+1)]), axis=0)

fig = plt.figure(figsize=(7.0, 9.0))
images = []
plt.axis('off')
plt.plot(np.real(test), np.imag(test), c='grey', linewidth='1.0')
plt.ylim(np.min(ims)-50, np.max(ims)+50)
plt.xlim(np.min(res)-50, np.max(res)+50)
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()

for phi in np.linspace(0, 2*np.pi, 3001)[:-1]:
    arrows = np.zeros((2*q+1,2))
    z = cns[q]
    arrows[0] = z.real, z.imag
    for i in range(1, q+1):
        z = cns[q+i] * np.exp(1j*i*phi)
        arrows[2*i-1] = z.real, z.imag
        z = cns[q-i] * np.exp(-1j*i*phi)
        arrows[2*i] = z.real, z.imag
    sums = np.zeros_like(arrows)
    sums[0] = arrows[0]
    for i in range(1,2*q+1):
        sums[i] = sums[i-1] + arrows[i]
    image, = plt.plot(sums[:,0], sums[:,1], c='black', linewidth='1.0', animated=True)
    images.append([image])

ani = animation.ArtistAnimation(fig, images, interval=20, blit=True, repeat_delay=20)

if save:
    ani.save(output_file_path)
    print('Animation saved to ' + output_file_path)
if show:
    print('Showing animation...')
    plt.show()
