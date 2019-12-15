import mysql.connector
import csv
import os
import functools
import time
import collections
import multiprocessing

def partition(lst, number_of_chunks):
    return [ lst[i::number_of_chunks] for i in range(number_of_chunks)]

mydb = mysql.connector.connect(
    host="localhost",
    user="hello",
    passwd='',
    database='db'
)

mycursor = mydb.cursor()

mycursor.execute("select id,topic from MOCK_DATA limit 100000")
topicList=[]
freq={}
for row in mycursor:
    topicList.append(row[1])



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

#reduced=functools.reduce(reducer,mapped)
start_time=time.time()
pool=multiprocessing.Pool(processes=16)
part_data=partition(topicList, number_of_chunks=16)
print(len(part_data))
mapped=pool.map(pool_mapper, part_data)

reduced=functools.reduce(reducer,mapped)
print(reduced.most_common(20))


print("mapreduce took",time.time()-start_time," seconds")
def freq_words(data):
    cnt=collections.Counter()
    for word in data:
        cnt.update(word.split())
    return cnt.most_common(20)

start_time=time.time()
print(freq_words(topicList))
print("non-mapreduce took",time.time()-start_time," seconds")




