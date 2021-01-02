from flask import json, jsonify, Response, request, Flask
from ORM import Datarequest
from datetime import datetime
from systemd.journal import JournaldLogHandler
import logging
from os import getenv
from systemd.journal import JournaldLogHandler

DB_URL = getenv("DB_URL")

app = Flask(__name__)
DB = Datarequest(DB_URL)

logger = logging.getLogger("REST - sgp 30")
journald_handler = JournaldLogHandler()
journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)

@app.route('/',methods=['POST'])
def standard():
    return Response(status=200)
@app.route('/ESP/PUSH_DATA', methods=['POST'])
def storeData():
    if request.headers['Content-Type'] == 'application/json':
        logger.debug("JSON: {}".format(request.get_data()))
        temperature = request.get_json()['temperature']
        eCO2        = request.get_json()['eCO2']
        raw_Ethanol = request.get_json()['raw_Ethanol']
        raw_H2      = request.get_json()['raw_H2']
        pressure    = request.get_json()['pressure']
        humidity    = request.get_json()['humidity']
        TVOC        = request.get_json()['TVOC']
        sensor_id   = int(request.get_json()['mac_addr'].replace(":",""), 16)
        try:
            DB.DatenEinfuegen([
                                temperature,
                                eCO2,
                                raw_Ethanol,
                                raw_H2,
                                pressure,
                                humidity,
                                TVOC,
                                sensor_id
                                ])
        except Exception as err:
            logger.error(err)
            return Response(status=503)
        else:
            return Response(status=200)
    else: return Response(status=415)
    

if __name__ == "__main__":
    app.run()