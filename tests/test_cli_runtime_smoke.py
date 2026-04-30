import importlib.util
import os
import tempfile
import unittest


REQUIRED_CLI_MODULES = (
    'click',
    'colorama',
    'pandas',
    'psutil',
    'requests',
    'scipy',
    'torch',
)

missing_cli_modules = [
    module
    for module in REQUIRED_CLI_MODULES
    if importlib.util.find_spec(module) is None
]


@unittest.skipIf(
    bool(missing_cli_modules),
    "full CLI smoke requires runtime dependencies: " + ", ".join(missing_cli_modules),
)
class FullCLIRuntimeSmokeTests(unittest.TestCase):
    def test_manual_mlr_cli_smoke_runs_on_generated_data(self):
        from click.testing import CliRunner
        from tecpg.cli import cli

        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = runner.invoke(
                cli,
                [
                    '-r',
                    temp_dir,
                    '-t',
                    '1',
                    '--save-threads',
                    '2',
                    'init',
                    'smoke',
                    '-y',
                ],
                obj={},
            )
            self.assertEqual(result.exit_code, 0, result.output)

            root_dir = os.path.join(temp_dir, 'smoke')
            result = runner.invoke(
                cli,
                [
                    '-r',
                    root_dir,
                    '-t',
                    '1',
                    '--save-threads',
                    '2',
                    'data',
                    'dummy',
                    '-s',
                    '12',
                    '-m',
                    '4',
                    '-g',
                    '3',
                ],
                obj={},
            )
            self.assertEqual(result.exit_code, 0, result.output)

            result = runner.invoke(
                cli,
                [
                    '-r',
                    root_dir,
                    '-t',
                    '1',
                    '--save-threads',
                    '2',
                    'run',
                    'mlr',
                    '--all',
                    '-g',
                    '2',
                    '-m',
                    '2',
                    '--mlr-method',
                    'manual',
                ],
                obj={},
            )
            self.assertEqual(result.exit_code, 0, result.output)

            output_dir = os.path.join(root_dir, 'output')
            csv_outputs = [
                os.path.join(output_dir, name)
                for name in os.listdir(output_dir)
                if name.endswith('.csv')
            ]
            self.assertGreater(len(csv_outputs), 0)
            self.assertTrue(
                all(os.path.getsize(path) > 0 for path in csv_outputs)
            )


if __name__ == '__main__':
    unittest.main()
