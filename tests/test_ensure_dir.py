import pytest
import os
import sys
from unittest.mock import patch


def ensure_directories():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    # Directories you want to create
    directories = [
        os.path.join(base_path, 'src/data/BlInMemory'),
        os.path.join(base_path, 'src/data/PreResize'),
        os.path.join(base_path, 'src/data/PostResize')
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# The test function
@patch('os.makedirs')  # Mock the os.makedirs call
@patch('os.path.exists', return_value=False)  # Mock os.path.exists to always return False
def test_ensure_directories(mock_exists, mock_makedirs):
    # Use patch.dict to safely modify sys._MEIPASS during the test
    with patch.dict(sys.__dict__, {'_MEIPASS': '/mock/base/path'}):
        # Call the function
        ensure_directories()

        # Directories to check
        mock_directories = [
            '/mock/base/path/src/data/BlInMemory',
            '/mock/base/path/src/data/PreResize',
            '/mock/base/path/src/data/PostResize'
        ]
        
        # Check that os.makedirs was called for each directory
        for directory in mock_directories:
            mock_makedirs.assert_any_call(directory)  # Ensure makedirs was called for each directory

        # Ensure makedirs was called the correct number of times (3 times in this case)
        assert mock_makedirs.call_count == len(mock_directories)
