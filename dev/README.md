# Development Folder

This folder contains development and testing files that are excluded from the main project distribution but useful for development and debugging.

## Contents

### Test Scripts
- **`test_jinja2_conversion.py`** - Tests the Jinja2 template system conversion
- **`test_git_feature.py`** - Tests git-related functionality

### Usage

Run tests from the project root directory:

```bash
# Test Jinja2 conversion
python dev/test_jinja2_conversion.py

# Test git features
python dev/test_git_feature.py
```

### Development Notes

This folder is automatically excluded from:
- Git tracking (via `.gitignore`)
- Project packaging (not included in distribution)
- Generated project templates

Add any temporary development files, test scripts, or debugging tools here to keep the main project directory clean.
