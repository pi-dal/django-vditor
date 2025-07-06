## v1.1.3 (2025-01-06)

### Added
- **🚀 Production-Ready Enhancements by Vibe Coding**
  - Complete type hints for better IDE support and code safety
  - Comprehensive security enhancements with file validation and content sanitization
  - Multi-level caching system for improved performance
  - Enhanced error handling and logging throughout the codebase
  - Django management commands for cache operations (`vditor_cache`)
  - Security utilities module with file validation and path traversal protection
  - Performance optimizations with LRU caching and file deduplication

### Changed
- **🔧 Code Quality Improvements**
  - Formatted all code with Black for consistent style
  - Enhanced test suite with 31/31 tests passing
  - Improved error messages and user feedback
  - Updated README with comprehensive documentation and Vibe Coding attribution
  - Modernized CI/CD workflows with GitHub Actions best practices

### Security
- **🔒 Enhanced Security Features**
  - File upload validation with magic number detection
  - Content sanitization and dangerous pattern detection
  - Path traversal protection
  - Secure filename handling
  - Comprehensive logging for security events

### Performance
- **⚡ Performance Optimizations**
  - Configuration caching with LRU cache
  - File deduplication using content hashing
  - Atomic file operations for safe uploads
  - Cache invalidation strategies

### Infrastructure
- **🛠️ CI/CD Modernization**
  - Updated to use official `pdm-project/setup-pdm@v4` action
  - Added Python multi-version matrix testing (3.10, 3.11, 3.12)
  - Enabled dependency caching for faster builds
  - Added Codecov integration for coverage reporting
  - Implemented security scanning with safety
  - Created modern publishing workflow with PyPI Trusted Publishers
  - Added Dependabot configuration for automatic dependency updates
  - Support for both TestPyPI and PyPI publishing environments

### Requirements
- **📋 Updated Dependencies**
  - Minimum Python version: 3.10+
  - Minimum Django version: 5.2+
  - Updated coverage to 7.0+
  - Added safety, twine for development

## v1.1.2 (2022-08-30)

### Feat

- **Update vditor version to v3.8.17**

## v1.1.1 (2022-01-01)

### Feat

- **Update vditor version to v3.8.10**

### Fix

- **Update-CI/CD-file**: update pypi-release.yml

### Docs

- **README.md**: update README.md

## v1.1.0 (2021-08-01)

### Fix

- **Delete-the-redundant-dist-folder-under-vditor**: Delete vditor folder, simplify volume
- **Update-CI/CD-file**: Update workflow so git can override the dev branch
- **Update-CI/CD-file**: Make the dist folder not duplicate in CI/CD
- **Change-vditor-static-file-location**: Change dist to static/dist

## v1.0.1 (2021-08-01)
