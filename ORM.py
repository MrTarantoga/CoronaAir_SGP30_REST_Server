import os, datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import logging
import time
from systemd.journal import JournaldLogHandler
from threading import Lock

class NoDBException(Exception):
    def __init__(self,Path):
        self.Path = Path
    def __str__(self):
        return "Path to Database does not exists: {}".format(self.Path)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Sensor_Value(declarative_base()):
    __tablename__ = "sgp_30"

    id          = Column(Integer, primary_key=True)
    sensor_id   = Column(Integer)
    temperature = Column(Float)
    eCO2        = Column(Integer)
    raw_Ethanol = Column(Integer)
    raw_H2      = Column(Integer)
    pressure    = Column(Float)
    humidity    = Column(Float)
    TVOC        = Column(Integer)
    timestamp   = Column(DateTime(timezone=True), default=func.now())

class Datarequest(metaclass=Singleton):

    def __init__(self, DB_URL: str):
        self.conc_lock = Lock()
        self.engine = create_engine(DB_URL)
        self.logger = logging.getLogger("ORM - sgp 30")
        self.journald_handler = JournaldLogHandler()
        self.journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(self.journald_handler)
        self.logger.setLevel(logging.DEBUG)

    def DatenEinfuegen(self,values):
        self.conc_lock.acquire()
        self.logger.debug("temperature: " + str(values[0]) + " eCO2: " + str(values[1]) + " Ethanol: " + str(values[2]) + " H2: " + str(values[3]) + " Pressure: " + str(values[4]) + " Humidity: " + str(values[5]) + " TVOC: " + str(values[6]) + " Sensor id:" + str(values[7]))
        dataset = Sensor_Value(
                                sensor_id   = values[7],
                                temperature = values[0],
                                eCO2        = values[1],
                                raw_Ethanol = values[2],
                                raw_H2      = values[3],
                                pressure    = values[4],
                                humidity    = values[5],
                                TVOC        = values[6]
        )
        session = sessionmaker(bind=self.engine)()
        session.add(dataset)
        session.commit()
        session.close()
        self.conc_lock.release()
        