import json
import requests

def _data_to_server(obj):
    if obj.text.split(' ')[0].lower() in ['you', 'forefront', 'poe']:
        response = {
            'all_data': json.dumps(dict(obj)),
            'question': ' '.join(obj.text.split(' ')[1:]),
            'gpt_mode': obj.text.split(' ')[0].lower(),
        }
        return response
    else:
        return {
            'all_data': json.dumps(dict(obj)),
            'question': obj.text,
        }
