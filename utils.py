import json
import os


def valid_process_number():
    # [0-9]{7}\-[0-9]{2}\.[0-9]{4}\.[0-9]{1}\.[0-9]{2}\.[0-9]+
    pass


def save_json_file(data, file_name: str):
    json_object = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    if not file_name.endswith('.json'):
        file_name += '.json'

    path = os.path.join('output', file_name)
    os.makedirs('output', exist_ok=True)

    with open(path, "w", encoding='utf8') as outfile:
        outfile.write(json_object)
