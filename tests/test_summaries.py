from exif_analyzer.metadata_extractor import PhotoMetadata
from exif_analyzer.summaries import (
    bucket_focal,
    top_apertures,
    top_cameras,
    top_focals,
    top_focals_by_camera,
    top_iso,
    top_shutter_speeds,
)

def md(fl):
    """Helper to create a PhotoMetadata object with default values."""
    return PhotoMetadata(
        file="x",
        make="Canon",
        model="5D3",
        focal_length=fl,
        iso=100,
        aperture=4.0,
        shutter_speed=0.01,
    )


def test_top_focals_without_bucket_counts_raw_values():
    data = [md(50.0), md(50.0), md(85.0)]
    got = top_focals(data, top_n=10, use_bucket=False)

    # Counter.most_common returns list of tuples (value, count)
    assert got[0] == (50.0, 2)
    assert got[1] == (85.0, 1)


def test_top_focals_filters_none_values():
    data = [md(None), md(50.0), md(50.0)]
    got = top_focals(data, top_n=10, use_bucket=False)

    assert got == [(50.0, 2)]


def test_top_focals_top_n_limits_results():
    data = [md(50.0), md(50.0), md(85.0), md(85.0), md(200.0)]
    got = top_focals(data, top_n=1, use_bucket=False)

    # first item should be either 50 or 85 (both count=2)
    assert len(got) == 1
    assert got[0][1] == 2


def test_top_focals_with_bucket_groups_values():
    # This test assumes that bucket_focal(85.0) -> 85, etc.
    # If bucket_focal rounds to standard buckets (e.g. 84->85), test it here.
    data = [md(84.9), md(85.1), md(85.0)]
    got = top_focals(data, top_n=10, use_bucket=True)

    # We expect all to end up in the same bucket (85)
    assert got[0][1] == 3

def test_top_focals_with_bucket():
    data = [
        md(84.9),
        md(85.1),
        md(86.0),
        md(135.0),
    ]

    got = top_focals(data, top_n=10, use_bucket=True)

    # 3 focal lengths are in bucket 85, 1 in bucket 135
    assert got[0] == (85, 3)
    assert got[1] == (135, 1)


def test_bucket_focal():
    assert bucket_focal(14.2) == 14
    assert bucket_focal(16.9) == 17
    assert bucket_focal(35.0) == 35
    assert bucket_focal(400) == 400
    assert bucket_focal(1000) == 600  # max bucket


def test_top_cameras():
    data = [
        md(50),
        md(50),
    ]
    data[1].make = "Sony"
    data[1].model = "A7III"

    got = top_cameras(data, top_n=10)
    assert got[0] == ("Canon 5D3", 1)
    assert ("Sony A7III", 1) in got


def test_top_focals_by_camera():
    data = [
        md(50),
        md(50),
    ]
    data[1].model = "A7III"

    got = top_focals_by_camera(data, top_n=10)
    assert got["5D3"] == [(50, 1)]
    assert got["A7III"] == [(50, 1)]


def test_top_iso():
    data = [md(50)]
    data[0].iso = 105
    got = top_iso(data, top_n=10)
    assert got == [(100, 1)]


def test_top_apertures():
    data = [md(50)]
    data[0].aperture = 2.84
    got = top_apertures(data, top_n=10)
    assert got == [(2.8, 1)]


def test_top_shutter_speeds():
    data = [md(50)]
    data[0].shutter_speed = 1 / 500
    got = top_shutter_speeds(data, top_n=10)
    assert got == [(0.002, 1)]

# adds test for None values

def test_top_shutter_speeds_none():
    data = [md(50)]
    data[0].shutter_speed = None
    got = top_shutter_speeds(data, top_n=10)
    assert got == []

def test_top_apertures_none():
    data = [md(50)]
    data[0].aperture = None
    got = top_apertures(data, top_n=10)
    assert got == []

def test_top_iso_none():
    data = [md(50)]
    data[0].iso = None
    got = top_iso(data, top_n=10)
    assert got == []

def test_top_cameras_none():
    data = [md(50)]
    data[0].make = None
    data[0].model = None
    got = top_cameras(data, top_n=10)
    assert got == []

def test_top_focals_by_camera_none():
    data = [md(50)]
    data[0].focal_length = None
    got = top_focals_by_camera(data, top_n=10)
    assert got == {}
