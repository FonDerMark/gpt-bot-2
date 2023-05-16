import json
import os
import dotenv
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

dotenv.load_dotenv()
AES_SECRET_KEY = os.environ['AES_SECRET_KEY'].encode('utf-8')

def data_to_server(obj, crypto=False):
    if crypto:
        response = {
            'all_data': json.dumps(dict(obj)),
            'key': __encrypter(obj),
        }
        return response
    elif obj.text.split(' ')[0].lower() in ['you', 'forefront', 'poe', 'theb']:
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
        return response

def __encrypter(obj):
    json_text_binary = json.dumps(dict(obj)).encode()
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json_text_binary)
    return json.dumps([cipher.nonce.decode('iso-8859-1'), tag.decode('iso-8859-1'), ciphertext.decode('iso-8859-1')])