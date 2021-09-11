from marshmallow import fields, Schema, pre_dump


class CoordinatesSchema(Schema):
    datetime = fields.DateTime(attribute="datetime_at", format="iso8601")
    lat = fields.Float(attribute="latitude")
    lon = fields.Float(attribute="longitude")


class TrackSchema(Schema):
    uuid = fields.String(attribute="uuid")


class TrackCoordinateInfoSchema(Schema):
    begin_datetime = fields.String(allow_none=True, required=True)
    end_datetime = fields.String(allow_none=True, required=True)


class TrackSensorInfoSchema(Schema):
    begin_datetime = fields.String(allow_none=True, required=True)
    end_datetime = fields.String(allow_none=True, required=True)


class TrackInfoSchema(Schema):
    uuid = fields.String(attribute="uuid")
    coordinates = fields.Nested(TrackCoordinateInfoSchema, required=True)
    sensors = fields.Nested(TrackSensorInfoSchema, required=True)

    @pre_dump
    def group(self, data, many):
        return {
            "uuid": data.uuid,
            "coordinates": {
                "begin_datetime": data.datetime_min_coords,
                "end_datetime": data.datetime_max_coords
            },
            "sensors": {
                "begin_datetime": data.datetime_min_sens,
                "end_datetime": data.datetime_max_sens
            }
        }


class Accelerometer(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)


class Gyroscope(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)


class Magnetometer(Schema):
    x = fields.Float(allow_none=True, required=True)
    y = fields.Float(allow_none=True, required=True)
    z = fields.Float(allow_none=True, required=True)


class SensorsSchema(Schema):
    datetime = fields.String(allow_none=True, required=True)
    accelerometer = fields.Nested(Accelerometer, required=True)
    gyroscope = fields.Nested(Gyroscope, required=True)
    magnetometer = fields.Nested(Magnetometer, required=True)

    @pre_dump
    def group(self, data, many):
        return {
            "datetime": data.dt,
            "accelerometer": {
                "x": data.a_x,
                "y": data.a_y,
                "z": data.a_z
            },
            "gyroscope": {
                "x": data.g_x,
                "y": data.g_y,
                "z": data.g_z
            },
            "magnetometer": {
                "x": data.m_x,
                "y": data.m_y,
                "z": data.m_z
            }
        }


coordinates_schema = CoordinatesSchema(many=True)
sensors_schema = SensorsSchema(many=True)
uuid_schema = TrackSchema(many=True)
tracks_info_schema = TrackInfoSchema(many=True)
track_info_schema = TrackInfoSchema()
