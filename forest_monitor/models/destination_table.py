import datetime
from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, Numeric, String, Text
from forest_monitor.models import BaseModel
from forest_monitor.config import getCurrentConfig
import json
from geoalchemy2 import functions

appConfig = getCurrentConfig()

destinationTable = appConfig.DESTINATION_TABLE
maskTable = appConfig.MASK_TABLE_DETER

class DestinationTable(BaseModel):
    __tablename__ = destinationTable

    id = Column(Integer, primary_key=True)
    geom = Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True)
    classname = Column(String(254))
    quadrant = Column(String(5))
    path_row = Column(String(10))
    view_date = Column(Date)
    sensor = Column(String(10))
    satellite = Column(String(13))
    areauckm = Column(Numeric)
    uc = Column(String(254))
    areamunkm = Column(Numeric)
    municipali = Column(String(254))
    uf = Column(String(2))

    scene_id = Column(String(254))
    source = Column(String(2))
    user_id = Column(String(254))
    ncar_ids = Column(Integer)
    car_imovel = Column(Text(2048))
    created_at = Column(Date,
                       default=datetime.date.today(),
                       onupdate=datetime.date.today())
    image_date = Column(Date)
    def getFeature(self):
        feature = {
            "tablename": self.__tablename__,
            "id": self.id,
            "classname": self.classname,
            "quadrant": self.quadrant,
            "path_row": self.path_row,
            "view_date": self.view_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "sensor": self.sensor,
            "satellite": self.satellite,
            "areauckm": str(self.areauckm),
            "uc": self.uc,
            "areamunkm": str(self.areamunkm),
            "municipali": self.municipali,
            "uf": self.uf,
            "scene_id": self.scene_id,
            "source": self.source,
            "user_id": self.user_id,
            "ncar_ids": self.ncar_ids,
            "car_imovel": self.car_imovel,
            "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "image_date": self.image_date.strftime("%m/%d/%Y, %H:%M:%S")
        }
        
        return feature

class MaskTable(BaseModel):
    __tablename__ = maskTable
    id = Column(Integer, primary_key=True)
    geom = Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True)
    classname = Column(String(254))
    quadrant = Column(String(5))
    path_row = Column(String(10))
    view_date = Column(Date)
    sensor = Column(String(10))
    satellite = Column(String(13))
    areauckm = Column(Numeric)
    uc = Column(String(254))
    areamunkm = Column(Numeric)
    municipali = Column(String(254))
    uf = Column(String(2))

    scene_id = Column(String(254))
    source = Column(String(2))
    user_id = Column(String(254))
    ncar_ids = Column(Integer)
    car_imovel = Column(Text(2048))
    created_at = Column(Date,
                       default=datetime.date.today(),
                       onupdate=datetime.date.today())
    image_date = Column(Date)

