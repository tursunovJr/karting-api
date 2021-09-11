from app import create_app
from extensions import db
import unittest


class TracksTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # POST: Создать новый маршрут
    def test_create_new_track(self):
        response = self.client.post("/api/v1/tracks")
        self.assertIn("location", response.headers)
        self.assertIn("/api/v1/tracks/", response.headers["Location"])
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        self.assertIn("/api/v1/tracks/", response.json["location"])

    # GET: Получить список маршрутов
    def test_get_track_list(self):
        response = self.client.get("/api/v1/tracks")
        self.assertEqual(response.status_code, 200)
        self.assertIn("tracks", response.json.keys())

    # GET: Получить информацию об одном маршруте
    def test_get_one_track(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.get("/api/v1/tracks/{}".format(uuid))
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json.keys())
        self.assertIn("begin_datetime", response.json["coordinates"].keys())
        self.assertIn("end_datetime", response.json["coordinates"].keys())
        self.assertIn("sensors", response.json.keys())
        self.assertIn("begin_datetime", response.json["sensors"].keys())
        self.assertIn("end_datetime", response.json["sensors"].keys())

    # GET: Получить информацию об одном не существующем маршруте
    def test_get_one_track_empty_info(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            "/api/v1/tracks/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json.keys())

    # POST: Добавить координаты в маршрут
    def test_add_coordinates(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.post(
            "/api/v1/tracks/{}/coordinates".format(uuid),
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lat": 55.755831,
                        "lon": 88.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:01.000",
                        "lat": 99.755831,
                        "lon": 33.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:02.000",
                        "lat": 77.755831,
                        "lon": 11.617673
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, None)

    # POST: Добавить координаты в не существующий маршрут
    def test_add_coordinate(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/api/v1/tracks/00000000-0000-0000-0000-000000000000/coordinates",
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lat": 55.999999,
                        "lon": 77.888888
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json.keys())

    # POST: Добавить координаты в маршрут с неправильными входными данными
    def test_add_coordinate_incorrect_date(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.post(
            "/api/v1/tracks/{}/coordinates".format(uuid),
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lattitude": 55.755831,
                        "lon": 88.617673
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json.keys())
        self.assertEqual("Bad JSON format", response.json["message"])

    # GET: Получить список координат маршрута
    def test_get_track_all_coordinates(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        self.client.post(
            "/api/v1/tracks/{}/coordinates".format(uuid),
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:01.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:02.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    }
                ]
            }
        )
        response = self.client.get(
            "/api/v1/tracks/{}/coordinates".format(uuid)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json.keys())
        self.assertEqual(len(response.json["coordinates"]), 3)

    # GET: Получить список координат о не существующем маршруте
    def test_get_empty_track_all_coordinates(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            "/api/v1/tracks/00000000-0000-0000-0000-000000000000/coordinates"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json.keys())

    # POST: Добавить показания датчиков
    def test_add_sensors_data(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.post(
            "/api/v1/tracks/{}/sensors".format(uuid),
            json={
                "sensors": [
                    {
                        "datetime": "2021-01-01 00:00:02.000",
                        "accelerometer": [15.5487, 84.0024, 47.4963],
                        "gyroscope": [5.1001, 12.5221, 37.1864],
                        "magnetometer": [42.9732, 63.2212, 83.3663]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, None)

    # POST: Добавить показания датчиков для несуществующего маршрута
    def test_add_sensors_data_empty_track(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/api/v1/tracks/00000000-0000-0000-0000-000000000000/sensors",
            json={
                "sensors": [
                    {
                        "datetime": "2021-01-01 00:00:02.000",
                        "accelerometer": [15.5487, 84.0024, 47.4963],
                        "gyroscope": [5.1001, 12.5221, 37.1864],
                        "magnetometer": [42.9732, 63.2212, 83.3663]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json.keys())

    # GET: Получить показания датчиков
    def test_get_sensors_data(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        self.client.post(
            "/api/v1/tracks/{}/sensors".format(uuid),
            json={
                "sensors": [
                    {
                        "datetime": "2021-01-01 00:00:02.000",
                        "accelerometer": [15.5487, 84.0024, 47.4963],
                        "gyroscope": [5.1001, 12.5221, 37.1864],
                        "magnetometer": [42.9732, 63.2212, 83.3663]
                    },

                    {
                        "datetime": "2021-01-01 00:00:02.000",
                        "accelerometer": [77.5487, 84.0024, 47.4963],
                        "gyroscope": [88.1001, 12.5221, 37.1864],
                        "magnetometer": [99.9732, 63.2212, 83.3663]
                    },
                    {
                        "datetime": "2021-01-01 00:00:02.000",
                        "accelerometer": [11.5487, 84.0024, 47.4963],
                        "gyroscope": [22.1001, 12.5221, 37.1864],
                        "magnetometer": [33.9732, 63.2212, 83.3663]
                    }
                ]
            }
        )
        response = self.client.get("/api/v1/tracks/{}/sensors".format(uuid))
        self.assertEqual(response.status_code, 200)
        self.assertIn("sensors", response.json.keys())
        self.assertEqual(len(response.json["sensors"]), 3)

    # GET: Получить список показаний датчиков о не существующем маршруте
    def test_get_empty_track_all_sensors(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
          "/api/v1/tracks/00000000-0000-0000-0000-000000000000/sensors")
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json.keys())

    # GET: Получить список координат с использованием end_datetime
    # и begin_datetime
    def test_get_range_coordinates(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        self.client.post(
            "/api/v1/tracks/{}/coordinates".format(uuid),
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:01.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:02.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    }
                ]
            }
        )
        response = self.client.get(
            "/api/v1/tracks/{}/coordinates"
            "?end_datetime=2021-01-01T00:00:01.500".format(uuid)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json.keys())
        self.assertEqual(len(response.json["coordinates"]), 2)

        response = self.client.get(
            "/api/v1/tracks/{}/coordinates"
            "?begin_datetime=2021-01-01T00:00:01.500".format(uuid)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json.keys())
        self.assertEqual(len(response.json["coordinates"]), 1)

        response = self.client.get(
            "/api/v1/tracks/{}/coordinates"
            "?begin_datetime=2021-01-01T00:00:55.000".format(uuid)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json.keys())
        self.assertEqual(len(response.json["coordinates"]), 0)

    # GET: Получить список отсортированных координат
    def test_get_sort_coordinates(self):
        response = self.client.post("/api/v1/tracks")
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        self.client.post(
            "/api/v1/tracks/{}/coordinates".format(uuid),
            json={
                "coordinates": [
                    {
                        "datetime": "2021-01-01T00:00:00.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:02.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    },
                    {
                        "datetime": "2021-01-01T00:00:01.000",
                        "lat": 55.755831,
                        "lon": 37.617673
                    }
                ]
            }
        )
        response = self.client.get("/api/v1/tracks/{}/coordinates"
                                   .format(uuid))
        self.assertEqual(len(response.json["coordinates"]), 3)
        self.assertIn(response.json["coordinates"][0]["datetime"],
                      "2021-01-01T00:00:00.000")
        self.assertIn(response.json["coordinates"][1]["datetime"],
                      "2021-01-01T00:00:01.000")
        self.assertIn(response.json["coordinates"][2]["datetime"],
                      "2021-01-01T00:00:02.000")


if __name__ == '__main__':
    unittest.main()
