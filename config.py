# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 15:28
# @Author  : wenlei

'''
配置文件
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders.baidu import Baidu
import time
import numpy as np

sns.set(style="whitegrid")

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


raw_path='E:/研究生数学建模2019/2019年最终获奖名单/raw_path/'
save_path='E:/研究生数学建模2019/2019年最终获奖名单/save_path/'
img_path='E:/研究生数学建模2019/2019年最终获奖名单/img/'