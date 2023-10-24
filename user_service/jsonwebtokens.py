import datetime
import jwt

SECRET_KEY = 'mysecretkey'

def create_jwt(data):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    header = {
        'alg': 'HS256', 
        'typ': 'JWT'
    }
    payload = {
        'data': data,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256', headers=header)
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "JWT đã hết hạn"
    except jwt.InvalidTokenError:
        return "JWT không hợp lệ"
