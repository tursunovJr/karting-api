from flask import request
from flask_restful import Resource, abort, url_for
from marshmallow import ValidationError
from sqlalchemy.sql import func
from api.tracks.parsers import CoordinatesSchema, CoordinatesQuerySchema,\
    SensorsQuerySchema
from api.tracks.fields import coordinates_schema, sensors_schema,\
    tracks_info_schema, track_info_schema
from api.tracks.models import Coordinate, Sensor, Track
from api.utils import make_response, make_empty
from extensions import db
from sqlalchemy import exc
from datetime import datetime


# todo: Add Resource
class Tracks(Resource):
    @staticmethod
    def get():
        """Получить список маршрутов"""

        tracks = db.session.query(Track.uuid.label("uuid"),
                                  func.max(func.ifnull(Coordinate.datetime_at,
                                                       None))
                                  .label("datetime_max_coords"),
                                  func.min(func.ifnull(Coordinate.datetime_at,
                                                       None))
                                  .label("datetime_min_coords"),
                                  func.max(func.ifnull(Sensor.datetime_at,
                                                       None))
                                  .label("datetime_max_sens"),
                                  func.min(func.ifnull(Sensor.datetime_at,
                                                       None))
                                  .label("datetime_min_sens"))\
            .outerjoin(Coordinate, Track.uuid == Coordinate.track_uuid)\
            .outerjoin(Sensor, Track.uuid == Sensor.track_uuid)\
            .group_by(Track.uuid)\
            .all()

        return make_response(200, tracks=tracks_info_schema.dump(tracks))

    @staticmethod
    def post():
        """Создать новый маршрут"""

        track = Track()
        db.session.add(track)
        db.session.commit()
        location_url = url_for("api.track_info", track_uuid=track.uuid)
        resp = make_response(201, location=location_url)
        resp.headers["Location"] = location_url
        return resp


class TrackInfo(Resource):
    @staticmethod
    def get(track_uuid):
        """Получить информацию о маршруте"""

        track_info = db.session.query(Track.uuid.label("uuid"), func.max(
            func.ifnull(Coordinate.datetime_at, None))
                                      .label("datetime_max_coords"), func.min(
            func.ifnull(Coordinate.datetime_at, None))
                                      .label("datetime_min_coords"), func.max(
            func.ifnull(Sensor.datetime_at, None))
                                      .label("datetime_max_sens"), func.min(
            func.ifnull(Sensor.datetime_at, None))
                                      .label("datetime_min_sens"))\
            .outerjoin(Coordinate, Track.uuid == Coordinate.track_uuid) \
            .outerjoin(Sensor, Track.uuid == Sensor.track_uuid) \
            .filter(Track.uuid.like(str(track_uuid)))\
            .one_or_none()

        if track_info is None or track_info.uuid is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        return make_response(200, **track_info_schema.dump(track_info))


class Coordinates(Resource):
    @staticmethod
    def post(track_uuid):
        """Добавить координаты в маршрут"""

        if db.session.query(Track).filter(Track.uuid.like(str(track_uuid)))\
                .one_or_none() is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        try:
            args = CoordinatesSchema().load(request.json)
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        for coord_data in args["coordinates"]:
            coordinate = Coordinate(track_uuid=str(track_uuid), **coord_data)
            try:
                db.session.add(coordinate)
            except exc.SQLAlchemyError:
                db.session.rollback()
                return make_response(500, message="Database add error")

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(201)

    @staticmethod
    def get(track_uuid):
        """Получить список координат маршрута"""

        # todo: Убрать или добавить проверку в основной запрос
        if db.session.query(Track).filter(Track.uuid.like(str(track_uuid)))\
                .one_or_none() is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        query = CoordinatesQuerySchema().load(request.args)
        coords = db.session\
            .query(Coordinate)\
            .filter(
                Coordinate.track_uuid.like(str(track_uuid)),
                Coordinate.datetime_at.between(query["begin_datetime"],
                                               query["end_datetime"])
            )\
            .order_by(Coordinate.datetime_at)\
            .all()

        if coords is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        return make_response(200, coordinates=coordinates_schema.dump(coords))


class Sensors(Resource):
    @staticmethod
    def post(track_uuid):
        """Добавить показания датчиков"""

        if db.session.query(Track).filter(Track.uuid.like(str(track_uuid)))\
                .one_or_none() is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        # todo: Upgrade parsing->Update 400 error
        args = request.json
        if len(args) == 0:
            return make_response(400, message="Bad JSON format")
        for sensors_data in args["sensors"]:
            sensor = Sensor(
                track_uuid=str(track_uuid),
                datetime_at=datetime.strptime(sensors_data["datetime"],
                                              "%Y-%m-%d %H:%M:%S.%f"),
                accelerometerX=sensors_data["accelerometer"][0],
                accelerometerY=sensors_data["accelerometer"][1],
                accelerometerZ=sensors_data["accelerometer"][2],
                gyroscopeX=sensors_data["gyroscope"][0],
                gyroscopeY=sensors_data["gyroscope"][1],
                gyroscopeZ=sensors_data["gyroscope"][2],
                magnetometerX=sensors_data["magnetometer"][0],
                magnetometerY=sensors_data["magnetometer"][1],
                magnetometerZ=sensors_data["magnetometer"][2],
            )
            try:
                db.session.add(sensor)
            except exc.SQLAlchemyError:
                db.session.rollback()
                return make_response(500, message="Database add error")

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(201)

    @staticmethod
    def get(track_uuid):
        """Получить список показаний датчиков"""

        if db.session.query(Track).filter(Track.uuid.like(str(track_uuid)))\
                .one_or_none() is None:
            abort(404, message="Track with uuid={} not found"
                  .format(track_uuid))

        query = SensorsQuerySchema().load(request.args)
        sens = db.session.query(Sensor.datetime_at.label("dt"),
                                Sensor.accelerometerX.label("a_x"),
                                Sensor.accelerometerY.label("a_y"),
                                Sensor.accelerometerZ.label("a_z"),
                                Sensor.gyroscopeX.label("g_x"),
                                Sensor.gyroscopeY.label("g_y"),
                                Sensor.gyroscopeZ.label("g_z"),
                                Sensor.magnetometerX.label("m_x"),
                                Sensor.magnetometerY.label("m_y"),
                                Sensor.magnetometerZ.label("m_z"),)\
            .filter(
            Sensor.track_uuid.like(str(track_uuid)),
            Sensor.datetime_at.between(query["begin_datetime"],
                                       query["end_datetime"])) \
            .order_by(Sensor.datetime_at)\
            .all()

        return make_response(200, sensors=sensors_schema.dump(sens))
