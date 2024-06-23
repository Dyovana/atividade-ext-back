import hashlib


def enconder(password):
    encode_password = password.encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(encode_password)

    return hasher.hexdigest()
