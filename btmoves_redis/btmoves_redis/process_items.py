# 把redis缓存中的数据转存到mongoDB或者mysql中
import  pymysql
import pymongo
from redis import Redis
from btmoves_redis.btmoves_redis import settings
import json

# 从redis中取数据
rds = Redis(settings.REDIS_HOST, settings.REDIS_PORT )
# client = pymongo.MongoClient(host='47.104.128.150', port=27017)
# db = client['btdy']
# collection = db['movies']
# collection.insert(data)
    # break
#     mysql数据库
conn = pymysql.connect(
    host= '127.0.0.1',
    user= 'root',
    password= '0321',
    db= 'movies',
    charset= 'utf8'
)
cursor = conn.cursor()

# 取出数据
while True:
    _, item = rds.blpop(settings.REDIS_ITEMS_KEY)
    # 2. 把取出的数据存储到数据库中
    data = json.loads(item.decode())
    print(data)
    sql = 'insert into moves1(`name`, score, category ) VALUES (%s, %s, %s)'
    cursor.execute(sql, (data['name'], data['score'], data['category']))
    conn.commit()
    # cursor.close()
    # conn.close()
