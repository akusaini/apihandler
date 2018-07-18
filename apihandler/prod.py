REDIS_HP = "127.0.0.1:6379"
REDIS_PASSWORD = "123"
REDIS_DB = "0"


CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/0",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
			"PASSWORD": REDIS_PASSWORD,
			"PICKLE_VERSION": -1,
			"SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
			"SOCKET_TIMEOUT": 5,  # in seconds
			"IGNORE_EXCEPTIONS": True,
			#"CONNECTION_POOL_KWARGS": {"max_connections": 100},

		}
	}
}
