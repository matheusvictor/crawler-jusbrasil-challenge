import json
import os


def save_json_file(data, file_name: str):
    json_object = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    if not file_name.endswith('.json'):
        file_name += '.json'

    path = os.path.join('output', file_name)
    os.makedirs('output', exist_ok=True)

    with open(path, "w", encoding='utf8') as outfile:
        outfile.write(json_object)
        outfile.close()
