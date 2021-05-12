from redis import Redis

from swiper.config import REDIS_CONFIG


rds = Redis(**REDIS_CONFIG)
