from unittest.mock import patch, MagicMock
from argparse import Namespace
import logging
from exif_analyzer.runner import run, main

def test_run_no_images():
    args = Namespace(quiet=False)
    with patch("exif_analyzer.runner.get_images", return_value=[]):
        # Should return early
        assert run(args) is None

def test_run_with_images():
    args = Namespace(quiet=False)
    metadata_list = [MagicMock()]
    report = {"data": "test"}
    
    with patch("exif_analyzer.runner.get_images", return_value=["img1.jpg"]), \
         patch("exif_analyzer.runner.extract_metadata", return_value=metadata_list), \
         patch("exif_analyzer.runner.build_summary", return_value=report) as mock_build, \
         patch("exif_analyzer.runner.emit_summary") as mock_emit:
        
        run(args)
        
        mock_build.assert_called_once_with(metadata_list, args)
        mock_emit.assert_called_once_with(report, args)

def test_run_quiet_mode():
    args = Namespace(quiet=True)
    metadata_list = [MagicMock()]
    
    with patch("exif_analyzer.runner.get_images", return_value=["img1.jpg"]), \
         patch("exif_analyzer.runner.extract_metadata", return_value=metadata_list), \
         patch("exif_analyzer.runner.build_summary") as mock_build:
        
        result = run(args)
        
        assert result == metadata_list
        mock_build.assert_not_called()

def test_main_orchestration():
    args = Namespace(quiet=False, debug=False)
    
    with patch("exif_analyzer.runner.parse_args", return_value=args), \
         patch("exif_analyzer.runner.run") as mock_run, \
         patch("logging.basicConfig") as mock_logging:
        
        main()
        
        mock_logging.assert_called_once()
        mock_run.assert_called_once_with(args)

def test_main_debug_logging():
    args = Namespace(quiet=False, debug=True)
    
    with patch("exif_analyzer.runner.parse_args", return_value=args), \
         patch("exif_analyzer.runner.run"), \
         patch("logging.basicConfig") as mock_logging:
        
        main()
        # Check if level is DEBUG (10)
        # basicConfig is called with multiple args, we check the 'level' kwarg
        called_args, called_kwargs = mock_logging.call_args
        assert called_kwargs['level'] == logging.DEBUG
