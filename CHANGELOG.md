# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2025-03-23

### Added
- Interactive progress indicator showing comparison progress, estimated time to completion, and processing speed
- Command line option `--no-progress` to disable progress bar display

## [0.1.0] - 2025-03-20

### Added
- Core directory comparison functionality, supporting detection of file content differences, missing files, and extra files
- Chunked hash comparison algorithm, optimized for handling large files
- Multi-process parallel processing support for improved performance
- Detailed text format results reporting
- HTML report generation feature, providing visual comparison results
- Cross-platform support (Windows, Linux, and MacOS)
- File and directory ignore pattern support
- Command line arguments for custom chunk size and worker process count
- Unit test suite verifying all functionality

### Optimized
- Performance optimization for small files, bypassing hash calculation
- Chunked processing for large files to avoid memory overflow
- File size checking before comparison to improve comparison speed

### Fixed
- None (first release)

## Future Plans
- Provide JSON format reporting
- Support for regular expression ignore patterns
- Add file timestamp comparison option 