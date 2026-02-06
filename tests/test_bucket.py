from exif_analyzer.summaries import bucket_focal


def test_bucket_exact_values():
    assert bucket_focal(14) == 14
    assert bucket_focal(50) == 50
    assert bucket_focal(200) == 200


def test_bucket_rounding_down():
    assert bucket_focal(84.0) == 85
    assert bucket_focal(68.0) == 70
    assert bucket_focal(134.0) == 135


def test_bucket_rounding_up():
    assert bucket_focal(86.0) == 85
    assert bucket_focal(72.0) == 70
    assert bucket_focal(148.0) == 150


def test_bucket_wide_values():
    assert bucket_focal(410.0) == 400
    assert bucket_focal(580.0) == 600


def test_bucket_small_values():
    assert bucket_focal(15.0) == 14
    assert bucket_focal(18.0) == 17

def test_bucket_equidistant_prefers_lower():
    # 77.5 is equidistant between 70 and 85, thus the function returns the first (70)
    assert bucket_focal(77.5) == 70
