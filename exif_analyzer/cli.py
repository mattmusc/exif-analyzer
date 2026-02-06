import argparse
import os


def parse_args(args=None):
    """Creates a parser for command-line arguments.

    Args:
        args (list[str], optional): Arguments to parse. Defaults to None (sys.argv[1:]).

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract image metadata and display summaries."
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Directory to search (default: current directory)",
    )
    parser.add_argument(
        "-n",
        "--top-n",
        type=int,
        default=10,
        help="Number of top results to show (default: 10)",
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=[
            ".arw",
            ".cr2",
            ".cr3",
            ".dng",
            ".nef",
            ".orf",
            ".raf",
            ".rw2",
            ".sr2",
            ".srw",
        ],
        help="Image extensions to look for",
    )
    parser.add_argument(
        "--skip-table",
        default=True,
        action="store_true",
        help="Skip the full metadata table (default: True)",
    )
    parser.add_argument(
        "--bucket-focals",
        action="store_true",
        default=True,
        help="Group focal lengths into standard photographic buckets (default: on)",
    )
    parser.add_argument(
        "--no-bucket-focals",
        dest="bucket_focals",
        action="store_false",
        help="Use raw focal length values without bucketing",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=3000,
        help="Number of images to process in each batch (default: 3000)",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=8,
        help="Number of threads to use for processing (default: 8)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress all output (default: False)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug output (default: False)",
    )
    parser.add_argument(
        "--format",
        choices=["console", "json"],
        default="console",
        help="Output format (default: console)",
    )
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")

    return parser.parse_args(args)
