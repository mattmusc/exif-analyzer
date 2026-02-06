from exiftool import ExifToolHelper
from time import time
import os
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


@dataclass
class PhotoMetadata:
    """Dataclass to store photo metadata."""

    file: str
    make: str
    model: str
    focal_length: float
    iso: int
    aperture: float
    shutter_speed: float


TAGS = [
    "Make",
    "Model",
    "FocalLength",
    "ScaleFactorTo35mmEquivalent",
    "ISO",
    "FNumber",
    "ExposureTime",
]


def chunked(seq, size):
    """Chunks a sequence into smaller chunks.

    Args:
        seq (list): The sequence to chunk.
        size (int): The size of each chunk.

    Returns:
        list: List of chunks.
    """
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def extract_metadata_chunked(image_files, args) -> list[PhotoMetadata]:
    """Extract metadata from image files in chunks.

    Args:
        image_files (list[str]): List of image file paths.
        args (argparse.Namespace): Arguments to use for the analysis.

    Returns:
        list[PhotoMetadata]: List of PhotoMetadata objects.
    """
    results: list[PhotoMetadata] = []
    common_args = ["-fast2", "-n", "-q", "-q", "-m"]

    with ExifToolHelper(common_args=common_args) as et:
        for batch in chunked(image_files, args.batch_size):
            logger.debug(f"Processing batch of {len(batch)} images")
            metas = et.get_tags(batch, tags=TAGS)  # bulk pass

            for path, m in zip(batch, metas):
                make = m.get("Make", "Unknown")
                model = m.get("Model", "Unknown")

                fl = float(m.get("FocalLength", 0.0) or 0.0)
                sf = float(m.get("ScaleFactorTo35mmEquivalent", 1.0) or 1.0)
                fl35 = fl * sf

                iso = int(float(m.get("ISO", 0) or 0))
                aperture = float(m.get("FNumber", 0.0) or 0.0)
                shutter = float(m.get("ExposureTime", 0.0) or 0.0)

                results.append(
                    PhotoMetadata(
                        file=os.path.basename(path),
                        make=make,
                        model=model,
                        focal_length=fl35,
                        iso=iso,
                        aperture=aperture,
                        shutter_speed=shutter,
                    )
                )

    return results


def extract_metadata(image_files, args):
    """Extract metadata from image files using multiple processes.

    Args:
        image_files (list[str]): List of image file paths.
        args (argparse.Namespace): Arguments to use for the analysis.

    Returns:
        list[PhotoMetadata]: List of PhotoMetadata objects.
    """
    chunks = list(chunked(image_files, args.batch_size))
    all_rows = []

    logger.info(f"Processing {len(image_files)} images with {args.threads} threds...")
    start = time()

    with ProcessPoolExecutor(max_workers=args.threads) as ex:
        futures = [ex.submit(extract_metadata_chunked, ch, args) for ch in chunks]
        for f in as_completed(futures):
            all_rows.extend(f.result())

    logger.info(
        f"Processed {len(image_files)} image files in {time() - start:.2f} seconds"
    )

    return all_rows
