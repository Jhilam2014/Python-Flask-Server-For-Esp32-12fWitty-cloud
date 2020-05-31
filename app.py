from flask import Flask,jsonify,render_template,request
import requests
try:
    from ConfigParser import SafeConfigParser
except:
    from six.moves.configparser import SafeConfigParser
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from utilities import dataProcessing
import os,sys
import keras

# print(os.system('which python'))
ml=keras.models.load_model("extra/model/model.h5")

app = Flask(__name__)

parser = SafeConfigParser()
parser.read('config.ini')
LOCALADDRESS = parser.get('setup', 'LOCAL_ADDRESS')
PORTPI = int(parser.get('setup', 'PORT_PI'))
GET_COOD = parser.get('api','GET_COOD')
RNG = parser.get('variable','RNG')

fig = plt.figure()
axis = fig.add_subplot(1,1,1)

dProcess = dataProcessing(ml)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/api/voice_assist/get_gyro', methods=['GET'])
def getGyroDataForAssist():
    URL = LOCALADDRESS+GET_COOD
    payload  = {}
    headers = {
        'Content-Type': 'application/json'
    }
    jsonData = []
    for each in range(0,int(RNG)):
        try:
            res = requests.get(url=URL, headers=headers,data = payload,verify=False, timeout=2)
            if(res.status_code == 200):
                jsonData.append(res.json())
            else:
                jsonData.append(res.status_code)
        except:
            # print(error)
            jsonData=None
            return jsonify({"Status":jsonData})

    if jsonData:
        gyroData = dProcess.sensorMotionDatForAssist(jsonData,'gyroData')
    return jsonify({"Type":gyroData})

@app.route('/api/gyro', methods=['GET'])
def getGyroData():
    URL = LOCALADDRESS+GET_COOD
    payload  = {}
    headers = {
        'Content-Type': 'application/json'
    }
    jsonData = []
    for each in range(0,int(RNG)):
        try:
            res = requests.get(url=URL, headers=headers,data = payload,verify=False, timeout=2)
            if(res.status_code == 200):
                jsonData.append(res.json())
            else:
                jsonData.append(res.status_code)
        except:
            # print(error)
            jsonData=None
            return jsonify({"Status":jsonData})

    if jsonData:
        gyroData = dProcess.sensorMotionData(jsonData,'gyroData')
    return jsonify({"Status":gyroData[0], "Type":gyroData[1]})

status = 1

@app.route('/api/condition', methods=['GET'])
def trigger():
    global status
    getGtatus = request.args.get('status')
    if getGtatus=="on":
        status = 1
    elif getGtatus=="off":
        status = 0
    else:
        status = status
    return jsonify({"Status":status})

if __name__ == '__main__':
    app.run(debug=True, port=PORTPI, host='0.0.0.0') 