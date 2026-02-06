import pytest
from argparse import Namespace
from exif_analyzer.renderers.console import (
    print_table,
    print_focal_lengths_summary,
    print_cameras_summary,
    print_camera_focal_lengths_summary,
    print_iso_summary,
    print_aperture_summary,
    print_shutter_speed_summary,
    render_console,
)

@pytest.fixture
def mock_args():
    return Namespace(top_n=10)

def test_print_table(capsys):
    title = "Test Table"
    headers = ["H1", "H2"]
    rows = [["R1C1", "R1C2"], ["R2C1", "R2C2"]]
    widths = [10, 10]
    
    print_table(title, headers, rows, widths)
    captured = capsys.readouterr()
    
    assert title in captured.out
    assert "H1" in captured.out
    assert "R1C1" in captured.out
    assert "R2C2" in captured.out

def test_print_focal_lengths_summary(capsys, mock_args):
    summary = {
        "focal_lengths": [{"focal_mm": 50, "count": 5}, {"focal_mm": 85, "count": 2}]
    }
    print_focal_lengths_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used Focal Lengths:" in captured.out
    assert "50mm" in captured.out
    assert "5" in captured.out

def test_print_cameras_summary(capsys, mock_args):
    summary = {
        "cameras": [{"camera": "Canon 5D3", "count": 10}]
    }
    print_cameras_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used Cameras:" in captured.out
    assert "Canon 5D3" in captured.out

def test_print_camera_focal_lengths_summary(capsys, mock_args):
    summary = {
        "camera_focal_lengths": [{"camera": "Sony A7", "focal_mm": 35, "count": 3}]
    }
    print_camera_focal_lengths_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used Focal Lengths for each camera:" in captured.out
    assert "Sony A7" in captured.out
    assert "35mm" in captured.out

def test_print_iso_summary(capsys, mock_args):
    summary = {
        "isos": [{"iso": 100, "count": 20}]
    }
    print_iso_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used ISO Values:" in captured.out
    assert "100" in captured.out

def test_print_aperture_summary(capsys, mock_args):
    summary = {
        "apertures": [{"aperture": "ƒ2.8", "count": 15}]
    }
    print_aperture_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used Aperture Values:" in captured.out
    assert "ƒ2.8" in captured.out

def test_print_shutter_speed_summary(capsys, mock_args):
    summary = {
        "shutter_speeds": [{"shutter_speed": "1/500", "count": 8}]
    }
    print_shutter_speed_summary(summary, mock_args)
    captured = capsys.readouterr()
    assert "Top 10 Most Used Shutter Speed Values:" in captured.out
    assert "1/500" in captured.out

def test_render_console(capsys, mock_args):
    summary = {
        "focal_lengths": [],
        "cameras": [],
        "camera_focal_lengths": [],
        "isos": [],
        "apertures": [],
        "shutter_speeds": [],
    }
    render_console(summary, mock_args)
    captured = capsys.readouterr()
    # Check if a few titles exist
    assert "Top 10 Most Used Focal Lengths:" in captured.out
    assert "Top 10 Most Used Cameras:" in captured.out
