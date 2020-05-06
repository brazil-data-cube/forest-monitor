import datetime
from json import dumps as json_dumps
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from forest_monitor.models.base_sql import db
from forest_monitor.models.deter import DeterD
from forest_monitor.models.deter import DeterM

class FeatureBusiness:
    @classmethod
    def add(cls, values, user_id=None):
        """
        Add a feature to database

        Args:
            values (dict): Values to insert in database
            user_id (str or None): User identifier

        """
        values['scene_id'] = values.get('scene_id', '')
        values['user_id'] = user_id
        values['source'] = 'M'
        values['created_at'] = datetime.date.today()

        feature = {
            'coordinates': [],
            'type': values['geom']['features'][0]['geometry']['type']
        }
        for coord in values['geom']['features'][0]['geometry']['coordinates']:
            with db.session.begin_nested():
                geom = feature
                geom['coordinates'] = [coord]

                statement = text('''
                    WITH converted_geom as (
                        SELECT ST_setSRID(ST_GeomFromGeoJson(:geom), 4326) AS geom
                    ), result_deter_d_intersection AS (
                        SELECT ST_Union(deter_d.geom) AS geom
                        FROM deter_d, converted_geom
                        WHERE ST_Intersects(deter_d.geom, converted_geom.geom)
                    ), result_deter_m_intersection AS (
                        SELECT ST_Union(deter_m.geom) AS geom
                        FROM deter_m, converted_geom
                        WHERE ST_Intersects(deter_m.geom, converted_geom.geom)
                    ), result_mask_intersection AS (
                        SELECT ST_Union(mask.geom) AS geom
                        FROM mascara_prodes AS mask, converted_geom
                        WHERE ST_Intersects(mask.geom, converted_geom.geom)
                    ), result_collect AS (
                        SELECT  ST_Union(
                                    ARRAY[
                                        mask.geom,
                                        deter_d.geom,
                                        deter_m.geom
                                    ]
                                ) AS geom
                        FROM result_mask_intersection AS mask,
                            result_deter_d_intersection AS deter_d,
                            result_deter_m_intersection AS deter_m
                    ), result AS (
                        SELECT ST_Difference(converted_geom.geom, coalesce(r.geom, ST_SetSRID('GEOMETRYCOLLECTION EMPTY'::geometry, 4326))) AS geom
                        FROM converted_geom, result_collect r
                    )
                    INSERT INTO deter_m (classname, quadrant, path_row, view_date, sensor,
                                    satellite, areauckm, uc, areamunkm, municipali,
                                    uf, geom, scene_id, source, user_id, created_at, image_date)
                        SELECT :classname AS classname, :quadrant AS quadrant,
                                :path_row AS path_row, :view_date AS view_date, :sensor AS sensor,
                                :satellite AS satellite, :areauckm AS areauckm,
                                :uc AS uc, :areamunkm AS areamunkm, :municipali AS municipali,
                                :uf AS uf, ST_Multi(geom), :scene_id AS scene_id, :source AS source,
                                :user_id AS user_id, :created_at as created_at, :image_date AS image_date
                        FROM result
                ''')

                values['geom'] = json_dumps(geom)
                db.session.execute(statement, params=values)
            db.session.commit()

    @classmethod
    def delete(cls, feature_id):
        with db.session.begin_nested():
            try:
                feature = db.session.query(DeterM).filter_by(id=feature_id, source='M').one()

                db.session.delete(feature)
            except NoResultFound:
                raise NotFound('Feature "{}" not found or cannot be removed.'.format(feature_id))

        db.session.commit()