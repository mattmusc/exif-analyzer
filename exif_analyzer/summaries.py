from collections import Counter, defaultdict

DEFAULT_ISO_BINS = (50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200)

FOCAL_BUCKETS = (
    14,
    17,
    20,
    21,
    23,
    24,
    28,
    35,
    40,
    50,
    70,
    85,
    100,
    135,
    150,
    200,
    300,
    400,
    600,
)


def bucket_focal(focal: float) -> int:
    """Buckets a focal length into the nearest standard focal length.

    Args:
        focal (float): The focal length to bucket.

    Returns:
        int: The nearest standard focal length.
    """
    return min(FOCAL_BUCKETS, key=lambda b: abs(b - focal))


def top_focals(results, top_n: int, use_bucket: bool = True):
    """Gets the top N most used focal lengths.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top focal lengths to return.
        use_bucket (bool): Whether to use bucketed focal lengths.

    Returns:
        list[tuple[int, int]]: List of (focal length, count) tuples.
    """
    fls = [r.focal_length for r in results if r.focal_length is not None]
    if use_bucket:
        fls = [bucket_focal(fl) for fl in fls]
    return Counter(fls).most_common(top_n)


def top_cameras(results, top_n: int):
    """Gets the top N most used cameras.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top cameras to return.

    Returns:
        list[tuple[str, int]]: List of (camera, count) tuples.
    """
    cams = [f"{r.make} {r.model}" for r in results if r.make and r.model]
    return Counter(cams).most_common(top_n)


def top_focals_by_camera(results, top_n: int, use_bucket: bool = True):
    """Gets the top N most used focal lengths for each camera.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top focal lengths to return.
        use_bucket (bool): Whether to use bucketed focal lengths.

    Returns:
        dict[str, list[tuple[int, int]]]: Dictionary of (camera, focal length, count) tuples.
    """
    data = defaultdict(Counter)
    for r in results:
        if r.focal_length is None:
            continue
        focal = bucket_focal(r.focal_length) if use_bucket else r.focal_length
        data[r.model][focal] += 1
    return {cam: cnt.most_common(top_n) for cam, cnt in data.items()}


def top_iso(results, top_n: int, bins=DEFAULT_ISO_BINS):
    """Gets the top N most used ISO values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top ISO values to return.
        bins (tuple[int, ...]): ISO bins to use.

    Returns:
        list[tuple[int, int]]: List of (ISO, count) tuples.
    """
    counter = Counter()
    for r in results:
        if not r.iso:
            continue
        bucket = min(bins, key=lambda b: abs(b - r.iso))
        counter[bucket] += 1
    return counter.most_common(top_n)


def top_apertures(results, top_n: int):
    """Gets the top N most used aperture values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top aperture values to return.

    Returns:
        list[tuple[float, int]]: List of (aperture, count) tuples.
    """
    counter = Counter()
    for r in results:
        if r.aperture is None:
            continue
        counter[round(r.aperture, 1)] += 1
    return counter.most_common(top_n)


def top_shutter_speeds(results, top_n: int):
    """Gets the top N most used shutter speed values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top shutter speed values to return.

    Returns:
        list[tuple[float, int]]: List of (shutter speed, count) tuples.
    """
    counter = Counter()
    for r in results:
        if not r.shutter_speed:
            continue
        counter[r.shutter_speed] += 1
    return counter.most_common(top_n)
