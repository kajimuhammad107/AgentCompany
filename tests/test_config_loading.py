#!/usr/bin/env python3
"""Unit tests for configuration loading in the backend"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import after path setup
import app


class TestConfigurationLoading(unittest.TestCase):
    """Test suite for configuration loading functionality"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Create a temporary directory for test configs
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.test_dir, 'config')
        os.makedirs(self.config_dir, exist_ok=True)

        # Store original paths
        self.original_root_dir = app.ROOT_DIR
        self.original_config_dir = app.CONFIG_DIR
        self.original_org_config = app.ORGANIZATION_CONFIG_FILE
        self.original_status_config = app.STATUS_REGISTRY_CONFIG_FILE

        # Override paths to use test directory
        app.ROOT_DIR = self.test_dir
        app.CONFIG_DIR = self.config_dir
        app.ORGANIZATION_CONFIG_FILE = os.path.join(self.config_dir, "organization.json")
        app.STATUS_REGISTRY_CONFIG_FILE = os.path.join(self.config_dir, "status-registry.json")

    def tearDown(self):
        """Clean up after each test"""
        # Restore original paths
        app.ROOT_DIR = self.original_root_dir
        app.CONFIG_DIR = self.original_config_dir
        app.ORGANIZATION_CONFIG_FILE = self.original_org_config
        app.STATUS_REGISTRY_CONFIG_FILE = self.original_status_config

        # Remove temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_organization_config_success(self):
        """Test that organization.json loads correctly"""
        # Create test organization config
        test_org_data = {
            "departments": [
                {"id": "tech", "name": "Tech", "color": "#4A90E2"},
                {"id": "investment", "name": "Investment", "color": "#50C878"}
            ],
            "roles": [
                {"id": "spark", "name": "Spark", "title": "CEO", "departmentId": None, "avatar": "spark.png"},
                {"id": "forge", "name": "Forge", "title": "Tech Lead", "departmentId": "tech", "avatar": "forge.png"}
            ]
        }

        with open(app.ORGANIZATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(test_org_data, f, ensure_ascii=False, indent=2)

        # Load and verify
        result = app.load_organization_config()

        self.assertIsInstance(result, dict)
        self.assertIn("departments", result)
        self.assertIn("roles", result)
        self.assertEqual(len(result["departments"]), 2)
        self.assertEqual(len(result["roles"]), 2)
        self.assertEqual(result["departments"][0]["id"], "tech")
        self.assertEqual(result["roles"][0]["name"], "Spark")

    def test_load_status_registry_config_success(self):
        """Test that status-registry.json loads correctly"""
        # Create test status registry config
        test_status_data = {
            "idle": {
                "label": "空闲",
                "color": "#888",
                "icon": "💤",
                "animation": "idle"
            },
            "working": {
                "label": "工作中",
                "color": "#4A90E2",
                "icon": "💻",
                "animation": "typing"
            }
        }

        with open(app.STATUS_REGISTRY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(test_status_data, f, ensure_ascii=False, indent=2)

        # Load and verify
        result = app.load_status_registry_config()

        self.assertIsInstance(result, dict)
        self.assertIn("idle", result)
        self.assertIn("working", result)
        self.assertEqual(result["idle"]["label"], "空闲")
        self.assertEqual(result["working"]["color"], "#4A90E2")

    def test_load_organization_config_missing_file(self):
        """Test that missing organization.json returns default empty structure"""
        # Don't create the file
        result = app.load_organization_config()

        self.assertIsInstance(result, dict)
        self.assertIn("departments", result)
        self.assertIn("roles", result)
        self.assertEqual(result["departments"], [])
        self.assertEqual(result["roles"], [])

    def test_load_status_registry_config_missing_file(self):
        """Test that missing status-registry.json returns empty dict"""
        # Don't create the file
        result = app.load_status_registry_config()

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_load_organization_config_invalid_json(self):
        """Test error handling when organization.json has invalid JSON"""
        # Create invalid JSON file
        with open(app.ORGANIZATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")

        # Should return default structure on error
        result = app.load_organization_config()

        self.assertIsInstance(result, dict)
        self.assertIn("departments", result)
        self.assertIn("roles", result)
        self.assertEqual(result["departments"], [])
        self.assertEqual(result["roles"], [])

    def test_load_status_registry_config_invalid_json(self):
        """Test error handling when status-registry.json has invalid JSON"""
        # Create invalid JSON file
        with open(app.STATUS_REGISTRY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")

        # Should return empty dict on error
        result = app.load_status_registry_config()

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_load_organization_config_wrong_type(self):
        """Test error handling when organization.json contains wrong data type"""
        # Create file with array instead of object
        with open(app.ORGANIZATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(["not", "an", "object"], f)

        # Should return default structure
        result = app.load_organization_config()

        self.assertIsInstance(result, dict)
        self.assertEqual(result["departments"], [])
        self.assertEqual(result["roles"], [])

    def test_load_status_registry_config_wrong_type(self):
        """Test error handling when status-registry.json contains wrong data type"""
        # Create file with array instead of object
        with open(app.STATUS_REGISTRY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(["not", "an", "object"], f)

        # Should return empty dict
        result = app.load_status_registry_config()

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_backend_can_access_config_data(self):
        """Test that the backend can access configuration data"""
        # Create both config files
        org_data = {
            "departments": [{"id": "test", "name": "Test Dept", "color": "#000"}],
            "roles": [{"id": "tester", "name": "Tester", "title": "QA", "departmentId": "test", "avatar": "test.png"}]
        }
        status_data = {
            "testing": {"label": "测试中", "color": "#FFF", "icon": "🧪", "animation": "test"}
        }

        with open(app.ORGANIZATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(org_data, f)
        with open(app.STATUS_REGISTRY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(status_data, f)

        # Access both configs
        org_result = app.load_organization_config()
        status_result = app.load_status_registry_config()

        # Verify backend can access the data
        self.assertEqual(org_result["departments"][0]["id"], "test")
        self.assertEqual(org_result["roles"][0]["name"], "Tester")
        self.assertEqual(status_result["testing"]["label"], "测试中")

    def test_config_files_exist_in_real_project(self):
        """Test that actual config files exist in the project"""
        # Use original paths
        real_org_config = self.original_org_config
        real_status_config = self.original_status_config

        self.assertTrue(os.path.exists(real_org_config),
                       f"organization.json should exist at {real_org_config}")
        self.assertTrue(os.path.exists(real_status_config),
                       f"status-registry.json should exist at {real_status_config}")

    def test_real_config_files_are_valid_json(self):
        """Test that actual config files contain valid JSON"""
        # Use original paths
        real_org_config = self.original_org_config
        real_status_config = self.original_status_config

        # Test organization.json
        try:
            with open(real_org_config, 'r', encoding='utf-8') as f:
                org_data = json.load(f)
            self.assertIsInstance(org_data, dict)
            self.assertIn("departments", org_data)
            self.assertIn("roles", org_data)
        except json.JSONDecodeError as e:
            self.fail(f"organization.json contains invalid JSON: {e}")

        # Test status-registry.json
        try:
            with open(real_status_config, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
            self.assertIsInstance(status_data, dict)
        except json.JSONDecodeError as e:
            self.fail(f"status-registry.json contains invalid JSON: {e}")


if __name__ == '__main__':
    unittest.main()
