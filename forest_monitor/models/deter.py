import datetime
from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, Numeric, String, Text
from forest_monitor.models import BaseModel


class Deter(BaseModel):
    __tablename__ = 'deter'

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
    car_imovel_id = Column(Text(2048))
    created_at = Column(Date,
                       default=datetime.date.today(),
                       onupdate=datetime.date.today())
    image_date = Column(Date)
