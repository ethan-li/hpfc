#!/usr/bin/env python3
"""
Basic usage examples for the folder-compare tool.
This script demonstrates how to use the folder-compare package in your own code.
"""

import os
import tempfile
import shutil
from folder_compare.core import compare_folders, generate_html_report

def create_test_directories():
    """Create temporary test directories with some files for comparison"""
    # Create temporary directory structure
    dir1 = tempfile.mkdtemp(prefix="example_dir1_")
    dir2 = tempfile.mkdtemp(prefix="example_dir2_")
    
    # Create subdirectories
    os.makedirs(os.path.join(dir1, "subdir1"), exist_ok=True)
    os.makedirs(os.path.join(dir2, "subdir1"), exist_ok=True)
    os.makedirs(os.path.join(dir2, "subdir2"), exist_ok=True)  # Extra directory in dir2
    
    # Create identical files
    with open(os.path.join(dir1, "same_file.txt"), "w") as f:
        f.write("This file is identical in both directories")
    with open(os.path.join(dir2, "same_file.txt"), "w") as f:
        f.write("This file is identical in both directories")
    
    # Create files with different content
    with open(os.path.join(dir1, "different_file.txt"), "w") as f:
        f.write("Content in directory 1")
    with open(os.path.join(dir2, "different_file.txt"), "w") as f:
        f.write("Content in directory 2 is different")
    
    # Create file only in dir1
    with open(os.path.join(dir1, "only_in_dir1.txt"), "w") as f:
        f.write("This file exists only in directory 1")
    
    # Create file only in dir2
    with open(os.path.join(dir2, "only_in_dir2.txt"), "w") as f:
        f.write("This file exists only in directory 2")
    
    # Create identical files in subdirectory
    with open(os.path.join(dir1, "subdir1", "subdir_same.txt"), "w") as f:
        f.write("This subdirectory file is identical")
    with open(os.path.join(dir2, "subdir1", "subdir_same.txt"), "w") as f:
        f.write("This subdirectory file is identical")
    
    return dir1, dir2

def example_basic_comparison():
    """Basic comparison example"""
    print("=== Basic Comparison Example ===")
    dir1, dir2 = create_test_directories()
    
    try:
        print(f"Comparing directories:\n  {dir1}\n  {dir2}\n")
        
        # Perform comparison with default settings
        result = compare_folders(dir1, dir2)
        
        # Print comparison summary
        print("Comparison Summary:")
        print(f"  Total files in dir1: {len(result.dir1_files)}")
        print(f"  Total files in dir2: {len(result.dir2_files)}")
        print(f"  Identical files: {len(result.identical_files)}")
        print(f"  Different files: {len(result.different_files)}")
        print(f"  Missing files (in dir2): {len(result.missing_files)}")
        print(f"  Extra files (in dir2): {len(result.extra_files)}")
        
        # Print detailed results
        if result.different_files:
            print("\nFiles with different content:")
            for path in result.different_files:
                print(f"  - {path}")
        
        if result.missing_files:
            print("\nFiles missing from dir2:")
            for path in result.missing_files:
                print(f"  - {path}")
        
        if result.extra_files:
            print("\nExtra files in dir2:")
            for path in result.extra_files:
                print(f"  - {path}")
    finally:
        # Clean up temporary directories
        shutil.rmtree(dir1)
        shutil.rmtree(dir2)

def example_html_report():
    """Generate an HTML report example"""
    print("\n=== HTML Report Example ===")
    dir1, dir2 = create_test_directories()
    
    try:
        print(f"Comparing directories:\n  {dir1}\n  {dir2}")
        
        # Perform comparison
        result = compare_folders(dir1, dir2)
        
        # Generate HTML report
        report_path = "comparison_report.html"
        generate_html_report(result, dir1, dir2, report_path)
        
        print(f"\nHTML report generated: {os.path.abspath(report_path)}")
        print("You can open this file in a web browser to view the detailed comparison report.")
    finally:
        # Clean up temporary directories
        shutil.rmtree(dir1)
        shutil.rmtree(dir2)

def example_with_custom_settings():
    """Example with custom comparison settings"""
    print("\n=== Custom Settings Example ===")
    dir1, dir2 = create_test_directories()
    
    try:
        print(f"Comparing directories with custom settings:\n  {dir1}\n  {dir2}")
        
        # Custom comparison with larger chunk size and ignore pattern
        result = compare_folders(
            dir1, 
            dir2,
            chunk_size=1024 * 1024,  # 1MB chunks
            workers=2,               # Use 2 worker processes
            ignore=["only_in"]       # Ignore files containing "only_in" in their name
        )
        
        print("\nComparison Summary (ignoring files with 'only_in' in their name):")
        print(f"  Identical files: {len(result.identical_files)}")
        print(f"  Different files: {len(result.different_files)}")
        print(f"  Missing files (in dir2): {len(result.missing_files)}")
        print(f"  Extra files (in dir2): {len(result.extra_files)}")
    finally:
        # Clean up temporary directories
        shutil.rmtree(dir1)
        shutil.rmtree(dir2)

if __name__ == "__main__":
    example_basic_comparison()
    example_html_report()
    example_with_custom_settings()
    
    print("\nAll examples completed. If you created an HTML report, you can open it in a web browser.") 