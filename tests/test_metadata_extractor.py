import pytest
from unittest.mock import MagicMock, patch
from argparse import Namespace
from exif_analyzer.metadata_extractor import (
    chunked,
    extract_metadata_chunked,
    extract_metadata,
    PhotoMetadata,
)

def test_chunked():
    data = [1, 2, 3, 4, 5]
    chunks = list(chunked(data, 2))
    assert chunks == [[1, 2], [3, 4], [5]]
    
    assert list(chunked([], 2)) == []
    assert list(chunked([1], 10)) == [[1]]

@patch("exif_analyzer.metadata_extractor.ExifToolHelper")
def test_extract_metadata_chunked(mock_et_class):
    # Setup mock ExifToolHelper
    mock_et = mock_et_class.return_value.__enter__.return_value
    mock_et.get_tags.return_value = [
        {
            "SourceFile": "test1.jpg",
            "Make": "Canon",
            "Model": "5D3",
            "FocalLength": 50.0,
            "ScaleFactorTo35mmEquivalent": 1.0,
            "ISO": 100,
            "FNumber": 2.8,
            "ExposureTime": 0.01,
        },
        {
            "SourceFile": "test2.jpg",
            # Testing defaults for missing fields
        }
    ]
    
    args = Namespace(batch_size=10)
    files = ["test1.jpg", "test2.jpg"]
    
    results = extract_metadata_chunked(files, args)
    
    assert len(results) == 2
    
    # Check first image
    r1 = results[0]
    assert r1.make == "Canon"
    assert r1.focal_length == 50.0
    assert r1.iso == 100
    assert r1.aperture == 2.8
    assert r1.shutter_speed == 0.01
    
    # Check second image (defaults)
    r2 = results[1]
    assert r2.make == "Unknown"
    assert r2.model == "Unknown"
    assert r2.focal_length == 0.0
    assert r2.iso == 0
    assert r2.aperture == 0.0
    assert r2.shutter_speed == 0.0

def test_extract_metadata_chunked_focal_calc(mock_et_class=None): # using decorator inside
    with patch("exif_analyzer.metadata_extractor.ExifToolHelper") as mock_et_class:
        mock_et = mock_et_class.return_value.__enter__.return_value
        mock_et.get_tags.return_value = [{
            "FocalLength": 35.0,
            "ScaleFactorTo35mmEquivalent": 1.5,
        }]
        
        args = Namespace(batch_size=10)
        results = extract_metadata_chunked(["img.jpg"], args)
        assert results[0].focal_length == 52.5

@patch("exif_analyzer.metadata_extractor.ProcessPoolExecutor")
@patch("exif_analyzer.metadata_extractor.extract_metadata_chunked")
def test_extract_metadata_concurrency(mock_extract_chunk, mock_executor_class):
    # Mock executor and its context manager
    mock_executor = mock_executor_class.return_value.__enter__.return_value
    
    # Mock futures
    mock_future = MagicMock()
    mock_future.result.return_value = [PhotoMetadata("f1", "M1", "Mod1", 50.0, 100, 2.8, 0.01)]
    
    mock_executor.submit.return_value = mock_future
    
    # Mock as_completed to return our mock future
    with patch("exif_analyzer.metadata_extractor.as_completed", return_value=[mock_future]):
        args = Namespace(batch_size=1, threads=2)
        files = ["file1.jpg", "file2.jpg"]
        
        results = extract_metadata(files, args)
        
        assert len(results) == 1
        assert results[0].file == "f1"
        assert mock_executor.submit.call_count == 2
