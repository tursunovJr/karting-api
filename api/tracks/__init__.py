from flask import Blueprint, json
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from api.tracks.controllers import Tracks, Coordinates, TrackInfo, Sensors


api_tracks_bp = Blueprint("api", __name__)
api_tracks = Api(api_tracks_bp)

# Add resources
api_tracks.add_resource(Tracks, "/tracks")
api_tracks.add_resource(TrackInfo, "/tracks/<uuid:track_uuid>",
                        endpoint="track_info")
api_tracks.add_resource(Coordinates, "/tracks/<uuid:track_uuid>/coordinates")
api_tracks.add_resource(Sensors, "/tracks/<uuid:track_uuid>/sensors")


# JSON format for error
@api_tracks_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
