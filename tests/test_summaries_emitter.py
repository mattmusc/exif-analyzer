import pytest
from unittest.mock import patch, mock_open
from argparse import Namespace
from exif_analyzer.summaries_emitter import emit_summary

def test_emit_summary_console():
    args = Namespace(format="console")
    summary = {"data": "test"}
    with patch("exif_analyzer.summaries_emitter.render_console") as mock_render:
        emit_summary(summary, args)
        mock_render.assert_called_once_with(summary, args)

def test_emit_summary_json_stdout(capsys):
    args = Namespace(format="json", output=None)
    summary = {"data": "test"}
    emit_summary(summary, args)
    captured = capsys.readouterr()
    assert '"data": "test"' in captured.out

def test_emit_summary_json_file():
    args = Namespace(format="json", output="result.json")
    summary = {"data": "test"}
    m = mock_open()
    with patch("builtins.open", m):
        emit_summary(summary, args)
        m.assert_called_once_with("result.json", "w", encoding="utf-8")
        m().write.assert_called_once()

def test_emit_summary_unknown_format():
    args = Namespace(format="yaml")
    summary = {}
    with pytest.raises(ValueError, match="Unknown format: yaml"):
        emit_summary(summary, args)
