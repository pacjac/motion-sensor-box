import unittest
import os

from numpy import who

from msb_config.MSBConfig import MSBConfig

from msb_fusionlog.FusionlogConfig import FusionlogConfig


class TestConfig(unittest.TestCase):
    def test_correct_env(self):
        env_varname = "MSB_CONFIG_DIR"
        self.assertIn(env_varname, os.environ)

    def test_can_import(self):
        config = MSBConfig()



class TestFusionLogConfig(unittest.TestCase):
    def setUp(self):
        env_varname = "MSB_CONFIG_DIR"

        here = os.path.dirname(os.path.abspath(__file__))
        self.expected_config_dir = os.path.join(here, "config") 

        os.environ[env_varname] = self.expected_config_dir

        self.config = FusionlogConfig()

    def test_correct_env(self):
        env_varname = "MSB_CONFIG_DIR"
        self.assertIn(env_varname, os.environ)
        self.assertEqual(self.expected_config_dir, os.environ[env_varname])

    def test_creates_config_dir(self):
        data_path = os.path.join(os.getcwd(), "test/msb_data")
        self.assertTrue(os.path.exists(data_path))
