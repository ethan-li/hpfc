#!/usr/bin/env python3
"""
Progress Bar Demo - Folder Compare Tool

This script demonstrates the progress bar functionality in the Folder Compare tool.
It creates two test directories with multiple files and performs a comparison,
showing the actual effect of the progress bar.
"""

import os
import sys
import tempfile
import shutil
import random

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.folder_compare.core import FolderCompare


def create_test_directories(num_files=100):
    """Create two directories with multiple test files for comparison"""
    print(f"Creating {num_files} test files in each directory...")
    dir1 = tempfile.mkdtemp(prefix="progress_demo_dir1_")
    dir2 = tempfile.mkdtemp(prefix="progress_demo_dir2_")
    
    # Create files with identical content
    for i in range(num_files // 2):
        with open(os.path.join(dir1, f"same_file_{i}.txt"), "w") as f:
            content = f"This is an identical file {i}\n" * 10
            f.write(content)
        with open(os.path.join(dir2, f"same_file_{i}.txt"), "w") as f:
            content = f"This is an identical file {i}\n" * 10
            f.write(content)
    
    # Create files with different content
    for i in range(num_files // 4):
        with open(os.path.join(dir1, f"diff_file_{i}.txt"), "w") as f:
            content = f"This is a different file in dir1 {i}\n" * 10
            f.write(content)
        with open(os.path.join(dir2, f"diff_file_{i}.txt"), "w") as f:
            content = f"This is a different file in dir2 {i}\n" * 10
            f.write(content)
    
    # Create files that only exist in dir1
    for i in range(num_files // 8):
        with open(os.path.join(dir1, f"only_dir1_{i}.txt"), "w") as f:
            content = f"This file only exists in dir1 {i}\n" * 5
            f.write(content)
    
    # Create files that only exist in dir2
    for i in range(num_files // 8):
        with open(os.path.join(dir2, f"only_dir2_{i}.txt"), "w") as f:
            content = f"This file only exists in dir2 {i}\n" * 5
            f.write(content)
    
    return dir1, dir2


def main():
    """Main function to demonstrate the progress bar functionality"""
    # Create directories with test files
    num_files = 50  # Fewer files for quick demonstration
    dir1, dir2 = create_test_directories(num_files)
    
    try:
        print("\n=== Using Progress Bar (Default) ===")
        print(f"Comparing directories with {num_files} files:")
        print(f"  Directory 1: {dir1}")
        print(f"  Directory 2: {dir2}")
        print()
        
        # Compare with progress bar (default behavior)
        comparer = FolderCompare(dir1, dir2, show_progress=True)
        results = comparer.compare()
        
        # Print summary
        print("\nComparison Summary:")
        print(f"  Identical files: {len(results['identical_files'])}")
        print(f"  Different files: {len(results['different_files'])}")
        print(f"  Missing files: {len(results['missing_files'])}")
        print(f"  Extra files: {len(results['extra_files'])}")
        
        print("\n=== Without Progress Bar ===")
        print(f"Comparing the same directories without progress bar:")
        
        # Compare without progress bar
        comparer = FolderCompare(dir1, dir2, show_progress=False)
        results = comparer.compare()
        
        # Print summary
        print("\nComparison Summary:")
        print(f"  Identical files: {len(results['identical_files'])}")
        print(f"  Different files: {len(results['different_files'])}")
        print(f"  Missing files: {len(results['missing_files'])}")
        print(f"  Extra files: {len(results['extra_files'])}")
        
    finally:
        # Clean up temporary directories
        print("\nCleaning up temporary directories...")
        shutil.rmtree(dir1, ignore_errors=True)
        shutil.rmtree(dir2, ignore_errors=True)
        print("Done!")


if __name__ == "__main__":
    main() 