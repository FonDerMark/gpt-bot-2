import json
import requests

def _data_to_server(obj):
    return {
        'all_data': json.dumps(dict(obj))
    }
