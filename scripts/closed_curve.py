# Скрипт читает json-файл с точками и пишет новый файл со сглаженной кривой.
#
# Запускать через командную строку.
# Перед этим нужно положить json-файл с точками в одну папку с этим скриптом.
#
# В командной строке указываем название файла с точками (без полного пути).
# Также можно указать параметр сглаживания. Чем он больше, тем больше точек
# на построенной кривой будет между каждой парой исходных точек. По умолчанию
# параметр сглаживания равен 20, но он не может быть меньше 4.
#
#       Примеры запуска скрипта из командной строки:
# Ввод: 
# python D:/Sasha/python/closed_curve.py coordinates123456.json
#
# Вывод:
# Closed curve with smoothness == 20 saved to 
# D:/Sasha/python/coordinates123456_smooth20.json
#
# Ввод:
# python D:/Sasha/python/closed_curve.py coordinates123456.json 35
#
# Вывод:
# Closed curve with smoothness == 35 saved to 
# D:/Sasha/python/coordinates123456_smooth35.json

import os
import sys
import json
import numpy as np
from scipy.interpolate import splrep, splev


smoothness = 20 if len(sys.argv) < 3 else int(sys.argv[2])
assert smoothness > 3, 'Smoothness must be greater than 3'

cd = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(cd, sys.argv[1])

fp = open(input_file_path, 'r')
data = np.array(json.load(fp))
fp.close()

dts = np.linalg.norm(data[1:] - data[:-1], axis=1)
tts = np.zeros(len(data))
tts[1:] = np.cumsum(dts)

t_arr = np.linspace(0, tts[-1], len(data)*smoothness)
xtck = splrep(tts, data[:,0])
ytck = splrep(tts, data[:,1])

xins = splev(t_arr, xtck)
yins = splev(t_arr, ytck)

ends_xs = np.concatenate((xins[-2:], xins[:2]))
ends_ys = np.concatenate((yins[-2:], yins[:2]))
ends_ts = np.array([0, 1, smoothness+1, smoothness+2])

cls_xtck = splrep(ends_ts, ends_xs)
cls_ytck = splrep(ends_ts, ends_ys)
cls_ts = np.arange(smoothness + 3)
cls_xs = splev(cls_ts, cls_xtck)
cls_ys = splev(cls_ts, cls_ytck)

finalxs = np.concatenate((xins, cls_xs[2:-2]))
finalys = np.concatenate((yins, cls_ys[2:-2]))

finallist = [[finalxs[i], finalys[i]] for i in range(len(finalxs))]

output_filename = (os.path.splitext(os.path.basename(sys.argv[1]))[0] 
    + '_smooth' + str(smoothness) + '.json')

output_filepath = os.path.join(cd, output_filename)

fp = open(output_filepath, 'w')
json.dump(finallist, fp)
fp.close()

print('Closed curve with smoothness ==', 
    smoothness, 'saved to\n', output_filepath)
