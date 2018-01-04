import csv
data = {}
# open file and create reader
f=open('/var/www/html/ML-crisis-prediction/^IXIC.csv', 'r')
f.readline()
# read header
# header = next(reader)
# store the contents of the csv file as a dictionary
for line in f:
   row = line.split(",")	
   data[row[0]] = {}
   data[row[0]]['open']=row[1]
   data[row[0]]['high']=row[2]
   data[row[0]]['low']=row[3]
   data[row[0]]['close']=row[4]
   data[row[0]]['adj_close']=row[5]
   data[row[0]]['volume']=row[6]

# print (data['2017-06-26'])
print (data)