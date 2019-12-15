import mysql.connector
import csv
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="hello",
    passwd='',
    database='db'
)

mycursor = mydb.cursor()
# lst=[]
# with open('MOCK_DATA (1).csv') as f:
#   reader=csv.reader(f,delimiter=',')
#   for row in reader:
#     lst.append(row)
#
# print(lst[1])
# sql="insert into brands (id,name) values (%s,%s)"
# for row in lst[1:]:
#   val=(row[0],row[1])
#   mycursor.execute(sql,val)

# mydb.commit()
go =1001
with os.scandir('data/') as data:
    for file in data:
        fe='data/'+file.name
        lst=[]
        with open(fe) as f:
            reader=csv.reader(f,delimiter=',')
            for row in reader:
                lst.append(row)

        print(file.name)
        sql="insert into MOCK_DATA (id,topic) values (%s,%s)"
        for row in lst[1:]:
            val=(str(go),row[1])
            mycursor.execute(sql,val)
            go+=1
mydb.commit()

#
# mycursor.execute("select id from MOCK_DATA order by id desc limit 1")
# for row in mycursor:
#     print(row[0])

# mycursor.execute("select id,topic from MOCK_DATA")
# for row in mycursor:
#     print(row[0],row[1])