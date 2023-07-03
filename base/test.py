import hashlib
hl = hashlib.md5()
password = 'test11'
hl.update(password.encode(encoding='utf-8'))
password = hl.hexdigest()
print(password)