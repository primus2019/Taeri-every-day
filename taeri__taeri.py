from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import urllib.request
import uuid
import cv2
import numpy as np
import sklearn.cluster
import ctypes
import os

instagram = 'https://www.instagram.com/taeri__taeri/?hl=en'

def test():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(instagram)
    Nnq7C_weEfm = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/*[self::div]')
    # print('len of Nnq7C weEfm: {}'.format(len(Nnq7C_weEfm)))
    rand_1 = random.randint(0, len(Nnq7C_weEfm) - 1)
    print('random 1: {}'.format(rand_1))
    v1Nh3_kIKUG___bz0w = Nnq7C_weEfm[rand_1].find_elements_by_tag_name('a')
    # print('lem of viNh3_kIKUG____bz0w: {}'.format(len(v1Nh3_kIKUG___bz0w)))
    rand_2 = random.randint(0, len(v1Nh3_kIKUG___bz0w) - 1)
    print('random 2: {}'.format(rand_2))
    pic_link           = v1Nh3_kIKUG___bz0w[rand_2].get_attribute('href')
    driver.get(pic_link)
    
    pic_url = driver.find_elements_by_tag_name('img')[1].get_attribute('src')
    pic_name = 'taeri/{}.jpg'.format(uuid.uuid4().hex)
    urllib.request.urlretrieve(pic_url, pic_name)
    return pic_name


def picy(pic_name):
    pic_ds = cv2.imread(pic_name)
    pic_ds_ori = pic_ds
    height = len(pic_ds)
    width  = len(pic_ds[0])
    print('height:\t{}'.format(len(pic_ds)))
    print('width:\t{}'.format(len(pic_ds[0])))
    print('pixel:\t{}'.format(len(pic_ds[0][0])))
    pic_ds = np.reshape(pic_ds, (-1,3))
    kmeans = sklearn.cluster.KMeans(10).fit(pic_ds)
    colors = kmeans.cluster_centers_
    colors_vote = []
    for i, rgb in enumerate(colors):
        colors[i][0] = (int)(colors[i][0])
        colors[i][1] = (int)(colors[i][1])
        colors[i][2] = (int)(colors[i][2])
    for rgb in colors:
        colors_vote.append((int)(rgb[0] + rgb[1] + rgb[2]))
    lightest = np.argmax(colors_vote)
    print(colors)
    top    = (int)((1824 - height) / 2)
    bottom = (int)((1824 - height) / 2)
    left   = (int)((2736 - width) / 2)
    right  = (int)((2736 - width) / 2)
    ideal  = colors[lightest]
    print('top: {}; botton: {}; left: {}; right: {}'.format(top, bottom, left, right))
    print('ideal color: [{}, {}, {}]'.format(ideal[0], ideal[1], ideal[2]))
    pic_ds = cv2.copyMakeBorder(pic_ds_ori, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=[(int)(ideal[0]), (int)(ideal[1]), (int)(ideal[2])])
    cv2.imwrite(pic_name, pic_ds)
    pic_name = os.path.abspath(pic_name)
    print('pic_dir: {}'.format(pic_name))
    return pic_name


def setPaper(pic_dir):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_dir, 0)


if __name__ == '__main__':
    pic_name = test()
    pic_dir = picy(pic_name)
    setPaper(pic_dir)