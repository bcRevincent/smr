#!/usr/bin/env python3
#  -*- coding:utf-8 -*-

import threading
import time
import random
from pymongo import MongoClient
import json
import requests


def takeSecond(elem):
    return int(elem[1:])


def task(url, datas, headers):
    r = requests.post(url, data=datas, headers=headers)
    print(r.text)
    print(r.status_code)


def main():
    # db_client = MongoClient("127.0.0.1", 27017, replicaset='rs0')
    db_client = MongoClient("127.0.0.1", 27017)
    db_handler2 = db_client["network"]["attack_info"]
    db_handler1 = db_client["network"]["attack_info_temp"]

    url = "http://httpbin.org/post"
    headers = {'Content-Type': 'application/json'}

    sw_result_list = [('1', 'ARP_FLOOD'), ('2', 'LLDP_FLOOD'), ('3', 'DDoS'), ('4', 'FLOW_TABLE_OVERFLOW'),
                      ('5', 'FLOW_TABLE_FLUSH')]
    # sw_result_id, sw_result_name = random.sample(sw_result_list, 1)[0]
    sw_name_list = ['openflow:1', 'openflow:2', 'openflow:3', 'openflow:4', 'openflow:5', 'openflow:6', 'openflow:7', 'openflow:8', 'openflow:9', 'openflow:10']
    # sw_name = random.sample(sw_name_list, 1)[0]
    judge = "neural network"

    while True:
        timestamp_oldlocal = time.localtime()
        timestamp_old = time.time()
        output_data_list = []
        while time.time() - timestamp_old < 52:
            sw_result_id, sw_result_name = random.sample(sw_result_list, 1)[0]

            output_data1 = ({"id": sw_result_id})
            output_post = ({"alarmType": int(sw_result_id)})

            output_post.update({"alarmLevel": 2})

            output_data1.update({"name": sw_result_name})
            output_post.update({"alarmTitle": sw_result_name})

            output_post.update({"alarmContent": "测试测试"})

            output_post.update({"alarmAdvice": "alarmAdvice"})

            sw_name_number = random.randint(1, 3)
            sw_name_sample = (random.sample(sw_name_list, sw_name_number))
            sw_name_sample.sort(key=takeSecond)
            sw_name = '#'.join(sw_name_sample)
            output_data1.update({"target": sw_name})
            output_post.update({"csResourceId": 666})

            timestamp = time.localtime()
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
            output_data1.update({"time": timestr})
            output_post.update({"alarmCreateTime": timestr})

            output_data1.update({"judge_standard": judge})
            db_handler1.insert_one(output_data1)
            output_data_list.append(output_data1)

            alarmId1 = int((str(output_data1['_id']))[:8], 16)
            alarmId = time.strftime("%Y%m%d%H%M%S", time.localtime(alarmId1))
            output_post.update({"alarmId": int(alarmId)})

            datas = json.dumps(output_post)
            print(datas)

            t1 = threading.Thread(target=task, args=(url, datas, headers))
            t1.start()
            # r = requests.post(url, data=datas, headers=headers)
            # print(r.text)
            # print(r.status_code)

            sleeptime = random.randint(3, 12)
            print("sleep" + str(sleeptime))
            time.sleep(sleeptime)

        print("db_handler2 refresh!!")
        with db_client.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                db_handler2.delete_many({'time': {'$lte': time.strftime('%Y-%m-%d %H:%M:%S', timestamp_oldlocal)}},
                                        session=session)
                db_handler2.insert_many(output_data_list, session=session)


if __name__ == "__main__":
    main()
