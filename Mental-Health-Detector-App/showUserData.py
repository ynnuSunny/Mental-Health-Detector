import matplotlib.pyplot as plt
class Graph:
    def getHeartRate(self,id):
        f = open("data.csv", "r")
        all = f.readlines()
        f.close()
        heartRates = []
        for i in all:
            parts = i.split(",")
            if (len(parts) > 1 and parts[0] == str(id)):
                heartRates.append(float(parts[7]))
        return heartRates

    def getBodyTemp(self,id):
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
    def show(self,id,graphNo):
        l=[]
        if(graphNo==1):
            l = self.getBodyTemp(id)
        else:
            l=self.getHeartRate(id)
        plt.plot(l)
        plt.title("body temp")
        plt.show()

graph = Graph()
graph.show("2423534634",4)
