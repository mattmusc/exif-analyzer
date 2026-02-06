def render_console(summary, args):
    print_focal_lengths_summary(summary, args)
    print()
    print_cameras_summary(summary, args)
    print()
    print_camera_focal_lengths_summary(summary, args)
    print()
    print_iso_summary(summary, args)
    print()
    print_aperture_summary(summary, args)
    print()
    print_shutter_speed_summary(summary, args)


def print_table(title, headers, rows, widths):
    """Prints a table with the given title, headers, rows, and widths.

    Args:
        title (str): Title of the table.
        headers (list[str]): List of headers.
        rows (list[list[str]]): List of rows.
        widths (list[int]): List of widths.
    """

    def fmt_row(cols):
        return " ".join(str(c).ljust(w) for c, w in zip(cols, widths))

    print(title)
    print("-" * (sum(widths) + (len(widths) - 1)))
    print(fmt_row(headers))
    print("-" * (sum(widths) + (len(widths) - 1)))
    for row in rows:
        print(fmt_row(row))
    print("-" * (sum(widths) + (len(widths) - 1)))


def print_focal_lengths_summary(summary, args):
    """Prints a summary of the most used focal lengths.

    Args:
        summary (dict): Summary of the most used focal lengths.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    rows = summary["focal_lengths"]
    rows = [[f'{x["focal_mm"]}mm', str(x["count"])] for x in rows]
    print_table(
        title=f"Top {args.top_n} Most Used Focal Lengths:",
        headers=["Focal Length", "Count"],
        rows=rows,
        widths=[15, 10],
    )


def print_cameras_summary(summary, args):
    """Prints a summary of the most used cameras.

    Args:
        summary (dict): Summary of the most used cameras.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    rows = summary["cameras"]
    rows = [[x["camera"], str(x["count"])] for x in rows]
    print_table(
        title=f"Top {args.top_n} Most Used Cameras:",
        headers=["Camera", "Count"],
        rows=rows,
        widths=[40, 10],
    )


def print_camera_focal_lengths_summary(summary, args):
    """Prints a summary of the most used focal lengths for each camera.

    Args:
        summary (dict): Summary of the most used focal lengths for each camera.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    data = summary["camera_focal_lengths"]
    rows = [[x["camera"], f"{x['focal_mm']}mm", str(x["count"])] for x in data]
    print_table(
        title=f"Top {args.top_n} Most Used Focal Lengths for each camera:",
        headers=["Camera", "Focal Length", "Count"],
        rows=rows,
        widths=[40, 15, 10],
    )


def print_iso_summary(summary, args):
    """Prints a summary of the most used ISO values.

    Args:
        summary (dict): Summary of the most used ISO values.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    rows = summary["isos"]
    rows = [[x["iso"], str(x["count"])] for x in rows]
    print_table(
        title=f"Top {args.top_n} Most Used ISO Values:",
        headers=["ISO", "Count"],
        rows=rows,
        widths=[15, 10],
    )


def print_aperture_summary(summary, args):
    """Prints a summary of the most used aperture values.

    Args:
        summary (dict): Summary of the most used aperture values.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    rows = summary["apertures"]
    rows = [[x["aperture"], str(x["count"])] for x in rows]
    print_table(
        title=f"Top {args.top_n} Most Used Aperture Values:",
        headers=["Aperture", "Count"],
        rows=rows,
        widths=[15, 10],
    )


def print_shutter_speed_summary(summary, args):
    """Prints a summary of the most used shutter speed values.

    Args:
        summary (dict): Summary of the most used shutter speed values.
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    rows = summary["shutter_speeds"]
    rows = [[x["shutter_speed"], str(x["count"])] for x in rows]
    print_table(
        title=f"Top {args.top_n} Most Used Shutter Speed Values:",
        headers=["Shutter Speed", "Count"],
        rows=rows,
        widths=[15, 10],
    )
