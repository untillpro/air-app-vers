#!/usr/bin/env python3
"""
Notes file validation functions.

Validation checks for notes:
- YAML syntax is valid
- File name matches pattern {app}--{version}.yml
- App name in filename exists in config.yml
- Version in filename is valid semantic version
- At least one locale entry exists
- All locale names are defined in config.yml
- No duplicate locale entries in same notes file
- en-en locale is present (required for fallback)
- Each locale has non-empty notes field
- Notes text length is within limits (min 1, max 500 characters)
"""

import re
import yaml

# Notes validation constants
NOTES_MIN_LENGTH = 1
NOTES_MAX_LENGTH = 500
REQUIRED_LOCALE = 'en-en'


def validate_notes_filename(filename):
    """Validate notes filename matches pattern {app}--{version}.yml.

    Returns tuple (app_name, version) if valid, (None, None) if invalid.
    """
    pattern = r'^([a-z]+)--(\d+\.\d+\.\d+)\.yml$'
    match = re.match(pattern, filename)
    if match:
        return match.group(1), match.group(2)
    return None, None


def validate_notes_file(filepath, valid_locales):
    """Validate a single notes file.

    Args:
        filepath: Path to the notes file
        valid_locales: Set of valid locale names from config.yml

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML syntax error: {e}"]
    except Exception as e:
        return [f"Error reading file: {e}"]

    if not data or 'locales' not in data:
        return ["Missing 'locales' key"]

    locales = data['locales']
    if not isinstance(locales, list):
        return ["'locales' must be a list"]

    if not locales:
        return ["At least one locale entry is required"]

    seen_locales = set()
    has_required_locale = False

    for i, entry in enumerate(locales):
        if not isinstance(entry, dict):
            errors.append(f"Locale entry {i}: must be an object")
            continue

        # Validate locale name
        locale_name = entry.get('name')
        if not locale_name:
            errors.append(f"Locale entry {i}: missing 'name' field")
            continue

        if not isinstance(locale_name, str):
            errors.append(f"Locale entry {i}: 'name' must be a string")
            continue

        # Check for duplicates
        if locale_name in seen_locales:
            errors.append(f"Duplicate locale entry: {locale_name}")
        seen_locales.add(locale_name)

        # Check if locale is defined in config
        if locale_name not in valid_locales:
            errors.append(f"Locale '{locale_name}' not defined in config.yml")

        # Check for required locale
        if locale_name == REQUIRED_LOCALE:
            has_required_locale = True

        # Validate notes field
        notes = entry.get('notes')
        if notes is None:
            errors.append(f"Locale '{locale_name}': missing 'notes' field")
            continue

        if not isinstance(notes, str):
            errors.append(f"Locale '{locale_name}': 'notes' must be a string")
            continue

        notes_length = len(notes)
        if notes_length < NOTES_MIN_LENGTH:
            errors.append(f"Locale '{locale_name}': notes cannot be empty")
        elif notes_length > NOTES_MAX_LENGTH:
            errors.append(f"Locale '{locale_name}': notes exceeds {NOTES_MAX_LENGTH} characters ({notes_length})")

    if not has_required_locale:
        errors.append(f"Missing required locale '{REQUIRED_LOCALE}' (needed for fallback)")

    return errors

