import os
from argparse import Namespace
from exif_analyzer.files_retriever import get_images

def test_get_images_finds_files(tmp_path):
    # Setup temporary directory structure
    d = tmp_path / "images"
    d.mkdir()
    f1 = d / "test1.ARW"
    f1.write_text("dummy")
    f2 = d / "test2.jpg"
    f2.write_text("dummy")
    
    sub = d / "subdir"
    sub.mkdir()
    f3 = sub / "test3.cr2"
    f3.write_text("dummy")
    
    # Extensions we are looking for
    args = Namespace(directory=str(d), extensions=[".arw", ".cr2"])
    
    got = get_images(args)
    
    assert len(got) == 2
    assert any(f.endswith("test1.ARW") for f in got)
    assert any(f.endswith("test3.cr2") for f in got)
    assert not any(f.endswith("test2.jpg") for f in got)

def test_get_images_skips_hidden_and_appledouble(tmp_path):
    d = tmp_path / "images"
    d.mkdir()
    f1 = d / "valid.arw"
    f1.write_text("dummy")
    f2 = d / ".hidden.arw"
    f2.write_text("dummy")
    
    apple_dir = d / ".AppleDouble"
    apple_dir.mkdir()
    f3 = apple_dir / "meta.arw"
    f3.write_text("dummy")
    
    args = Namespace(directory=str(d), extensions=[".arw"])
    got = get_images(args)
    
    assert len(got) == 1
    assert got[0].endswith("valid.arw")

def test_get_images_returns_none_if_empty(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    args = Namespace(directory=str(d), extensions=[".arw"])
    assert get_images(args) is None
