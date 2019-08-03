import redis

redis_server = redis.Redis(host="localhost",port=6379)

#gets the value of the key from cache
def getFromCache(key):
	
	response = redis_server.get(key)
	print(redis_server.ttl(key))
	return response

# sends key,value pair to the cache.
def setToCache(key, value, hrs, set):
	
	redis_server.set(key, value)
	if set:
		redis_server.expire(key, hrs*3600)
	print(redis_server.ttl(key))

# Returns true if the numbers are blocked.
def isBlocked (to, frm):
	to_num = getFromCache(to)
	from_num = getFromCache(frm)
	# checks if the pair of to,from are stored in cache 
	if (to_num != None and to_num.decode('utf-8') == frm) or (from_num != None and from_num.decode('utf-8') == to) :
		return True
	else:
		return False

