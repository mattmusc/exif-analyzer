import json


def render_json(summary):
    return json.dumps(summary, indent=2, ensure_ascii=False)
