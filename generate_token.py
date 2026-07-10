import jwt
import datetime
from auth import JWT_SECRET

user_id = '107353106888683946567'
payload = {
    'user_id': user_id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
}
token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
print('--- YOUR SECURE TOKEN ---')
print(token)
print('-------------------------')

