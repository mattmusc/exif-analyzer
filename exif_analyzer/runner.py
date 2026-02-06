import logging

from .cli import parse_args
from .files_retriever import get_images
from .metadata_extractor import extract_metadata
from .summaries_builders import build_summary
from .summaries_emitter import emit_summary

logger = logging.getLogger(__name__)


def run(args):
    """Main function to extract information from raw images and display summaries.

    Args:
        args (argparse.Namespace): Arguments to use for the analysis.
    """
    image_files = get_images(args)

    if not image_files:
        # logged warning in get_images function
        return

    metadata_list = extract_metadata(image_files, args)

    if args.quiet:
        return metadata_list

    report = build_summary(metadata_list, args)
    emit_summary(report, args)


def main():
    """Main function to parse arguments and run the analysis."""
    args = parse_args()
    level = (
        logging.WARNING
        if args.quiet
        else (logging.DEBUG if args.debug else logging.INFO)
    )
    logging.basicConfig(level=level, format="%(levelname)s %(message)s", force=True)
    run(args)
