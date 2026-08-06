import importlib
import sys
import unittest
from pathlib import Path


class RootImportTests(unittest.TestCase):
    def test_root_main_module_exposes_app(self):
        root = Path(__file__).resolve().parents[1]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        module = importlib.import_module("main")
        self.assertTrue(hasattr(module, "app"))


if __name__ == "__main__":
    unittest.main()
