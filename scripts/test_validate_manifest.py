#!/usr/bin/env python3
"""
Unit tests for manifest file validation.
"""

import unittest
import tempfile
import os
import sys
import shutil

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validate import validate_manifest


class TestValidateManifest(unittest.TestCase):
    """Test manifest file validation."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def write_manifest(self, filename, content):
        """Helper to write a manifest file."""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_valid_manifest(self):
        """Test a valid manifest file."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    notes: Test version
    matchers:
      - matcher_type: default
        severity: green
  "2.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: country
        matcher_value: US
        severity: yellow
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("valid.yml", content)
        errors = validate_manifest(filepath)
        self.assertEqual(errors, [])

    def test_invalid_yaml(self):
        """Test manifest with invalid YAML syntax."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
      invalid yaml here: [
"""
        filepath = self.write_manifest("invalid_yaml.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("YAML syntax error" in err for err in errors))

    def test_missing_versions_key(self):
        """Test manifest without 'versions' key."""
        content = """other_key:
  value: test
"""
        filepath = self.write_manifest("no_versions.yml", content)
        errors = validate_manifest(filepath)
        self.assertIn("Missing 'versions' key", errors)

    def test_invalid_semver_format(self):
        """Test manifest with invalid semantic version."""
        content = """versions:
  "1.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("invalid_semver.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("Invalid semantic version format" in err for err in errors))

    def test_invalid_semver_with_letters(self):
        """Test manifest with letters in version (should not crash)."""
        content = """versions:
  "a.b.c":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("letters_version.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("Invalid semantic version format: a.b.c" in err for err in errors))

    def test_invalid_semver_followed_by_valid(self):
        """Test invalid version followed by valid version (should not crash on comparison)."""
        content = """versions:
  "a.b.c":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "1.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("invalid_then_valid.yml", content)
        errors = validate_manifest(filepath)
        # Should report invalid format but not crash
        self.assertTrue(any("Invalid semantic version format: a.b.c" in err for err in errors))
        # Should not report ordering error since invalid version is skipped
        self.assertFalse(any("not in ascending order" in err for err in errors))

    def test_multiple_invalid_semvers(self):
        """Test multiple invalid versions (should not crash)."""
        content = """versions:
  "x.y.z":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "1.2":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "a.b.c":
    released_at: 2026-01-20T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("multiple_invalid.yml", content)
        errors = validate_manifest(filepath)
        # Should report all invalid formats
        self.assertTrue(any("Invalid semantic version format: x.y.z" in err for err in errors))
        self.assertTrue(any("Invalid semantic version format: 1.2" in err for err in errors))
        self.assertTrue(any("Invalid semantic version format: a.b.c" in err for err in errors))

    def test_valid_then_invalid_semver(self):
        """Test valid version followed by invalid version (should not crash)."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "invalid":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("valid_then_invalid.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("Invalid semantic version format: invalid" in err for err in errors))

    def test_mixed_valid_invalid_versions_ordering(self):
        """Test that ordering check only applies to valid versions."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "invalid":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "2.0.0":
    released_at: 2026-01-20T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("mixed_versions.yml", content)
        errors = validate_manifest(filepath)
        # Should report invalid format
        self.assertTrue(any("Invalid semantic version format: invalid" in err for err in errors))
        # Should not report ordering error (1.0.0 < 2.0.0 is correct)
        self.assertFalse(any("not in ascending order" in err for err in errors))

    def test_versions_not_ascending(self):
        """Test manifest with versions not in ascending order."""
        content = """versions:
  "2.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "1.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("not_ascending.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("not in ascending order" in err for err in errors))

    def test_semantic_version_ordering(self):
        """Test that semantic version comparison works (9.0.0 < 10.0.0)."""
        content = """versions:
  "9.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "10.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("semver_order.yml", content)
        errors = validate_manifest(filepath)
        self.assertEqual(errors, [])

    def test_missing_released_at(self):
        """Test manifest with missing released_at field."""
        content = """versions:
  "1.0.0":
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("no_released_at.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("missing 'released_at'" in err for err in errors))

    def test_invalid_iso8601(self):
        """Test manifest with invalid ISO 8601 timestamp."""
        content = """versions:
  "1.0.0":
    released_at: "not a timestamp"
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("invalid_timestamp.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid ISO 8601 timestamp" in err for err in errors))

    def test_missing_matchers(self):
        """Test manifest with missing matchers field."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
"""
        filepath = self.write_manifest("no_matchers.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("missing 'matchers'" in err for err in errors))

    def test_invalid_matcher_type(self):
        """Test manifest with invalid matcher type."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: invalid_type
        severity: green
"""
        filepath = self.write_manifest("invalid_matcher.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid matcher_type" in err for err in errors))

    def test_invalid_severity(self):
        """Test manifest with invalid severity value."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: invalid
"""
        filepath = self.write_manifest("invalid_severity.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid severity" in err for err in errors))

    def test_invalid_country_code(self):
        """Test manifest with invalid country code."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: country
        matcher_value: XX
        severity: green
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("invalid_country.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid country code" in err for err in errors))

    def test_invalid_location_hash(self):
        """Test manifest with invalid location hash."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: location_hash
        matcher_value: "invalid"
        severity: green
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("invalid_hash.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid location hash format" in err for err in errors))

    def test_missing_default_matcher(self):
        """Test manifest without default matcher."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: country
        matcher_value: US
        severity: green
"""
        filepath = self.write_manifest("no_default.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("missing default matcher" in err for err in errors))

    def test_file_not_found(self):
        """Test non-existent file returns error."""
        filepath = os.path.join(self.temp_dir, "nonexistent.yml")
        errors = validate_manifest(filepath)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Error reading file" in err for err in errors))

    def test_empty_versions_dict(self):
        """Test manifest with explicitly empty versions dict."""
        content = """versions: {}
"""
        filepath = self.write_manifest("empty_versions_dict.yml", content)
        errors = validate_manifest(filepath)
        self.assertIn("No versions defined", errors)

    def test_country_matcher_missing_value(self):
        """Test country matcher without matcher_value."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: country
        severity: green
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("country_no_value.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid country code" in err for err in errors))

    def test_location_hash_missing_value(self):
        """Test location_hash matcher without matcher_value."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: location_hash
        severity: green
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("hash_no_value.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid location hash format" in err for err in errors))

    def test_missing_severity(self):
        """Test matcher without severity field."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
"""
        filepath = self.write_manifest("no_severity.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid severity" in err for err in errors))

    def test_valid_manifest_all_matcher_types(self):
        """Test valid manifest with all three matcher types."""
        valid_hash = "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
        content = f"""versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    notes: Optional notes field
    matchers:
      - matcher_type: location_hash
        matcher_value: {valid_hash}
        severity: red
      - matcher_type: country
        matcher_value: US
        severity: yellow
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("all_matchers.yml", content)
        errors = validate_manifest(filepath)
        self.assertEqual(errors, [])

    def test_multiple_versions_with_errors(self):
        """Test manifest with multiple versions having different errors."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: invalid_severity
  "2.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: country
        matcher_value: XX
        severity: green
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("multi_errors.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(any("invalid severity" in err for err in errors))
        self.assertTrue(any("invalid country code" in err for err in errors))

    def test_versions_is_list_not_dict(self):
        """Test manifest where versions is a list instead of dict."""
        content = """versions:
  - "1.0.0"
  - "2.0.0"
"""
        filepath = self.write_manifest("versions_list.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(len(errors) > 0)

    def test_version_details_is_not_dict(self):
        """Test manifest with multiple versions having invalid details types."""
        content = """versions:
  "1.0.0": "string"
  "2.0.0": 456
  "3.0.0": null
"""
        filepath = self.write_manifest("multiple_invalid_details.yml", content)
        errors = validate_manifest(filepath)
        # Should report all invalid details
        self.assertTrue(any("1.0.0" in err and "not str" in err for err in errors))
        self.assertTrue(any("2.0.0" in err and "not int" in err for err in errors))
        self.assertTrue(any("3.0.0" in err and "not NoneType" in err for err in errors))

    def test_duplicate_versions(self):
        """Test manifest with same version appearing twice (YAML overwrites)."""
        # Note: YAML will overwrite duplicate keys, so only the last one remains
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
  "1.0.0":
    released_at: 2026-01-15T09:00:00Z
    matchers:
      - matcher_type: default
        severity: green
"""
        filepath = self.write_manifest("duplicate_version.yml", content)
        errors = validate_manifest(filepath)
        # YAML silently overwrites, so this should be valid (only one version remains)
        self.assertEqual(errors, [])

    def test_empty_file(self):
        """Test empty manifest file."""
        content = ""
        filepath = self.write_manifest("empty.yml", content)
        errors = validate_manifest(filepath)
        self.assertIn("Missing 'versions' key", errors)

    def test_null_versions(self):
        """Test manifest with null versions value."""
        content = """versions: null
"""
        filepath = self.write_manifest("null_versions.yml", content)
        errors = validate_manifest(filepath)
        self.assertIn("No versions defined", errors)

    def test_matchers_not_a_list(self):
        """Test manifest where matchers is not a list."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers: "not a list"
"""
        filepath = self.write_manifest("matchers_string.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(len(errors) > 0)

    def test_matcher_not_a_dict(self):
        """Test manifest where matcher entry is not a dict."""
        content = """versions:
  "1.0.0":
    released_at: 2026-01-10T09:00:00Z
    matchers:
      - "just a string"
      - 123
"""
        filepath = self.write_manifest("matcher_not_dict.yml", content)
        errors = validate_manifest(filepath)
        self.assertTrue(len(errors) > 0)


if __name__ == '__main__':
    unittest.main()

