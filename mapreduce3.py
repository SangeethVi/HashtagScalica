import mysql.connector
import csv
import os
import functools
import time
import collections
import multiprocessing

def chunkify(lst,number_of_chunks):
    return [ lst[i::number_of_chunks] for i in range(number_of_chunks)]

mydb = mysql.connector.connect(
    host="localhost",
    user="hello",
    passwd='',
    database='db'
)

mycursor = mydb.cursor()

mycursor.execute("select id,topic from MOCK_DATA limit 100000")
data=[]
freq={}
for row in mycursor:
    data.append(row[1])



def mapper(str):
    tokens=str.split()
    return collections.Counter(tokens)
def reducer(cnt1,cnt2):
    cnt1.update(cnt2)
    return cnt1
def chunk_mapper(chunk):
    mapped=map(mapper,chunk)
    reduced=functools.reduce(reducer,mapped)
    return reduced
#reduced=functools.reduce(reducer,mapped)
start_time=time.time()
pool=multiprocessing.Pool(processes=16)
data_chunks=chunkify(data,number_of_chunks=16)
print(len(data_chunks))
mapped=pool.map(chunk_mapper,data_chunks)

reduced=functools.reduce(reducer,mapped)
print(reduced.most_common(20))


print("mapreduce took",time.time()-start_time," seconds")
def freq_words(data):
    cnt=collections.Counter()
    for word in data:
        cnt.update(word.split())
    return cnt.most_common(20)

start_time=time.time()
print(freq_words(data))
print("non-mapreduce took",time.time()-start_time," seconds")




