import redis
from redis import ConnectionPool
from base.base_readConfig import Config
from base.base_log import Log


class RedisDatabase:
    def __init__(self):
        try:
            host = Config().read_config('redis.ini', 'redis', 'host')
            port = Config().read_config('redis.ini', 'redis', 'port')
            password = Config().read_config('redis.ini', 'redis', 'password')
            self.connect = redis.StrictRedis(host=host, port=port, password=password)
        except Exception as e:
            Log().error('连接redis出错: {}'.format(e))

    def delete_redis(self, type, name, key=None):
        try:
            if self.connect.exists(name):
                if type == 'hash':
                    self.connect.hdel(name, key)
                else:
                    self.connect.delete(name)
        except Exception as e:
            Log().error('删除redis的值失败, {}'.format(e))

