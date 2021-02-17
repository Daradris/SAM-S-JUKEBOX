1
	
import hashlib


strr = b"15 - Jimi Hendrix - Electric Ladyland - All Along the Watchtower"

hash_object = hashlib.md5(strr)
print(hash_object.hexdigest())
print(len(hash_object.hexdigest()))
