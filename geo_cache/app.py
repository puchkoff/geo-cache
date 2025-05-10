from flask import Flask, request, jsonify
import requests
import redis
import json
from typing import Optional, Dict
from . import config
from loguru import logger

app = Flask(__name__)
logger.add("geo_cache.log", rotation="500 MB", backtrace=True, diagnose=True)
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True
)

def round_to_grid(value: float, precision: float = config.GRID_PRECISION) -> float:
    """Round a coordinate to the nearest grid point."""
    return round(value / precision) * precision

def get_cache_key(lat: float, lon: float) -> str:
    """Generate cache key for coordinates using grid system."""
    grid_lat = round_to_grid(lat)
    grid_lon = round_to_grid(lon)
    return f"geocache:{grid_lat}:{grid_lon}"

def get_address_from_coordinates(lat: float, lon: float) -> Optional[Dict]:
    """Get address from coordinates using Nominatim with grid-based caching.
    
    Uses a grid system where coordinates are rounded to the nearest 0.001 degree
    (approximately 100 meters) to improve cache hit rate for nearby locations.
    """
    # Check cache first using grid-based key
    cache_key = get_cache_key(lat, lon)
    if cached_result := redis_client.get(cache_key):
        logger.info(f"Cache hit for lat={lat}, lon={lon}")
        return json.loads(cached_result)
    
    # If not in cache, fetch from Nominatim
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "GeoCache/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Store in cache
        redis_client.setex(
            cache_key,
            config.CACHE_EXPIRATION,
            json.dumps(result)
        )
        logger.info(f"Fetched address from Nominatim for lat={lat}, lon={lon}")
        return result
    except requests.RequestException:
        logger.exception("Error while requesting Nominatim API")
        return None


@app.route("/spec")
def spec():
    return jsonify({
        "service": {
            "title": "GeoCache API",
            "description": "🌍 Fast and reliable geocoding service with Redis caching",
            "version": "1.0.0",
            "github": "https://github.com/yourusername/geo_cache"
        },
        "endpoints": {
            "GET /spec": {
                "description": "📚 Service information and documentation",
                "returns": "This documentation page"
            },
            "GET /ping": {
                "description": "🏓 Health check endpoint",
                "returns": "pong"
            },
            "GET /geocode": {
                "description": "🔍 Convert coordinates to address with Redis caching",
                "parameters": {
                    "lat": "Latitude (float)",
                    "lon": "Longitude (float)"
                },
                "example": "/geocode?lat=51.5074&lon=-0.1278",
                "cache": "Results are cached for 24 hours"
            }
        },
        "tech_stack": {
            "backend": "🐍 Python with Flask",
            "caching": "🚀 Redis",
            "deployment": "🐳 Docker & Docker Compose",
            "geocoding": "🗺️ OpenStreetMap Nominatim"
        }
    })

@app.route("/")
def index():
    return "Geo Cache service ver 1.0"

@app.route("/ping")
def ping():
    return "pong"

@app.route("/geocode", methods=["GET"])
def geocode():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        logger.warning("Invalid coordinates provided in request")
        return jsonify({"error": "Invalid coordinates provided"}), 400

    logger.info(f"Geocode request received for lat={lat}, lon={lon}")

    result = get_address_from_coordinates(lat, lon)    
    if not result:
        logger.error(f"Could not fetch address for lat={lat}, lon={lon}")
        return jsonify({"error": "Could not fetch address"}), 500    
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
