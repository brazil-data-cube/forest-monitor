from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Column, Integer, Numeric, String

from forest_monitor.models import BaseModel


class Prodes(BaseModel):
    __tablename__ = 'prodes_2019_area_maiores_50ha_area_teste'

    id = Column(Integer, primary_key=True)
    geom = Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True)
    object_id = Column(Numeric)
    cell_oid = Column(String(254))
    class_name = Column(String(254))
    ai_object = Column(String(254))
    areaha = Column(Numeric)
    id_2 = Column(BigInteger)
    nome_area = Column(String(60))
