from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Grid precision for coordinate rounding (in degrees)
GRID_PRECISION = float(getenv('GRID_PRECISION', '0.001'))

# Redis configuration
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(getenv('REDIS_PORT', '6379'))
REDIS_DB = int(getenv('REDIS_DB', '0'))

# Cache configuration
CACHE_EXPIRATION = int(getenv('CACHE_EXPIRATION', '86400'))  # 24 hours in seconds
