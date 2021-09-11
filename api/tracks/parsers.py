from marshmallow import Schema, fields
from datetime import datetime


class CoordinateSchema(Schema):
    datetime = fields.DateTime(attribute="datetime_at", format="iso8601",
                               required=True)
    lat = fields.Float(attribute="latitude", required=True)
    lon = fields.Float(attribute="longitude", required=True)


class CoordinatesSchema(Schema):
    coordinates = fields.List(fields.Nested(CoordinateSchema), required=True)


class TrackSchema(Schema):
    uuid = fields.String(attribute="track_uuid")


class CoordinatesQuerySchema(Schema):
    begin_datetime = fields.DateTime(format="iso8601", missing=datetime.min)
    end_datetime = fields.DateTime(format="iso8601", missing=datetime.utcnow)


class SensorsQuerySchema(Schema):
    begin_datetime = fields.DateTime(format="iso8601", missing=datetime.min)
    end_datetime = fields.DateTime(format="iso8601", missing=datetime.utcnow)
