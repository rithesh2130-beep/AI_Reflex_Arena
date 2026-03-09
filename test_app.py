import unittest
from streamlit.testing.v1 import AppTest
import os

class TestStreamlitApp(unittest.TestCase):
    def test_landing_page(self):
        at = AppTest.from_file("reflex_dashboard.py", default_timeout=15).run()
        self.assertFalse(at.exception, f"App crashed: {at.exception}")

    def test_virtual_arena(self):
        at = AppTest.from_file(os.path.join("pages", "1_🎮_Virtual_Arena.py"), default_timeout=15).run()
        self.assertFalse(at.exception, f"App crashed: {at.exception}")

    def test_analytics(self):
        at = AppTest.from_file(os.path.join("pages", "2_📊_Analytics.py"), default_timeout=15).run()
        self.assertFalse(at.exception, f"App crashed: {at.exception}")

    def test_hardware_arena(self):
        at = AppTest.from_file(os.path.join("pages", "3_⚙️_Hardware_Arena.py"), default_timeout=15).run()
        self.assertFalse(at.exception, f"App crashed: {at.exception}")

if __name__ == '__main__':
    unittest.main()
