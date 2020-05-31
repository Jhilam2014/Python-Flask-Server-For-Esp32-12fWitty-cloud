import re
import numpy as np
import keras.backend.tensorflow_backend as tb
class dataProcessing:
    
    def __init__(self,ml):
        self.model = ml
    def regxProcess(self,data):
        regex = r"[\d|\-]{1,}\.[\d]{2}"
        matches = re.findall(regex, data, re.MULTILINE)
        return matches
        
    def sensorMotionData(self,rawData,typ):
        collectData = []
        for each in rawData:
            collectData.extend(each[typ])
        x = [];y = [];z = []
        pkg=[]
        for each in collectData:
            eachAxisData = self.regxProcess(each)
            x.append(eachAxisData[0])
            y.append(eachAxisData[1])
            z.append(eachAxisData[2])
            pkg.append([eachAxisData[0],eachAxisData[1],eachAxisData[2]])
        ts = np.array([pkg])
        tb._SYMBOLIC_SCOPE.value = True
        ind = np.argmax(self.model.predict(ts))
        return [[x,y,z],ind]

    def sensorMotionDatForAssist(self,rawData,typ):
        collectData = []
        for each in rawData:
            collectData.extend(each[typ])

        pkg=[]
        for each in collectData:
            eachAxisData = self.regxProcess(each)
            pkg.append([eachAxisData[0],eachAxisData[1],eachAxisData[2]])
        ts = np.array([pkg])
        tb._SYMBOLIC_SCOPE.value = True
        ind = np.argmax(self.model.predict(ts))
        return ind

 

        






