#!/usr/bin python3
# -*- coding:utf-8 -*-

'''
Author: 索尔@U2
Email: i@aalyp.cc
user: 44929
'''

from api import *

import logging
import sys

import re
from collections import Counter

from time import sleep
import time
import datetime

def isnum(s):
	try:
		num = float(s)
		return 1
	except:
		return 0

logger = logging.getLogger('sweet')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("sweet.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

print('---参数设定---')
suc = input('赠送UC量: ')
while not isnum(suc):
	logger.error('格式不正确!')
	suc = input('赠送UC量: ')
suc = int(suc)
good = input('发给好人的信息: ')
bad = input('发给坏人的信息: ')
print('---参数设定完毕---')

chain = input('请输入发糖串: \n')

print('---发糖脚本开始---')
start = datetime.datetime.now()
logger.info('进程启动')
total = 0 # 总尝试次数

pattern = re.compile('\d{5}|\d{3}')
bank = chain.split('<--')
bank = [re.sub('\[em\d+]', '', text) for text in bank] # 去除 emoji
user = []
for text in bank:
	uid = pattern.findall(text)
	if uid != []:
		user.append(int(uid[0]))

cheater = Counter(user)
cheater.subtract(set(user))
cheater = set(list(cheater.elements())) # 重复发UID骗糖的坏人x
user = set(user) - cheater # 正常领糖的好人w

str1 = '{' + ', '.join(str(uid) for uid in user) + '}'
str2 = '{' + ', '.join(str(uid) for uid in cheater) + '}'
logger.info('好人: \n                                  %s', str1)
logger.info('坏人: \n                                  %s', str2)
# 预处理 UID 合法性
print('---预处理UID---')
temp = set()
for uid in user:
	retry = 0
	status = valid(uid)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5min 后重试... (尝试: %s)', str(retry))
		sleep(300)
		status = valid(uid)
	if status:
		temp.add(uid)
	else:
		logger.warning('不正确的UID: %s', uid)
user = temp

temp = set()
for uid in cheater:
	retry = 0
	status = valid(uid)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5min 后重试... (尝试: %s)', str(retry))
		sleep(300)
		status = valid(uid)
	if status:
		temp.add(uid)
	else:
		logger.warning('不正确的UID: %s', uid)
cheater = temp

estimate = (len(user) + len(cheater)) * ( suc * 1.5 + 100 ) # 消耗UC
print('---预处理完毕---')

str1 = '{' + ', '.join(str(uid) for uid in user) + '}'
str2 = '{' + ', '.join(str(uid) for uid in cheater) + '}'
logger.info('实发好人: \n                                      %s', str1)
logger.info('实发坏人: \n                                      %s', str2)

logger.info('共发送%s份糖, 其中好人%s名, 坏人%s名' % (str(len(user) + len(cheater)), str(len(user)), str(len(cheater))))
logger.info('预计消耗UC: %s' % (estimate))

retry = 0
myuc = uc(myuid())
while myuc == -1:
	retry += 1
	total += 1
	logger.error('U2娘抽风, 等待 5min 后重试... (尝试: %s)', str(retry))
	sleep(300)
	myuc = uc(myuid())
if myuc > 2:
	logger.info('当前UCoin存量: %s', str(myuc))
	if myuc < estimate:
		logger.critical('UCoin存量不足!')
		print('---发糖脚本结束---')
		exit()		

print('---发糖进程开始---')
logger.info('预热: 5分钟')
sleep(300)
logger.info('开始')

all = len(user)
min = all * 5
hrs = int(min / 60)
min -= hrs * 60
if hrs == 0:
	logger.info('正在处理好人组(%s), 预计耗时: %s分钟' % (str(all), str(min)))
else:
	logger.info('正在处理好人组(%s), 预计耗时: %s小时%s分钟' % (str(all), str(hrs), str(min)))
count = 1
for uid in user:
	retry = 0
	status = transfer(uid, suc, good)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5min 后重试... (尝试: %s)', str(retry))
		sleep(300)
		status = transfer(uid, suc, good)
	if status == 0:
		logger.info('%s/%s: %s', str(count), str(all), str(uid))
	else:
		logger.info('%s/%s: %s 未知错误', str(count), str(all), str(uid))
	count += 1
	sleep(300)

all = len(cheater)
min = all * 5
hrs = int(min / 60)
if hrs == 0:
	logger.info('正在处理坏人组(%s), 预计耗时: %s分钟' % (str(all), str(min)))
else:
	logger.info('正在处理坏人组(%s), 预计耗时: %s小时%s分钟' % (str(all), str(hrs), str(min)))
count = 1
for uid in cheater:
	retry = 0
	status = transfer(uid, suc, bad)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5min 后重试... (尝试: %s)', str(retry))
		sleep(300)
		status = transfer(uid, suc, bad)
	if status == 0:
		logger.info('%s/%s: %s', str(count), str(all), str(uid))
	else:
		logger.info('%s/%s: %s 未知错误', str(count), str(all), str(uid))
	count += 1
	sleep(300)

end = datetime.datetime.now()
print('---发糖进程结束---')
current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
logger.info('结束时间: %s' % (current))

delta = end - start
delta_gmtime = time.gmtime(delta.total_seconds())
duration = time.strftime("%H:%M:%S", delta_gmtime)
logger.info('总耗时: %s, 其中U2娘掉线%s次' % (duration, str(total)))
print('---发糖脚本结束---')