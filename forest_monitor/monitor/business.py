import datetime
from json import dumps as json_dumps

from sqlalchemy import text

from forest_monitor.config import getCurrentConfig
from forest_monitor.models.base_sql import getDatabase


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
            
            try:
                db = getDatabase()

                connection = db.connect().execution_options(autocommit=True)

                geom = feature
                geom['coordinates'] = [coord]

                sql = text('''
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
                                :uf AS uf, st_multi(st_collectionextract(st_makevalid(geom),3)), :scene_id AS scene_id, :source AS source,
                                :user_id AS user_id, :created_at as created_at, :image_date AS image_date, :project AS project
                        FROM result
                ''')

                values['geom'] = json_dumps(geom)
                connection.execute(sql, geom=json_dumps(geom), classname=values['classname'], quadrant=values['quadrant'], path_row=values['path_row'], view_date=values['view_date'], sensor=values['sensor'], satellite=values['satellite'], areauckm=values['areauckm'], uc=values['uc'], areamunkm=values['areamunkm'], municipali=values['municipali'], uf=values['uf'], scene_id=values['scene_id'], source=values['source'], user_id=values['user_id'], created_at=values['created_at'], image_date=values['image_date'], project=values['project'])

            except Exception as err:

                print("Original Exception Message: ", err)
                raise Exception("Failed inserting Feature on Forest Monitor Database.")

            finally:
                connection.close()
                db.dispose()


            

    @classmethod
    def get(cls,feature_id):

        appConfig = getCurrentConfig()

        destinationTable = appConfig.DESTINATION_TABLE

        try:

            db = getDatabase()
            connection = db.connect()

            sql = text('''select * from ''' + destinationTable +''' 
            where id= :id and source= :source''')

            features = connection.execute(sql, id=feature_id, source='M')

            for row in features:
                feature = {
                    "id": row['id'],
                    "classname": row['classname'],
                    "quadrant": row['quadrant'],
                    "path_row": row['path_row'],
                    "view_date": row['view_date'].strftime("%m/%d/%Y, %H:%M:%S"),
                    "sensor": row['sensor'],
                    "satellite": row['satellite'],
                    "areauckm": str(row['areauckm']),
                    "uc": row['uc'],
                    "areamunkm": str(row['areamunkm']),
                    "municipali": row['municipali'],
                    "uf": row['uf'],
                    "scene_id": row['scene_id'],
                    "source": row['source'],
                    "user_id": row['user_id'],
                    "ncar_ids": row['ncar_ids'],
                    "car_imovel": row['car_imovel'],
                    "created_at": row['created_at'].strftime("%m/%d/%Y, %H:%M:%S"),
                    "image_date": row['image_date'].strftime("%m/%d/%Y, %H:%M:%S")
                }
                return feature

        except Exception as err:

            print("Original Exception Message: ", err)
            raise Exception('Failed finding the requested Feature on Forest Monitor Database.')

        finally:
            connection.close()
            db.dispose()
                   

    @classmethod
    def update(cls, values, feature_id):

        appConfig = getCurrentConfig()

        destinationTable = appConfig.DESTINATION_TABLE

        try:


            db = getDatabase()
            connection = db.connect()

            sql = text('''update ''' + destinationTable + ''' set 
            classname= :classname,
            view_date= :view_date,
            path_row= :path_row,
            satellite= :satellite,
            sensor= :sensor,
            scene_id= :scene_id,
            image_date= :image_date
            where id= :id ''')

            connection.execute(sql, id=feature_id,classname=values["classname"], view_date=values["view_date"], path_row=values["path_row"], satellite=values["satellite"], sensor=values["sensor"], scene_id=values["scene_id"], image_date=values["image_date"])
            

        except Exception as err:
            print("Original Exception Message: ", err)
            db.rollback()
            raise Exception('Failed updating the requested Feature on Forest Monitor Database.')

        finally:
            connection.close()
            db.dispose()

    @classmethod
    def updateGeom(cls, values, feature_id):

        appConfig = getCurrentConfig()

        destinationTable = appConfig.DESTINATION_TABLE

        try:

            feature = {
                'coordinates': [values['edited_geom']['features'][0]['geometry']['coordinates']],
                'type': 'MultiPolygon'
            }
            db = getDatabase()
            connection = db.connect()

            values['edited_geom'] = json_dumps(feature)

            sql = text('''update ''' + destinationTable + ''' set 
            geom= ST_setSRID(ST_GeomFromGeoJson(:geom), 4326)
            where id= :id ''')

            connection.execute(sql, id=feature_id, geom=values["edited_geom"])


        except Exception as err:
            print("Original Exception Message: ", err)
            db.rollback()
            raise Exception('Failed updating the requested Feature on Forest Monitor Database.')

        finally:
            connection.close()
            db.dispose()

    @classmethod
    def delete(cls, feature_id):
        
        appConfig = getCurrentConfig()

        destinationTable = appConfig.DESTINATION_TABLE

        try:

            db = getDatabase()
            connection = db.connect()

            sql = text('delete from ' + destinationTable +' where id= :id and source= :source')

            print(sql)
            connection.execute(sql, id=feature_id, source='M')                        

        except Exception as err:
            print("Original Exception Message: ", err)
            raise Exception('Failed deleting the requested Feature on Forest Monitor Database.')
        
        finally:
            connection.close()
            db.dispose()

