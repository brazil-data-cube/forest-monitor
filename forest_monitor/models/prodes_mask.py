from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Numeric, String, Date

from forest_monitor.models import BaseModel


class ProdesMask(BaseModel):
    __tablename__ = 'mascara_prodes'

    id = Column(Integer, primary_key=True)
    geom = Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True)
    origin_id = Column(Numeric)
    uf = Column(String(99))
    pathrow = Column(String(20))
    mainclass = Column(String(254))
    class_name = Column(String(254))
    dsfnv = Column(Numeric)
    julday = Column(Numeric)
    view_date = Column(Date)
    ano = Column(Numeric)
    areakm = Column(Numeric)
    scene_id = Column(Numeric)
    publish_ye = Column(String(29))
