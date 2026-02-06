from argparse import Namespace
from exif_analyzer.metadata_extractor import PhotoMetadata
from exif_analyzer.summaries_builders import (
    build_summary,
    build_focal_lengths_summary,
    build_cameras_summary,
    build_camera_focal_lengths_summary,
    build_iso_summary,
    build_aperture_summary,
    build_shutter_speed_summary,
)

def md(
    focal=None,
    make="Canon",
    model="5D3",
    iso=100,
    aperture=2.8,
    shutter=0.01,
):
    return PhotoMetadata(
        file="x",
        make=make,
        model=model,
        focal_length=focal,
        iso=iso,
        aperture=aperture,
        shutter_speed=shutter,
    )

def test_build_focal_lengths_summary():
    results = [md(50.0), md(50.0), md(85.0)]
    got = build_focal_lengths_summary(results, top_n=10, use_bucket=False)
    assert got == [
        {"focal_mm": 50.0, "count": 2},
        {"focal_mm": 85.0, "count": 1},
    ]

def test_build_cameras_summary():
    results = [md(model="5D3"), md(model="A7III", make="Sony")]
    got = build_cameras_summary(results, top_n=10)
    assert {"camera": "Canon 5D3", "count": 1} in got
    assert {"camera": "Sony A7III", "count": 1} in got

def test_build_camera_focal_lengths_summary():
    results = [md(50.0, model="5D3"), md(35.0, model="A7III", make="Sony")]
    got = build_camera_focal_lengths_summary(results, top_n=10, use_bucket=False)
    assert {"camera": "5D3", "focal_mm": 50.0, "count": 1} in got
    assert {"camera": "A7III", "focal_mm": 35.0, "count": 1} in got

def test_build_iso_summary():
    results = [md(iso=105)]
    got = build_iso_summary(results, top_n=10)
    assert got == [{"iso": 100, "count": 1}]

def test_build_aperture_summary():
    results = [md(aperture=2.84)]
    got = build_aperture_summary(results, top_n=10)
    assert got == [{"aperture": "ƒ2.8", "count": 1}]

def test_build_shutter_speed_summary():
    results = [md(shutter=1/500)]
    got = build_shutter_speed_summary(results, top_n=10)
    assert got == [{"shutter_speed": "1/20", "count": 1}]

def test_build_summary():
    results = [md(focal=50.0, iso=100)]
    args = Namespace(top_n=10, bucket_focals=False)
    summary = build_summary(results, args)
    
    assert "focal_lengths" in summary
    assert "cameras" in summary
    assert "camera_focal_lengths" in summary
    assert "isos" in summary
    assert "apertures" in summary
    assert "shutter_speeds" in summary
    
    assert summary["focal_lengths"] == [{"focal_mm": 50.0, "count": 1}]
    assert summary["isos"] == [{"iso": 100, "count": 1}]
