import datetime
from geoalchemy2 import Geometry
from sqlalchemy import Column, Date, Integer, Numeric, String, Text
from forest_monitor.models import BaseModel, getDatabase
from forest_monitor.config import getCurrentConfig
from sqlalchemy.orm import sessionmaker

appConfig = getCurrentConfig()

destinationTable = appConfig.DESTINATION_TABLE
maskTable = appConfig.MASK_TABLE_DETER
prodesMaskTable = appConfig.MASK_TABLE_PRODES

development = appConfig.DEVELOPMENT


class DestinationTable(BaseModel):
    __tablename__ = destinationTable

    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
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
    created_at = Column(Date, default=datetime.date.today(), onupdate=datetime.date.today())
    image_date = Column(Date)
    ncar_ids = Column(Integer)
    car_imovel = Column(String(2048))
    continuo = Column(Integer)
    velocidade = Column(Numeric)
    porc_agreg = Column(Numeric)
    deltad = Column(Integer)
    car_duplo = Column(Integer)
    project = Column(Text())

class MaskTable(BaseModel):
    __tablename__ = maskTable
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True))
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
    created_at = Column(Date, default=datetime.date.today(), onupdate=datetime.date.today())
    image_date = Column(Date)
    ncar_ids = Column(Integer)
    car_imovel = Column(String(2048))
    continuo = Column(Integer)
    velocidade = Column(Numeric)
    porc_agreg = Column(Numeric)
    deltad = Column(Integer)
    car_duplo = Column(Integer)
    project = Column(Text())


class ProdesMaskTable(BaseModel):
    __tablename__ = prodesMaskTable
    tid = Column(Integer)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True))
    id = Column(Integer, primary_key=True)
    uf = Column(String(99))
    mainclass = Column(String(254))
    class_name = Column(String(254))
    dsfnv = Column(Numeric)
    julday = Column(Numeric)
    view_date = Column(Date)
    ano = Column(Numeric)
    scene_id = Column(Numeric)
    aream2 = Column(Numeric)


if development:
    Session = sessionmaker()
    database = getDatabase()
    session = Session(bind=database)
    BaseModel.metadata.create_all(bind=database)
    session.close()
