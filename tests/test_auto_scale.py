import ast
from pathlib import Path
import unittest


def load_auto_save_threads():
    cli_path = Path(__file__).resolve().parents[1] / 'tecpg' / 'cli.py'
    module = ast.parse(cli_path.read_text())
    function = next(
        node for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == '_auto_save_threads'
    )
    namespace = {}
    helper_module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    exec(compile(helper_module, str(cli_path), 'exec'), namespace)
    return namespace['_auto_save_threads']


class AutoSaveThreadsTests(unittest.TestCase):
    def test_auto_save_threads(self):
        auto_save_threads = load_auto_save_threads()

        # 16 GB / 8 physical cores -> 2
        self.assertEqual(auto_save_threads(8, 16.0), 2)

        # 512 GB / 32 physical cores -> 8
        self.assertEqual(auto_save_threads(32, 512.0), 8)

        # 1 TB / 128 physical cores -> 16 (capped)
        self.assertEqual(auto_save_threads(128, 1024.0), 16)

        # 8 GB / 4 physical cores -> 2 (floor)
        self.assertEqual(auto_save_threads(4, 8.0), 2)


if __name__ == '__main__':
    unittest.main()
