import json
from exif_analyzer.renderers.json import render_json

def test_render_json():
    data = {"key": "value", "list": [1, 2, 3]}
    got = render_json(data)
    
    parsed = json.loads(got)
    assert parsed == data
    # Check for indentation (indent=2)
    assert '  "key": "value"' in got
