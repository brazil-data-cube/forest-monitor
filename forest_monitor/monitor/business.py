import datetime
from json import dumps as json_dumps
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from forest_monitor.models.base_sql import db
from forest_monitor.models.destination_table import DestinationTable
from forest_monitor.config import getCurrentConfig


class FeatureBusiness:
    @classmethod
    def add(cls, values, user_id=None):
        """
        Add a feature to database

        Args:
            values (dict): Values to insert in database
            user_id (str or None): User identifier

        """

        appConfig = getCurrentConfig()

        destinationTable = appConfig.DESTINATION_TABLE
        maskTableDeter = appConfig.MASK_TABLE_DETER
        maskTableProdes = appConfig.MASK_TABLE_PRODES

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
                    ), result_''' + maskTableDeter + '''_intersection AS (
                        SELECT ST_Union(''' + maskTableDeter + '''.geom) AS geom
                        FROM ''' + maskTableDeter + ''', converted_geom
                        WHERE ST_Intersects(''' + maskTableDeter + '''.geom, converted_geom.geom) AND ''' + maskTableDeter + '''.source <> 'S' 
                    ), result_''' + destinationTable + '''_intersection AS (
                        SELECT ST_Union(''' + destinationTable + '''.geom) AS geom
                        FROM ''' + destinationTable + ''', converted_geom
                        WHERE ST_Intersects(''' + destinationTable + '''.geom, converted_geom.geom) AND ''' + destinationTable + '''.source <> 'S' 
                    ), result_mask_intersection AS (
                        SELECT ST_Union(mask.geom) AS geom
                        FROM ''' + maskTableProdes + ''' AS mask, converted_geom
                        WHERE ST_Intersects(mask.geom, converted_geom.geom)
                    ), result_collect AS (
                        SELECT  ST_Union(
                                    ARRAY[
                                        mask.geom,
                                        ''' + maskTableDeter + '''.geom,
                                        ''' + destinationTable + '''.geom
                                    ]
                                ) AS geom
                        FROM result_mask_intersection AS mask,
                            result_''' + maskTableDeter + '''_intersection AS ''' + maskTableDeter + ''',
                            result_''' + destinationTable + '''_intersection AS ''' + destinationTable + '''
                    ), result AS (
                        SELECT ST_Difference(converted_geom.geom, coalesce(r.geom, ST_SetSRID('GEOMETRYCOLLECTION EMPTY'::geometry, 4326))) AS geom
                        FROM converted_geom, result_collect r
                    )
                    INSERT INTO ''' + destinationTable + ''' (classname, quadrant, path_row, view_date, sensor,
                                    satellite, areauckm, uc, areamunkm, municipali,
                                    uf, geom, scene_id, source, user_id, created_at, image_date, project)
                        SELECT :classname AS classname, :quadrant AS quadrant,
                                :path_row AS path_row, :view_date AS view_date, :sensor AS sensor,
                                :satellite AS satellite, :areauckm AS areauckm,
                                :uc AS uc, :areamunkm AS areamunkm, :municipali AS municipali,
                                :uf AS uf, ST_Multi(geom), :scene_id AS scene_id, :source AS source,
                                :user_id AS user_id, :created_at as created_at, :image_date AS image_date, :project AS project
                        FROM result
                ''')

                values['geom'] = json_dumps(geom)
                db.session.execute(statement, params=values)
            db.session.commit()

    
    @classmethod
    def get(cls,feature_id):
        with db.session.begin_nested():
            try:
                feature = db.session.query(DestinationTable).filter_by(id=feature_id, source='M').one()
                
                return feature
            except NoResultFound:
                raise NotFound('Feature "{}" not found or cannot be replacee.'.format(feature_id))

        db.session.commit()

    @classmethod
    def update(cls, values, feature_id):
        with db.session.begin_nested():
               try:

                feature = db.session.query(DestinationTable).filter_by(id=feature_id, source='M').one()
                feature.classname=values["classname"]
                feature.view_date=values["view_date"]
                feature.path_row=values["path_row"]
                feature.satellite=values["satellite"]
                feature.sensor=values["sensor"]
                feature.scene_id=values["scene_id"]
                feature.image_date=values["image_date"]

               except NoResultFound:
                raise NotFound('Feature "{}" not found or cannot be replacee.'.format(feature_id))
        db.session.commit()              

    @classmethod
    def delete(cls, feature_id):
        with db.session.begin_nested():
             
            try:
                feature = db.session.query(DestinationTable).filter_by(id=feature_id, source='M').one()
                print(feature)
                db.session.delete(feature)

            except NoResultFound:
                raise NotFound('Feature "{}" not found or cannot be removed.'.format(feature_id))

        db.session.commit()

  