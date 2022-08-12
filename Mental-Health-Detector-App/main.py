import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import metrics
import pickle
import tkinter as tk
from _csv import writer
from datetime import date

import serial.tools.list_ports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

import matplotlib.pyplot as plt



class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='blue')

        ButtonN = tk.Button(self, text="New patient", font=("Arial", 15), command=lambda: controller.show_frame(NewPatient))
        ButtonN.place(x=350, y=200)
        ButtonO = tk.Button(self, text="Old patient", font=("Arial", 15), command=lambda: controller.show_frame(OldPatient))
        ButtonO.place(x=350, y=250)


class NewPatient(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='green')

        lavel1 = tk.Label(self,text="Enter Patient Name")
        lavel1.place(x=200,y=30)
        entry = tk.Entry(self, width=40)
        entry.focus_set()
        entry.place(x=330,y=30)

        lavel2 = tk.Label(self, text="Enter Patient Age")
        lavel2.place(x=200,y=80)
        entry2 = tk.Entry(self, width=40)
        entry2.focus_set()
        entry2.place(x=330,y=80)

        lavel3 = tk.Label(self, text="Patient Phone Number")
        lavel3.place(x=200,y=130)
        entry3 = tk.Entry(self, width=40)
        entry3.focus_set()
        entry3.place(x=330,y=130)

        Save = tk.Button(self, text="Submit And Take Hardware input", font=("Arial", 15), command=lambda: self.take_info(entry.get(),entry2.get(),entry3.get()))
        Save.place(x=120, y=160)

        showInfo = tk.Button(self, text="Show the Mental Health", font=("Arial", 15),
                         command=lambda: self.show(entry.get(), entry2.get(), entry3.get()))
        showInfo.place(x=460, y=160)

        levelms = tk.Label(self, text=" And Provide heartrate and body temperature ......")
        levelms.place(x=200, y=220)

        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=100, y=450)

    def runArduno(self):
        #arduion code
        ports = serial.tools.list_ports.comports()
        serialList = serial.Serial()
        portList = []

        for onePort in ports:
            portList.append(str(onePort))
            print(str(onePort))

        # val = input("Select Port: COM")
        val = 3
        it = 0
        for x in range(0, len(portList)):
            if portList[x].startswith("COM" + str(val)):
                portVar = "COM" + str(val)
                print(portList[x])

        serialList.baudrate = 9600
        serialList.port = portVar
        serialList.open()

        s = ""

        with open("test.txt", 'w') as f:
            while True:

                if serialList.in_waiting:
                    packet = serialList.readline()
                    f.write(packet.decode('utf'))
                    s = (packet.decode('utf'))
                    if (s[0] == "2"):
                        it += 1
                    if (it == 6):
                        break
                    # f.write("\n")
            f.close()
        return True
    def convertPrediction(self,prediction):
        if(prediction=='0'):
            return "no risk you are mentally healthy"
        if(prediction=="1"):
            return "moderate risk. take care yourself"
        return "high risk. take medical help immediately"
    def calucation(self,id,age):
        allTemp = []
        allHeartRate = []
        f = open("test.txt", "r")
        all = f.readlines()
        f.close()
        for i in all:
            if (i[0] == '1'):
                allTemp.append(float(i[2:-1]))
                continue
            if (i[0] == '2'):
                allHeartRate.append(float(i[2:-1]))

        nowD = date.today().strftime("%d/%m/%Y")
        bodyTemp = sum(allTemp) / len(allTemp)
        heartRate = sum(allHeartRate) / len(allHeartRate)
        bloodSugure = 8
        systolicBp = 113
        diastolicBp = 76

        List = [id, nowD, age, systolicBp, diastolicBp, bloodSugure, bodyTemp, heartRate, -1]
        with open('data.csv', 'a') as f_object:

            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(List)

            # Close the file object
            f_object.close()


        dataLocation = "data.csv"
        file = pd.read_csv(dataLocation)
        filename = 'finalized_model.pkl'
        loaded_model = pickle.load(open(filename, 'rb'))
        n = len(file) - 1
        age = file.iloc[n]["age"]
        systolicBp = file.iloc[n]["systolicBp"]
        diastolicBp = file.iloc[n]["diastolicBp"]
        bloodSugure = file.iloc[n]["bloodSugure"]
        bodyTemp = file.iloc[n]["bodyTemp"]
        heartRate = file.iloc[n]["heartRate"]
        p = [[age, systolicBp, diastolicBp, bloodSugure, bodyTemp, heartRate]]
        predAns = loaded_model.predict(p)[0]
        file.at[len(file) - 1, 'prediction'] = predAns
        file.reset_index(drop=True)
        file.to_csv(dataLocation, index=False)


        return  bodyTemp,heartRate,nowD,self.convertPrediction(str(predAns))
    def show(self,e1,e2,e3):

        temp,heart,dt,predict = self.calucation(e3,e2)
        level = tk.Label(self, text="Your Information has been saved Here is your mental heath details")
        level.place(x=200, y=220)
       # date bodyTemp, heartRate, prediction
        lv1 = tk.Label(self, text="Date = "+dt).place(x=200,y=250)
        lv2 = tk.Label(self, text="Body Temarature = "+str(temp)).place(x=200, y=280)
        lv3 = tk.Label(self, text="HeartRate = "+str(heart)).place(x=200, y=310)
        lv3 = tk.Label(self, text="Prediction = "+ predict).place(x=200, y=340)

    def take_info(self,e1,e2,e3):
        level = tk.Label(self, text="Your Information has been saved now check mental health")
        level.place(x=200, y=220)
        f = open("userInfo/"+e3, "w")
        f.write("Name  : "+e1+"\n")
        f.write("Age   : "+e2+"\n")
        f.write("Number: "+e3+"\n\n\n")
        f.close()

        f = open("userInfo/allUser",'a')
        f.write(e3+"\n")
        f.close()

        check = self.runArduno()
        if(check):
           # self.levelms.destroy()
            #level = tk.Label(self, text="Your Information has been saved now check mental health")
            #level.place(x=100, y=500)
            print("it work")







class OldPatient(tk.Frame):
    def getHeartRate(self, id):
        f = open("data.csv", "r")
        all = f.readlines()
        f.close()
        heartRates = []
        for i in all:
            parts = i.split(",")
            if (len(parts) > 1 and parts[0] == str(id)):
                heartRates.append(float(parts[7]))
        return heartRates

    def getBodyTemp(self, id):
        f = open("data.csv", "r")
        all = f.readlines()
        f.close()
        bodyTemps = []
        for i in all:
            parts = i.split(",")
            if (len(parts) > 1 and parts[0] == str(id)):
                bodyTemps.append(float(parts[6]))
        return bodyTemps

    def doesExist(id):
        f = open("C:\\Users\\USER\\PycharmProjects\\MentalHealthApp\\userInfo\\allUser", "r")
        all = f.readlines()
        f.close()
        return (id in all)

    def show(self, id, graphNo):
        l = []
        if (graphNo == 1):
            l = self.getBodyTemp(id)
        else:
            l = self.getHeartRate(id)
        plt.plot(l)
        if (graphNo == 1):
            plt.title("body temp")
        else:
            plt.title("heart rate")
        plt.show()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='Tomato')
        lavel1 = tk.Label(self, text="Enter Phone Number")
        lavel1.place(x=200, y=100)
        entry = tk.Entry(self, width=40)
        entry.focus_set()
        #self.show("6",1)
        entry.place(x=330, y=100)
        id = entry.get()
        Button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=450, y=650)

        Button = tk.Button(self, text="Show Graph of Temperature", font=("Arial", 15),
                           command=lambda: self.show(entry.get(),1))
        Button.place(x=380, y=200)
        Button = tk.Button(self, text="Show Graph of Heart rate", font=("Arial", 15),
                           command=lambda: self.show(entry.get(),2))
        Button.place(x=100, y=200)

        Button = tk.Button(self, text="Check Again", font=("Arial", 15), command=lambda: controller.show_frame(NewPatient))
        Button.place(x=100, y=450)

        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=650, y=450)




class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (FirstPage, NewPatient, OldPatient):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")


app = Application()
app.maxsize(800, 500)
app.mainloop()


