<p align="center">
  <img src="assets/earth.png" alt="Repo preview" width="150"/>
</p>

# GeoCache

> Fast and reliable geocoding service with Redis caching

A modern Flask-based API that converts geographic coordinates to human-readable addresses using OpenStreetMap's Nominatim service. Built with performance in mind, it includes Redis caching to minimize external API calls and Docker for easy deployment.

## ✨ Features

*   🗺️ Reverse geocoding using OpenStreetMap's Nominatim service
*   🚀 Smart grid-based caching:
    *   100m precision (0.001° grid) (configurable)
    *   Nearby locations share cache entries
    *   Redis backend for fast retrieval
    *   24-hour expiration
*   🐳 Easy deployment with Docker and Docker Compose
*   🔄 RESTful API with JSON responses
*   📚 Interactive API documentation at root endpoint

## 💻 Requirements

*   Docker and Docker Compose for containerization
*   Poetry for Python dependency management (local development)

## 🔧 Quick Start

### Using Docker (Recommended)

Clone the repository:

```
git clone https://github.com/puchkoff/geo_cache.git
cd geo_cache
```

Build and launch with Docker Compose:

```
docker compose up --build
```

Visit the API:

*   🌐 http://localhost - Service version
*   📚 http://localhost/spec - Interactive API documentation
*   🏓 http://localhost/ping - Health check endpoint
*   🔍 http://localhost/geocode - Geocoding endpoint

## 📖 API Documentation

### GET / - Service Version

Returns a simple service identification message.

```
Geo Cache service ver 1.0
```

### GET /spec - API Documentation

Returns detailed API documentation and service information.

```
{
    "service": {
        "title": "GeoCache API",
        "description": "🌍 Fast and reliable geocoding service with Redis caching",
        "version": "1.0.0"
    },
    "endpoints": { ... },
    "tech_stack": { ... }
}
```

### GET /ping - Health Check

Simple health check endpoint.

```
pong
```

### GET /geocode - Reverse Geocoding

Converts geographic coordinates to a human-readable address.

**Parameters:**

*   `lat` (float): Latitude coordinate
*   `lon` (float): Longitude coordinate

**Example:**

```
curl "http://localhost/geocode?lat=51.5074&lon=-0.1278"
```

**Response:**

Returns address details in JSON format with smart grid-based caching:

*   Coordinates are rounded to 0.001° precision (~100m grid) (configurable)
*   Nearby locations within the same grid cell share the cache (configurable)
*   Results are cached in Redis for 24 hours (configurable)

```
{
    "address": {
        "city": "London",
        "country": "United Kingdom",
        ...
    }
}
```

Request example:

```
curl "http://localhost/geocode?lat=51.5074&lon=-0.1278"
```

Answer example:

```
{
  "address": {
    "ISO3166-2-lvl4": "GB-ENG",
    "ISO3166-2-lvl8": "GB-WSM",
    "amenity": "Bench",
    "city": "City of Westminster",
    "country": "United Kingdom",
    "country_code": "gb",
    "neighbourhood": "Seven Dials",
    "postcode": "WC2N 5DX",
    "road": "Charing Cross",
    "state": "England",
    "state_district": "Greater London",
    "suburb": "Waterloo"
  },
  "addresstype": "amenity",
  "boundingbox": [
    "51.5073500",
    "51.5074500",
    "-0.1278500",
    "-0.1277500"
  ],
  "class": "amenity",
  "display_name": "Bench, Charing Cross, Seven Dials, Waterloo, City of Westminster, Greater London, England, WC2N 5DX, United Kingdom",
  "importance": 9.307927061870783e-05,
  "lat": "51.5074000",
  "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
  "lon": "-0.1278000",
  "name": "Bench",
  "osm_id": 12805868201,
  "osm_type": "node",
  "place_id": 405990550,
  "place_rank": 30,
  "type": "bench"
}
```

## 💻 Development

### Configuration

The service can be configured using environment variables in `.env` file:

*   `GRID_PRECISION` - Grid precision for coordinate rounding (default: 0.001)
*   `REDIS_HOST` - Redis server hostname (default: localhost)
*   `REDIS_PORT` - Redis server port (default: 6379)
*   `REDIS_DB` - Redis database number (default: 0)

### Tech Stack

*   🐍 Backend: Python 3.9 with Flask
*   🚀 Caching: Redis
*   🐳 Deployment: Docker & Docker Compose
*   🗺️ Geocoding: OpenStreetMap Nominatim

## 📝 License

MIT License - feel free to use this project for your own purposes