from extensions import db
from uuid import uuid4
from datetime import datetime


class Track(db.Model):
    uuid = db.Column(db.String(36), primary_key=True,
                     default=lambda: str(uuid4()))


class Coordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_uuid = db.Column(db.String(36), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    datetime_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return "<Coordinate: latitude={}, longitude={}, datetime=\"{}\">\n"\
            .format(self.latitude, self.longitude, self.datetime_at)


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_uuid = db.Column(db.String(36), nullable=False)
    accelerometerX = db.Column(db.Float, nullable=False)
    accelerometerY = db.Column(db.Float, nullable=False)
    accelerometerZ = db.Column(db.Float, nullable=False)
    gyroscopeX = db.Column(db.Float, nullable=False)
    gyroscopeY = db.Column(db.Float, nullable=False)
    gyroscopeZ = db.Column(db.Float, nullable=False)
    magnetometerX = db.Column(db.Float, nullable=False)
    magnetometerY = db.Column(db.Float, nullable=False)
    magnetometerZ = db.Column(db.Float, nullable=False)
    datetime_at = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return "<Sensors: accelerometer=[{}, {}, {}], " \
               "gyroscope=[{}, {}, {}], magnetometer=[{}, {}, {}], " \
               "datetime=\"{}\">\n" \
            .format(self.accelerometerX, self.accelerometerY,
                    self.accelerometerZ, self.gyroscopeX, self.gyroscopeY,
                    self.gyroscopeZ, self.magnetometerX, self.magnetometerY,
                    self.magnetometerZ, self.datetime_at)
