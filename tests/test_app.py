import pytest
from unittest.mock import patch, MagicMock
from geo_cache.app import app, round_to_grid, get_cache_key, get_address_from_coordinates
import json
import requests

@pytest.fixture
def mock_redis():
    with patch('geo_cache.app.redis_client') as mock:
        yield mock

@pytest.fixture
def mock_requests():
    with patch('geo_cache.app.requests.get') as mock:
        yield mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_coordinates():
    return {
        'lat': 51.5074,
        'lon': -0.1278,
        'grid_lat': 51.507,
        'grid_lon': -0.128
    }

def test_round_to_grid(test_coordinates):
    assert round_to_grid(test_coordinates['lat'], 0.001) == test_coordinates['grid_lat']
    assert round_to_grid(test_coordinates['lon'], 0.001) == test_coordinates['grid_lon']
    assert round_to_grid(0.0, 0.001) == 0.0

def test_get_cache_key(test_coordinates):
    key = get_cache_key(test_coordinates['lat'], test_coordinates['lon'])
    assert key == f"geocache:{test_coordinates['grid_lat']}:{test_coordinates['grid_lon']}"
    assert isinstance(key, str)

def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b'pong'

def test_geocode_invalid_params(client):
    response = client.get('/geocode')
    assert response.status_code == 400
    assert b'Invalid coordinates provided' in response.data

    response = client.get('/geocode?lat=invalid&lon=0')
    assert response.status_code == 400
    assert b'Invalid coordinates provided' in response.data

@pytest.fixture
def mock_address_data():
    return {"address": {"city": "London"}}

def test_get_address_from_coordinates_cache_hit(mock_requests, mock_redis, test_coordinates, mock_address_data):
    # Mock cached data
    mock_redis.get.return_value = json.dumps(mock_address_data)

    result = get_address_from_coordinates(test_coordinates['lat'], test_coordinates['lon'])
    
    assert result == mock_address_data
    mock_redis.get.assert_called_once()
    mock_requests.assert_not_called()

def test_get_address_from_coordinates_cache_miss(mock_requests, mock_redis, test_coordinates, mock_address_data):
    # Mock Redis cache miss
    mock_redis.get.return_value = None
    
    # Mock Nominatim response
    mock_response = MagicMock()
    mock_response.json.return_value = mock_address_data
    mock_requests.return_value = mock_response

    result = get_address_from_coordinates(test_coordinates['lat'], test_coordinates['lon'])
    
    assert result == mock_address_data
    mock_redis.get.assert_called_once()
    mock_requests.assert_called_once()
    mock_redis.setex.assert_called_once()

def test_get_address_from_coordinates_api_error(mock_requests, mock_redis, test_coordinates):
    # Mock Redis cache miss
    mock_redis.get.return_value = None
    
    # Mock Nominatim error
    mock_requests.side_effect = requests.RequestException("API Error")

    result = get_address_from_coordinates(test_coordinates['lat'], test_coordinates['lon'])
    
    assert result is None
    mock_redis.get.assert_called_once()
    mock_requests.assert_called_once()
