"""
    @Author: Leonardo Rossi Leao / Rodrigo de Oliveira Neto
    @Create: June 26, 2021
    @Title: Dat file monitor
"""

# Libraries
import os, time, threading
from datetime import datetime
from BasicFunctions import BasicFunctions
from BasicFunctions import DatFunctions

class DatMonitor(threading.Thread):
    
    def __init__(self):
        super(DatMonitor, self).__init__()
        self.kill = threading.Event()
        self.pathIn = "/home/reftek/bin/archive/seismicstation/"
        # self.pathIn = "C:/Users/ASUS/Desktop/ArchiverScripts/"
        
    def searchFiles(self):
        arquivos = set(os.listdir(self.pathIn))
        return arquivos
    
    def run(self):
        while not self.kill.is_set():
            content = self.searchFiles()
            for filename in content:
                if ".atr" in filename:
                    try:
                        BasicFunctions.recordAction("DAT: file founded")
                        file = open(self.pathIn + filename, "r")
                        data = file.read()
                        file.close()
                        DatFunctions.processFile(data, filename[-5])
                        os.remove(self.pathIn + filename)
                        BasicFunctions.recordAction("DAT: channel %s | concluded"  % filename[-5])
                    except:
                        print("Ocorreu um erro!")
            time.sleep(0.5) 
            
class RawMonitor(threading.Thread):
    
    def __init__(self):
        super(RawMonitor, self).__init__()
        self.kill = threading.Event()
        self.pathIn = "/home/reftek/bin/archive/"
        # self.pathIn = "C:/Users/ASUS/Desktop/archive/"
        self.pathCvt = self.pathIn + "pas2asc"
        
    def searchFiles(self):
        today = DatFunctions.howToRecord(datetime.now())
        path = "%s%d%d/B67D/1/" % (self.pathIn, today[0], today[1])
        files = set(os.listdir(path))
        return (path, files)
    
    def convertion(self, path, newFile):
        for file in newFile:
            pathIn = path + file
            if "_00000000" not in pathIn:
                os.system(self.pathCvt + " -Ln " + pathIn)
                os.remove(pathIn)
                BasicFunctions.recordAction("RAW: file converted to DAT")
                
    def run(self):
        BasicFunctions.recordAction("RAW: start raw monitor")
        path, content = self.searchFiles()
        while not self.kill.is_set():
            path, newContent = self.searchFiles()
            newFile = newContent.difference(content)
            if newFile:
                BasicFunctions.recordAction("RAW: file founded")
                self.convertion(path, newFile)
            content = newContent
            time.sleep(0.5)
            
if __name__ == "__main__":
    threadRM = RawMonitor()
    threadRM.start()
    threadDM = DatMonitor()
    threadDM.start()