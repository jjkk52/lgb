#!/usr/bin/python
# -*- coding: UTF-8 -*-
import string
from zhon.hanzi import punctuation
import numpy as np
import re
import pandas as pd
import json
from math import degrees
import os
import requests
import time
import datetime
import urllib3
urllib3.disable_warnings()
import random

headers = { # 虚拟号
    'authority': 'aqy.lgb360.com',
}

headers['content-type'] = 'application/json;charset=UTF-8'
headers['origin'] = 'https://aqy.lgb360.com'

cookies = {
}


def qukong(sss):  # 去除不可见字符
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 匹配不是中文、大小写、数字的其他字符
    sss = cop.sub('', str(sss))  # 将string1中匹配到的字符替换成空字符
    return sss


def getallda(filename):  # 获取所有答案
    # filename=r"D:\aqy.xls"
    df = pd.read_excel(filename, header=0, usecols=[1, 2])
    df = df.values
    shape = df.shape
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            df[x, y] = qukong(df[x, y])
           
    return df


def getda(timu):  # 根据题目获取答案
    for x in all:
        if x[0] == timu:
            return x[1].upper()
            break
    return ""


def char2num(a):  # 将答案AB转为12
    aa = ""
    for xx in a:
        aa = aa+str(ord(xx)-64)
    return aa


def startCompetition():
    # 开始考试
    url = 'https://aqy.lgb360.com/aqy/ques/startCompetition'
    data = {}
    response = requests.post(url, headers=headers,
                             cookies=cookies, verify=False,   data=data)
    state = json.loads(response.text)
    # print(response.text)
    return state


def answerQues(state):

    if state.get('data'):  # right:这种通过key来查询是否存在的方式是比较好的
        # {"result":{"msg":"成功"},"data":{"labelTag":"安全大神","percentAll":95,"score":32,"drawCount":3,"correctNum":15,"correctRate":100}}
        if state.get('data').get('labelTag'):
            #没有写抽奖次数，因为会没有drawCount
            print(f"安全称号：{state['data']['labelTag']}\n本次得分：{str(state['data']['score'])}")
            exit()
        if state.get('data',{}).get('rightOptions'):
            print(f"正确答案：{state['data']['rightOptions']}")
            print('-----------------------------------------------')     
        if state.get('data').get('ques'):  # 是题目
            if not(state.get('data',{}).get('isRight')) and state['data']['ques']['quesNo']!=1:
                # print(f"不是第一题，也没有isRight，代表答错了,提交")  
                return submitCompetition()
            else:               
                # {"result":{"msg":"成功"},"data":{"isRight":true,"answeredOptions":["组织或者参与本单位应急救援演练"],"ques":{"quesNo":4,"options":["张某","王某","李某"],"quesTypeStr":"单选题","quesId":"KDxQpRUeI70qGBgI","content":"张某为某服装厂安全生产管理人员，王某为某食品厂安全生产管理人员，李某为某煤矿安全生产管理人员。依据《安全生产法》的规定，上述人员的任免，应当告知主管的负有安全生产监督管理职责的部门的是（  ）。","quesType":1},"rightOptions":["组织或者参与本单位应急救援演练"]}}
                print(f"第{str(state['data']['ques']['quesNo'])}题，{str(state['data']['ques']['quesTypeStr'])}")
                print(f"题目：{str(state['data']['ques']['content'])}")
                print(f"选项：{str(state['data']['ques']['options'])}")
        else:
            #没有题目，说明全部答完，提交
            return submitCompetition()
    else:
        #     # {"result":{"code":9,"msg":"您当天的答题次数已用完，请明天再试~"}}
        if state.get('result',{}).get('msg'):
            print(state['result']['msg'])
            exit()



    
    url = 'https://aqy.lgb360.com/aqy/ques/answerQues'

    data = {"answerOptions": [], "quesId": "xxxx"}
    data["quesId"] = state["data"]["ques"]["quesId"]

    da = getda(qukong(str(state['data']['ques']['content'])))
    if da != "":
        print(da)
        da = char2num(da)
    else:
        print("未找到答案，默认选A")
        da = "1"
        # 下面是自己输入答案，不用默认答案
        # dainput = input('输入答案需要，第一个为1：')
        # if dainput != "":
        #     print(f'您输入的答案是{dainput}')
        #     da = dainput

    ms=random.randint(10,28)
    print(f'延时{ms}秒提交答案')
    time.sleep(ms)
    
    dalist = list(da)

    for x in dalist:
        data["answerOptions"].append(
            state["data"]["ques"]["options"][int(x)-1])

    data = json.dumps(data)
    response = requests.post(url, headers=headers,
                             cookies=cookies, verify=False,  data=data)
    state = json.loads(response.text)
    return state  


def submitCompetition():
    # 提交分数
    url = 'https://aqy.lgb360.com/aqy/ques/submitCompetition'
    data = '{}'
    response = requests.post(url, headers=headers, cookies=cookies,
                             verify=False,   data=data.encode())
    state = json.loads(response.text)
    return state 


def main():
    global all
    all = getallda(os.path.join(os.path.split(
        os.path.realpath(__file__))[0], "aqy.xls"))
    global cookies
    global headers
    data = '{}'
    state = startCompetition()
    while True:
        state = answerQues(state)


if __name__ == '__main__':

    main()

