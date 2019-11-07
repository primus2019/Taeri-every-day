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
import sys


def get_instagram():
    taeri = 'taeri__taeri'
    if len(sys.argv) > 1:
        if sys.argv[1] != '-t':
            taeri = ' '.join(sys.argv[1:])
        else: # if test mode
            taeri = ' '.join(sys.argv[2:])
    print('Looking for {}...'.format(taeri))
    instagram = 'https://www.instagram.com/{}/?hl=en'.format(taeri)
    return instagram


def test(instagram):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    # get url
    try:
        driver.get(instagram)
        # get pic_url
        Nnq7C_weEfm = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/*[self::div]')
        rand_1 = len(Nnq7C_weEfm) - random.randint(0, len(Nnq7C_weEfm) - 1)
        v1Nh3_kIKUG___bz0w = Nnq7C_weEfm[rand_1].find_elements_by_tag_name('a')
        rand_2 = random.randint(0, len(v1Nh3_kIKUG___bz0w) - 1)
        pic_link           = v1Nh3_kIKUG___bz0w[rand_2].get_attribute('href')
        driver.get(pic_link)
        pic_url = driver.find_elements_by_tag_name('img')[1].get_attribute('src')
        # set pic_name
        pic_name = 'taeri/{}.jpg'.format(uuid.uuid4().hex)
        urllib.request.urlretrieve(pic_url, pic_name)

        height  = 2 * ctypes.windll.user32.GetSystemMetrics(1)
        width = 2 * ctypes.windll.user32.GetSystemMetrics(0)

        if sys.argv[1] == '-t':
            print('len of Nnq7C weEfm: {}'.format(len(Nnq7C_weEfm)))
            print('random 1: {}'.format(rand_1))
            print('lem of viNh3_kIKUG____bz0w: {}'.format(len(v1Nh3_kIKUG___bz0w)))
            print('random 2: {}'.format(rand_2))
            print('h: {}'.format(height))
            print('w: {}'.format(width))
        driver.close()
    except Exception:
        driver.close()
        print('Sorry that an error occurred! Try other one!')
        exit()
    return pic_name


def picy(pic_name):
    print('Generating Insta-styled padded picture...')
    pic_ds = cv2.imread(pic_name)
    pic_ds_ori = pic_ds
    
    win_width  = 2 * ctypes.windll.user32.GetSystemMetrics(0)
    win_height = 2 * ctypes.windll.user32.GetSystemMetrics(1)
    width  = len(pic_ds[0])
    height = len(pic_ds)
    if sys.argv[1] == '-t':
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
    # print(colors)
    top    = (int)((win_height - height) / 2)
    bottom = (int)((win_height - height) / 2)
    left   = (int)((win_width  - width)  / 2)
    right  = (int)((win_width  - width)  / 2)
    ideal  = colors[lightest]
    if sys.argv[1] == '-t':
        print('top: {}; botton: {}; left: {}; right: {}'.format(top, bottom, left, right))
        print('ideal color: [{}, {}, {}]'.format(ideal[0], ideal[1], ideal[2]))
    pic_ds = cv2.copyMakeBorder(pic_ds_ori, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=[(int)(ideal[0]), (int)(ideal[1]), (int)(ideal[2])])
    cv2.imwrite(pic_name, pic_ds)
    pic_name = os.path.abspath(pic_name)
    print('Picture saved at {}'.format(pic_name))
    print('Just press Win+D and enjoy your adored one. XD')
    return pic_name


def setPaper(pic_dir):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_dir, 0)


if __name__ == '__main__':
    instagram = get_instagram()
    pic_name  = test(instagram)
    pic_dir   = picy(pic_name)
    setPaper(pic_dir)