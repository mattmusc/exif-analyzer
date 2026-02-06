import os
import logging

logger = logging.getLogger(__name__)


def get_images(args):
    """Get all image files recursively.

    Args:
        args (argparse.Namespace): Arguments to use for the analysis.

    Returns:
        list[str]: List of image file paths.
    """
    directory = args.directory
    image_extensions = tuple(
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in args.extensions
    )

    logger.debug(
        f"Searching for image files in {directory} with extensions {image_extensions}"
    )

    image_files = [
        os.path.join(root, f)
        for root, dirs, files in os.walk(directory)
        for f in files
        if f.lower().endswith(image_extensions)
        and not f.startswith(".")
        and ".AppleDouble" not in root
    ]

    if not image_files:
        logger.warning(
            f"No images found in {directory} with extensions {image_extensions}"
        )
        return

    logger.info(f"Found {len(image_files)} image files in {directory}")

    return image_files
