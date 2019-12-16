import mysql.connector
import csv
import os
import functools
import time
import collections
import multiprocessing

def partition(lst, number_of_chunks):
    return [ lst[i::number_of_chunks] for i in range(number_of_chunks)]
def mapper(str):
    tokens=str.split()
    return collections.Counter(tokens)

def reducer(counter1, counter2):
    counter1.update(counter2)
    return counter1

def pool_mapper(partitionedData):
    mapped=map(mapper, partitionedData)
    reduced=functools.reduce(reducer,mapped)
    return reduced
def trend(number):
    mydb = mysql.connector.connect(
        host="localhost",
        user="appserver",
        passwd='foobarzoot',
        database='scalica'
    )

    mycursor = mydb.cursor()

    mycursor.execute("select topic_id from micro_topic_posts limit 100000")
    topicList2 = []
    freq = {}
    for row in mycursor:
        topicList2.append(row[0])
    print(topicList2)
    topicList = []
    for num in topicList2:
        sql = "select topic from micro_topic where id=(%s)"
        val = (str(num),)
        mycursor.execute(sql, val)
        for row in mycursor:
            topicList.append(row[0])

    for row in mycursor:
        topicList.append(row[0])



    #reduced=functools.reduce(reducer,mapped)
    start_time=time.time()
    pool=multiprocessing.Pool(processes=8)
    part_data=partition(topicList, number_of_chunks=8)
    print(len(part_data))
    mapped=pool.map(pool_mapper, part_data)

    reduced=functools.reduce(reducer,mapped)
    trend=[]
    for item in reduced.most_common(number):
        trend.append(item[0])
    return trend
def down_field():
    mydb = mysql.connector.connect(
        host="localhost",
        user="appserver",
        passwd='foobarzoot',
        database='scalica'
    )

    mycursor = mydb.cursor()

    mycursor.execute("select id,topic from micro_topic limit 100000")
    topicList2 = []
    
    for row in mycursor:
        topicList2.append(row)
    return topicList
