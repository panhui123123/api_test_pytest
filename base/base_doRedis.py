import redis
from base.base_readConfig import Config
from base.base_log import Log


class RedisDatabase:
    def __init__(self):
        try:
            host = Config().read_config('redis.ini', 'redis', 'host')
            port = Config().read_config('redis.ini', 'redis', 'port')
            password = Config().read_config('redis.ini', 'redis', 'password')
            pool = redis.ConnectionPool(host=host, port=port, password=None, decode_responses=True)
            self.connect = redis.StrictRedis(connection_pool=pool)
        except Exception as e:
            Log().error('连接redis出错: {}'.format(e))

    def delete_redis(self, redis_type, redis_name, redis_key=None):
        try:
            if self.connect.exists(redis_name):
                if redis_type == "hash":
                    self.connect.hdel(redis_name, redis_key)
                else:
                    self.connect.delete(redis_name)
        except Exception as e:
            Log().error('删除redis的值失败，Error: {0}'.format(e))
        finally:
            # 关闭连接
            self.connect.close()

    def set_redis(self, redis_type, redis_name, redis_key, value):
        try:
            if self.connect.exists(redis_name):
                if redis_type == "hash":
                    self.connect.hset(redis_name, redis_key, value)
                elif redis_type == "string":
                    self.connect.setex(redis_name, redis_key, value)
                elif redis_type == "list":
                    self.connect.lset(redis_name, redis_key, value)
                    Log().info("已删除{0}的{1}的值".format(redis_key, redis_name))
            else:
                Log().info("设置redis{0}里面没有找到{1}".format(redis_name, redis_key))
        except Exception as e:
            Log().error('设置redis的值失败，Error: {}'.format(e))
        finally:
            # 关闭连接
            self.connect.close()

    def get_redis_value(self, redis_type, redis_name, redis_key=None, index=0):
        value = None
        try:
            if self.connect.exists(redis_name):
                if redis_type == "hash":
                    value = self.connect.hget(redis_name, redis_key)
                elif redis_type == "string":
                    value = self.connect.get(redis_name)
                elif redis_type == "list":
                    value = self.connect.lindex(redis_name, index)
                elif redis_type == "zset":
                    value = self.connect.zscore(redis_name, redis_key)
            else:
                Log().info("redis里不存在{0}里面没有找到{1}".format(redis_name, redis_key))
        except Exception as e:
            Log().error('Error: {}'.format(e))
        finally:
            # 关闭连接
            self.connect.close()
            return value

    def delete_all_hash_key(self, redis_name):
        try:
            if self.connect.exists(redis_name):
                for redis_key in self.connect.hkeys(redis_name):
                    self.connect.hdel(redis_name, redis_key)
            else:
                Log().info("redis里不存在{0}里面没有找到".format(redis_name))
        except Exception as e:
            Log().error('Error: {}'.format(e))
        finally:
            # 关闭连接
            self.connect.close()


if __name__ == '__main__':
    MyRedis = RedisDatabase()
    print(MyRedis.get_redis_value('string', 'guolong'))
    print(MyRedis.get_redis_value('list', 'mylist'))
    print(MyRedis.get_redis_value('hash', 'userinfo', 'name'))
