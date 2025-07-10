# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Django application** that provides a production-ready Markdown Editor plugin for Django applications, based on the vditor editor. The project integrates modern web editor capabilities with Django's admin interface and model system.

**Key Architecture:**

- **Django Framework**: Python web framework with model-view-template architecture
- **Vditor Editor**: Modern markdown editor with WYSIWYG, IR, and SV modes
- **PDM Package Management**: Modern Python dependency management
- **Production Security**: Enhanced with file validation, content sanitization, and security best practices
- **Admin Integration**: Seamless integration with Django's admin interface
- **Field Types**: Custom model fields and form fields for markdown content

## Development Commands

```bash
# Install dependencies
pdm install

# Run development server
python manage.py runserver

# Run tests
pdm run test
# or
python manage.py test

# Code quality checks
pdm run lint          # Run flake8 linting
pdm run format        # Format code with black
pdm run format-check  # Check formatting without changes
pdm run typecheck     # Run mypy type checking

# Test coverage
pdm run coverage      # Run tests with coverage
pdm run coverage-report  # Generate coverage report
pdm run coverage-xml  # Generate XML coverage report

# Database operations
python manage.py makemigrations
python manage.py migrate

# Cache management
python manage.py vditor_cache warm   # Warm up caches
python manage.py vditor_cache clear  # Clear all caches
python manage.py vditor_cache info   # Check cache status
```

## Testing Requirements

Always run these commands after making changes:

```bash
# Essential checks before committing
pdm run test          # Must pass all tests
pdm run lint          # Must pass linting
pdm run typecheck     # Must pass type checking
pdm run format-check  # Must pass formatting check
```

## Project Structure

### Core Application (`vditor/`)

- **`fields.py`**: Custom Django model and form fields (VditorTextField, VditorTextFormField)
- **`widgets.py`**: Django admin widget implementation (VditorWidget)
- **`views.py`**: Upload handling and file processing views
- **`urls.py`**: URL routing for vditor endpoints
- **`configs.py`**: Configuration management and settings
- **`security.py`**: Security validation and file sanitization
- **`cache_utils.py`**: Performance optimization and caching utilities

### Demo Application (`vditor_app/`)

- **`models.py`**: Example model implementations
- **`forms.py`**: Example form implementations
- **`admin.py`**: Admin interface configuration
- **`views.py`**: Example view implementations

### Demo Project (`vditor_demo/`)

- **`settings.py`**: Django project settings
- **`urls.py`**: Main URL configuration
- **`wsgi.py`** / **`asgi.py`**: WSGI/ASGI application entry points

### Static Assets (`vditor/static/`)

- **`dist/`**: Built vditor editor assets (CSS, JavaScript)
- **Third-party dependencies**: KaTeX, highlight.js, mermaid, etc.

### Templates (`vditor/templates/`)

- **`widget.html`**: Admin widget template for the editor

## Architecture Details

### Django Integration

1. **Model Fields**: `VditorTextField` extends Django's TextField with markdown editor capabilities
2. **Form Fields**: `VditorTextFormField` provides form integration with validation
3. **Admin Widgets**: `VditorWidget` integrates with Django's admin interface
4. **Media Handling**: Automatic CSS/JS inclusion for editor functionality

### Security Features

- **File Validation**: Magic number detection, MIME type checking
- **Path Traversal Protection**: Secure filename sanitization
- **Content Scanning**: Dangerous pattern detection
- **Upload Limits**: Configurable file size and type restrictions
- **CSRF Protection**: Django's built-in CSRF protection

### Performance Optimizations

- **Configuration Caching**: Reduces repeated settings access
- **File Deduplication**: Content-based hashing to prevent duplicate uploads
- **LRU Caching**: Widget and media file caching
- **Atomic Operations**: Safe file uploads with rollback support

### Editor Features

- **Three Editing Modes**: WYSIWYG, Instant Rendering (IR), Split Screen Preview (SV)
- **Rich Content Support**: Mathematical formulas, diagrams, charts, multimedia
- **Toolbar Customization**: 36+ operations with full customization support
- **Upload Support**: Drag & drop, clipboard paste, real-time progress
- **Internationalization**: Chinese, English, Korean localization

## Configuration

### Basic Settings

```python
# settings.py
INSTALLED_APPS = [
    ...
    'vditor',
]

# Required for Django 3.0+
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'
```

### Advanced Configuration

```python
# Editor configuration
VDITOR_CONFIGS = {
    'default': {
        "width": "100%",
        "height": 360,
        "mode": "ir",  # sv, ir, wysiwyg
        "theme": "classic",  # classic, dark
        "icon": "ant",  # ant, material
        "outline": False,
        "typewriterMode": False,
        "debugger": False,
    }
}

# Security settings
VDITOR_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
VDITOR_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VDITOR_ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
}
```

## Development Guidelines

### Code Quality Standards

- **Type Safety**: Use type hints throughout the codebase
- **Security**: Validate all user inputs and file uploads
- **Performance**: Implement caching where appropriate
- **Testing**: Write comprehensive tests for all functionality
- **Documentation**: Document all public APIs and complex logic

### Django Best Practices

- **Model Design**: Use appropriate field types and validation
- **Admin Integration**: Provide intuitive admin interfaces
- **URL Patterns**: Use meaningful URL patterns with proper namespacing
- **Static Files**: Organize static assets properly
- **Templates**: Use Django's template inheritance

### Security Considerations

- **File Uploads**: Always validate file types and content
- **User Input**: Sanitize all user-provided content
- **Path Handling**: Prevent path traversal attacks
- **Error Handling**: Don't expose sensitive information in error messages

## Package Management

- **PDM**: Modern Python dependency management
- **Development Dependencies**: Includes testing, linting, and formatting tools
- **Production Dependencies**: Minimal runtime requirements (Django, werkzeug)

## Testing Strategy

### Test Structure

- **Unit Tests**: Test individual components (fields, widgets, security)
- **Integration Tests**: Test Django integration (admin, forms, models)
- **Security Tests**: Test file validation and sanitization
- **Performance Tests**: Test caching and optimization features

### Test Data

- **Fixtures**: Use Django fixtures for test data
- **Factories**: Consider using factory_boy for complex test data
- **Mocking**: Mock external dependencies and file system operations

## Deployment Considerations

### Production Settings

- **Security**: Enable all security features
- **Performance**: Configure caching appropriately
- **Static Files**: Use Django's static file handling
- **Database**: Configure appropriate database backend

### Static Asset Management

- **Collection**: Use `collectstatic` for production deployment
- **CDN**: Consider CDN for static assets in production
- **Compression**: Enable gzip compression for static files

## Error Handling

### Logging

- **Django Logging**: Use Django's logging framework
- **Security Events**: Log security-related events
- **Performance Metrics**: Log performance-critical operations
- **Error Tracking**: Implement proper error tracking

### User Experience

- **Graceful Degradation**: Provide fallbacks for JavaScript failures
- **Error Messages**: Show user-friendly error messages
- **Progress Indicators**: Show upload progress and status

## Internationalization

### Translation Support

- **Django i18n**: Use Django's internationalization framework
- **Editor Localization**: Vditor supports multiple languages
- **Admin Interface**: Ensure admin interface is translatable

## Browser Compatibility

- **Modern Browsers**: Supports all modern browsers
- **Mobile Support**: Responsive design for mobile devices
- **Accessibility**: Consider accessibility requirements

## Contributing Guidelines

### Code Style

- **Black**: Use black for code formatting
- **Flake8**: Follow flake8 linting rules
- **MyPy**: Use type hints and mypy checking
- **Imports**: Use isort for import organization

### Pull Request Process

1. Create feature branch from main
2. Implement changes with tests
3. Run all quality checks
4. Update documentation if needed
5. Submit pull request with clear description

### Release Process

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Run comprehensive tests
4. Build and test package
5. Create release tag
6. Publish to PyPI