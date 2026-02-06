from .summaries import (
    top_focals,
    top_cameras,
    top_focals_by_camera,
    top_iso,
    top_apertures,
    top_shutter_speeds,
)


def build_summary(results, args):
    return {
        "focal_lengths": build_focal_lengths_summary(
            results, args.top_n, use_bucket=args.bucket_focals
        ),
        "cameras": build_cameras_summary(results, args.top_n),
        "camera_focal_lengths": build_camera_focal_lengths_summary(
            results, args.top_n, use_bucket=args.bucket_focals
        ),
        "isos": build_iso_summary(results, args.top_n),
        "apertures": build_aperture_summary(results, args.top_n),
        "shutter_speeds": build_shutter_speed_summary(results, args.top_n),
    }


def build_focal_lengths_summary(results, top_n: int, *, use_bucket: bool = False):
    """Returns a summary of the most used focal lengths.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top focal lengths to return.
        use_bucket (bool): Whether to bucket focal lengths.
    """
    rows = [
        {"focal_mm": fl, "count": count}
        for fl, count in top_focals(results, top_n, use_bucket=use_bucket)
    ]
    return rows


def build_cameras_summary(results, top_n: int):
    """Returns a summary of the most used cameras.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top cameras to return.
    """
    rows = [
        {"camera": cam, "count": count} for cam, count in top_cameras(results, top_n)
    ]
    return rows


def build_camera_focal_lengths_summary(
    results, top_n: int, *, use_bucket: bool = False
):
    """Returns a summary of the most used focal lengths for each camera.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top focal lengths to return.
        use_bucket (bool): Whether to bucket focal lengths.
    """
    rows = []
    data = top_focals_by_camera(results, top_n, use_bucket=use_bucket)
    for cam, items in data.items():
        rows.extend(
            [{"camera": cam, "focal_mm": fl, "count": count} for fl, count in items]
        )
    return rows


def build_iso_summary(results, top_n: int):
    """Returns a summary of the most used ISO values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top ISO values to return.
    """
    rows = [{"iso": iso, "count": count} for iso, count in top_iso(results, top_n)]
    return rows


def build_aperture_summary(results, top_n: int):
    """Returns a summary of the most used aperture values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top aperture values to return.
    """
    rows = [
        {"aperture": f"ƒ{ap}", "count": count}
        for ap, count in top_apertures(results, top_n)
    ]
    return rows


def build_shutter_speed_summary(results, top_n: int):
    """Returns a summary of the most used shutter speed values.

    Args:
        results (list[PhotoMetadata]): List of PhotoMetadata objects.
        top_n (int): Number of top shutter speed values to return.
    """
    rows = [
        {"shutter_speed": f"1/{int(s*10000)}", "count": count}
        for s, count in top_shutter_speeds(results, top_n)
    ]
    return rows
