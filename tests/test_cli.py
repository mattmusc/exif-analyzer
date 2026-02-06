import os
from exif_analyzer.cli import parse_args

def test_parse_args_defaults():
    args = parse_args([])
    assert args.directory == os.getcwd()
    assert args.top_n == 10
    assert args.extensions == [
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
    ]
    assert args.skip_table is True
    assert args.bucket_focals is True
    assert args.batch_size == 3000
    assert args.threads == 8
    assert args.quiet is False
    assert args.debug is False
    assert args.format == "console"
    assert args.output is None

def test_parse_args_custom_directory():
    args = parse_args(["/tmp/images"])
    assert args.directory == "/tmp/images"

def test_parse_args_top_n():
    args = parse_args(["-n", "5"])
    assert args.top_n == 5
    
    args = parse_args(["--top-n", "20"])
    assert args.top_n == 20

def test_parse_args_extensions():
    args = parse_args(["-e", ".jpg", ".png"])
    assert args.extensions == [".jpg", ".png"]

def test_parse_args_no_bucket_focals():
    args = parse_args(["--no-bucket-focals"])
    assert args.bucket_focals is False

def test_parse_args_format():
    args = parse_args(["--format", "json"])
    assert args.format == "json"

def test_parse_args_threads():
    args = parse_args(["--threads", "16"])
    assert args.threads == 16
