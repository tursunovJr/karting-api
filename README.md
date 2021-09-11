# Docker

```bash
docker build -t karting_api .
docker run -d --restart=always -v {path}/sqlite:/api/sqlite --network host karting_api
```
# Karting API v1.1.3

## Маршруты [/tracks]

### Создать новый маршрут [POST]
+ Response 201 (application/json)
    + Attributes(object)
        + uuid: 9d13061e-121a-47c1-a4ea-494838d9d9e0 (uuid, required) - Идентификатор созданного маршрута в формате UUID
    + Headers
        ```
        Location: http://{ip:port}/api/v1/tracks/{track_uuid}
        ```
    + Body
        ```
        {
            "location": "/api/v1/tracks/{uuid}" 
        }
        ```


### Получить список маршрутов [GET]

+ Response 200 (application/json)
    + Body
        ```
        {
            "tracks": [
                {
                    "uuid": "9d13061e-121a-47c1-a4ea-494838d9d9e0",
                    "coordinates": {
                        "begin_datetime": "2021-01-01 00:00:00.000",
                        "end_datetime": "2022-01-00 00:00:00.000",
                    },
                    "sensors": {
                        "begin_datetime": "2021-01-0 T00:00:00.000",
                        "end_datetime": "2022-01-00 00:00:00.000",
                    }
                },
                ...
            ]
        }
        ```

## Маршрут [/tracks/{uuid}]

+ Parameters
    + uuid (uuid, required)
        Идентификатор маршрута в формате UUID
        + Sample: 9d13061e-121a-47c1-a4ea-494838d9d9e0

### Получить информацию о маршруте [GET]

+ Response 200 (application/json)
    + Body
        ```
        {
            "coordinates": {
                "begin_datetime": "2021-01-01 00:00:00.000",
                "end_datetime": "2022-01-00 00:00:00.000",
            },
            "sensors": {
                "begin_datetime": "2021-01-01 00:00:00.000",
                "end_datetime": "2022-01-00 00:00:00.000",
            }

        }
        ```

+ Response 404 (application/json)
    + Body
        ```
        {
            "message": "Track with uuid:{uuid} not found"
        }
        ```


## Координаты маршрута [/tracks/{uuid}/coordinates{?begin_datetime,end_datetime}]

+ Parameters
    + uuid (uuid, required)
        Идентификатор существующего маршрута в формате uuid
        + Sample: 9d13061e-121a-47c1-a4ea-494838d9d9e0
    + begin_datetime (datetime, optional)
        Временная метка начала измерений в формате ISO 8601
        + Sample: 2020-01-01T00:00:00.000
        + Default: временная метка начала маршрута
    + end_datetime (datetime, optional)
        Временная метка конца измерений в формате ISO 8601
        + Sample: 2050-01-01T00:00:00.000
        + Default: текущая временная метка

### Добавить координаты в маршрут [POST]

+ Request (application/json)
    + Attributes(object)
        + datetime: 2021-01-01T00:00:00.000 (datetime, required) - Время измерения координат
        + lat: 55.755831 (number, decimal, required) - Широта в десятичном формате
        + lot: 37.617673 (number, decimal, required) - Долгота в десятичном формате
    + Body
        ```
        {
            "coordinates": [
                {
                    "datetime": "2021-01-01T00:00:00.000",
                    "lat": 55.755831,
                    "lon": 37.617673
                },
                ...
            ]
        }
        ```

+ Response 201 (application/json)
    + Body
        ```
        {}
        ```
+ Response 400 (application/json)
    + Body
        ```
        {
            "message": "Bad JSON format"
        }
        ```

+ Response 404 (application/json)
    + Body
        ```
        {
            "message": "Track with uuid:{uuid} not found"
        }
        ```

### Получить список координат маршрута [GET]

+ Response 200 (application/json)
    + Body
        ```
        {
            "coordinates": [
                {
                    "datetime": "2021-01-01T00:00:00.000",
                    "lat": 55.755831,
                    "lon": 37,617673
                },
                ...
            ]
        }
        ```
    
+ Response 404 (application/json)
    + Body
        ```
        {
            "message": "Track with uuid:{uuid} not found"
        }
        ```

## Показания датчиков - [/tracks/{uuid}/sensors{?begin_datetime,end_datetime}]

+ Parameters
    + uuid (uuid, required)
        Идентификатор существующего маршрута в формате uuid
        + Sample: 9d13061e-121a-47c1-a4ea-494838d9d9e0
    + begin_datetime (datetime, optional)
        Временная метка начала измерений в формате ISO 8601
        + Sample: 2020-01-01T00:00:00.000
        + Default: временная метка начала маршрута
    + end_datetime (datetime, optional)
        Временная метка конца измерений в формате ISO 8601
        + Sample: 2050-01-01T00:00:00.000
        + Default: текущая временная метка

### Добавить показания датчиков [POST]

+ Request(application/json)
    + Attributes(object)
        + datetime: 2021-01-01 00:00:00.000 (datetime, required) - Время измерения сенсоров
        + accelerometer: [15.5487, 84.0024, 47.4963] (array[number,decimal], required) - Показания акселерометра по осям: x, y, z
        + gyroscope: [5.1001, 12.5221, 37.1864] (array[number,decimal], required) - Показания гироскопа по осям: x, y, z
        + magnetometer: [42.9732, 63.2212, 83.3663] (array[number,decimal], required) - Показания магнетометра по осям: x, y, z
    + Body
        ```
        "sensors": [
                {
                    "datetime": "2021-01-01 00:00:00.000",
                    "accelerometer": [15.5487, 84.0024, 47.4963],
                    "gyroscope": [5.1001, 12.5221, 37.1864],
                    "magnetometer": [42.9732, 63.2212, 83.3663] 
                },
                ...
            ]    
        ```
+ Response 201 (application/json)
    + Body
        ```
        {}
        ```
+ Response 400 (application/json)
    + Body
        ```
        {
            "message": "Bad JSON format"
        }
        ```
+ Response 404 (application/json)
    + Body
        ```
        {
            "message": "Track with uuid:{uuid} not found"
        }
        ```

### Получить список показаний датчиков [GET]

+ Response 200 (application/json)
    + Body
        ```
        {
            "sensors": [
                {
                    "datetime": "2021-01-01 00:00:00.000",
                    "accelerometer": {
                        "x": 15.5487,
                        "y": 84.0024,
                        "z": 47.4963
                    },
                    "gyroscope": {
                        "x": 5.1001,
                        "y": 12.5221,
                        "z": 37.1864
                    },
                    "magnetometer": {
                        "x": 42.9732,
                        "y": 63.2212,
                        "z": 83.3663
                    } 
                },
                ...
            ] 
        }
        ```
+ Response 404 (application/json)
    + Body
        ```
        {
            "message": "Track with uuid:{uuid} not found"
        }
        ```
