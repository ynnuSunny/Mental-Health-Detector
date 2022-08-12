from _csv import writer
from datetime import date
allTemp=[]
allHeartRate=[]
f = open("test.txt", "r")
all=f.readlines()
f.close()
for i in all:
    if(i[0]=='1'):
        allTemp.append(float(i[2:-1]))
        continue
    if(i[0]=='2'):
        allHeartRate.append(float(i[2:-1]))


id=100
age=53
nowD = date.today().strftime("%d/%m/%Y")
bodyTemp=sum(allTemp)/len(allTemp)
heartRate=sum(allHeartRate)/len(allHeartRate)
bloodSugure = 8
systolicBp = 113
diastolicBp = 76

List = [id,nowD,age, systolicBp, diastolicBp, bloodSugure, bodyTemp, heartRate, -1]
with open('data.csv', 'a') as f_object:

    writer_object = writer(f_object)

    # Pass the list as an argument into
    # the writerow()
    writer_object.writerow(List)

    # Close the file object
    f_object.close()
# print(allTemp)
# print(allHeartRate)
# print(avgTemp)
# print(avgHeartRate)

