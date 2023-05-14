import json
import os
import dotenv
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

dotenv.load_dotenv()
AES_SECRET_KEY = os.environ['AES_SECRET_KEY'].encode('utf-8')

def _data_to_server(obj, crypto=False):
    if obj.text.split(' ')[0].lower() in ['you', 'forefront', 'poe']:
        response = {
            'all_data': json.dumps(dict(obj)),
            'question': ' '.join(obj.text.split(' ')[1:]),
            'gpt_mode': obj.text.split(' ')[0].lower(),
        }
        return response
    else:
        response = {
            'all_data': json.dumps(dict(obj)),
            'question': obj.text,
        }
        if crypto:
            response['crypto_text'] = __encrypter(obj)
        return response

def __encrypter(obj):
    json_text = json.dumps(dict(obj))
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json_text)
    return json.dumps([cipher.nonce, tag, ciphertext])