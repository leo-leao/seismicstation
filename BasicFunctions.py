"""
    @Author: Leonardo Rossi Leao / Rodrigo de Oliveira Neto
    @Create: June 26, 2021
    @Title: Dat file monitor
"""

import os
from datetime import datetime, timedelta

class BasicFunctions:
    
    @staticmethod
    def getDatetime():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def recordAction(text):
        monitor = open("monitor.txt", "a")
        datetime = "[" + BasicFunctions.getDatetime() + "] "
        print(datetime + text + "\n")
        monitor.write(datetime + text + "\n")
        monitor.close()
        

class DatFunctions:
    
    @staticmethod
    def processFile(data, channel):
        seismicData = ""
        aSeismicData = []
        # Obtem as informacoes sobre a captacao de dados
        data = data.replace("$", "").split("\n")
        sampleRate = float(DatFunctions.getValue(data[3]))
        initialDate = DatFunctions.processDatetime(data[4])
        date = DatFunctions.processDatetime(data[4])
        bitWeight = float(DatFunctions.getValue(data[5]))
        # Processa os valores sismicos recebidos 
        for counts in data[9:len(data)-1]:
            speed = float(counts) * bitWeight / 800
            aSeismicData.append(speed)
            seismicData += str(datetime.timestamp(date)) + ": %.30f" % speed + "\n"
            date = date + timedelta(milliseconds = 1000/sampleRate)
        # Armazena os valores sismicos processados
        DatFunctions.recordData(initialDate, seismicData, channel)           
        
    @staticmethod
    def getValue(data):
        option, value = tuple(data.replace(" ", "").split("="))
        return value
    
    @staticmethod
    def processDatetime(date):
        date = DatFunctions.getValue(date)
        year, day, hour, minutes, seconds, ms = tuple(date.replace(".", ":").split(":"))
        dt = datetime(int(year), 1, 1) + timedelta(int(day) - 1)
        return datetime(dt.year, dt.month, dt.day, int(hour), int(minutes), int(seconds), int(ms)*100)
    
    @staticmethod
    def howToRecord(date):
        year = date.year
        day = (date - datetime(year, 1, 1)).days + 1
        hour = date.hour
        return (year, day, str(hour) + ".txt")
    
    @staticmethod
    def recordData(date, seismic, channel):
        pathIn = "/home/reftek/bin/archive/SeismicData/"
        # pathIn = "C:/Users/ASUS/Desktop/SeismicData/"
        path = (pathIn + "%s/%s/" + channel + "/%s") % DatFunctions.howToRecord(date)
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, "a") as file:
            file.write(seismic)
        file.close()
    
    
    
    
    