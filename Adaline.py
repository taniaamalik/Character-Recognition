import numpy as np
import random
import os

class Adeline(object):
    def __init__(self,alfa,treshold,size):
        self.alfa = alfa
        self.treshold = treshold
        self.bobot = [random.random() for _ in range(0,size)]
        self.bias = random.random()

    def bacaFile(self, directory):
        iterasi = 0
        isiFile = []
        self.huruf = []
        for file in os.listdir(directory): #Perulangan untuk mencari setiap file di direktori
            iterasi += 1
            if file.lower().endswith('.txt') and not file.startswith('._'): #Jika file berupa .txt maka dijalankan
                Openfile = open(directory + '/' + file, 'r', encoding="ISO-8859-1") #membuka file
                isiFile.append(Openfile.read()) #membaca semua isi file
                Openfile.close() #menutup file agak terhapus dari memori
                self.huruf.append(file[0:1])
        return isiFile
    
    def membuatArray(self, dataTxt):
        arr = []
        for i in range(len(dataTxt)) :
            dataTxt[i]=dataTxt[i].replace("#","1,").replace(".","-1,").replace("\n",'')
            arr.append(np.fromstring(dataTxt[i][:],dtype=int,sep=','))
        return arr
    
    def getTarget(self):
        target = []
        for i in range(len(self.huruf)):
            if (self.huruf[i] == "x"):
                target.append(1)
            else :
                target.append(-1)  
        return target

    def hitungOutput(self,arrData):
        self.y = np.matmul(arrData, self.bobot)+self.bias
        return self.y
    
    def updateBobot(self,arrData,target):
        bobotBaru = self.bobot + self.alfa * (target-self.y) * arrData
        biasBaru = self.bias + self.alfa * (target-self.y)
        return (bobotBaru,biasBaru)

    def fungsiyTest(self,v):
        if(v>=0):
            return 1
        else:
            return -1

    def testing(self,arrDataTesting):
        print("TESTING")
        print("bobot = "+str(self.bobot))
        print("bias = "+str(self.bias))
        target = self.getTarget()
        true = 0
        false = 0
        print ("-------------------------------")
        for i in range (len(arrDataTesting)) :
            print("Hasil Numeric Data Latih Huruf " + self.huruf[i] + " : ")
            print("data : "+ str(arrDataTesting[i]))
            print("target : " + str(target[i]))
            v = self.hitungOutput(arrDataTesting[i])
            print("v = " + str(v))
            yTest = self.fungsiyTest(v)
            print("yTest = " + str(yTest))
            print("Apakah y=target? ")
            if(target[i]==yTest):
                print("Sesuai")
                true +=1

            else:
                print("Tidak Sesuai")
                false +=1
            print ("-------------------------------")
            print ("-------------------------------")
        return(true,false)

    def akurasi(self,true,false):
        akurasi = (true/(true+false))*100
        return "hasil akurasi : "+str(akurasi)+" %"


    def training(self, arrData):
        maxBobot = 1
        epoch = 0
        while maxBobot > self.treshold :
            epoch += 1
            iterasi = 0
            arrbobot = []
            arrbobot.append(self.bobot)
            target = self.getTarget()
            print("alfa = " + str(self.alfa))
            print("treshold = " + str(self.treshold))
            for i in range (len(arrData)) :
                print("Hasil Numeric Data Latih Huruf " + self.huruf[i] + " : ")
                print("data : "+ str(arrData[i]))
                print("target : " + str(target[i]))
                print("bobot = " + str(self.bobot))  
                print("bias = " + str(self.bias))
                y=self.hitungOutput(arrData[i])
                print("y = " + str(y))
                self.bobot,self.bias = self.updateBobot(arrData[i],target[i])
                arrbobot.append(self.bobot)
                print("bobot = " + str(self.bobot))
                print("bias = " + str(self.bias))
                print ("-------------------------------")
                print ("-------------------------------")

            deltabobot = []
           
            for i in range(len(arrbobot)-1):
                arr = np.subtract(arrbobot[i+1],arrbobot[i])
                deltabobot.append(abs(arr[0]))
            print(str(deltabobot))
            maxBobot = np.amax(deltabobot)
            print('Max bobot epoch ke '+ str(epoch) + ' : ', maxBobot)

class Main():
    alfa = 0.25
    treshold = 0.4
    directoryTraining = "D:/Tania/UB/Semester 6/JST/Tugas/Tugas 2/train"

    adln = Adeline(alfa,treshold,25)
    dataTxt = adln.bacaFile(directoryTraining)
    arrData = adln.membuatArray(dataTxt)
    adln.training(arrData)


    directoryTesting = "D:/Tania/UB/Semester 6/JST/Tugas/Tugas 2/test"
    dataTesting = adln.bacaFile(directoryTesting)
    arrDataTesting =adln.membuatArray(dataTesting)
    true,false = adln.testing(arrDataTesting)
    print(adln.akurasi(true,false))