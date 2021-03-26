import unittest

import yaml
from jsonasobj import as_json
from linkml_model import SchemaDefinition

from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, as_yaml
from tests.support.test_environment import TestEnvironmentTestCase
from tests.test_utils.environment import env


class YamlUtilTestCase(TestEnvironmentTestCase):
    env = env

    def test_dupcheck_loader(self):
        """ Make sure the duplicate checker finds duplicates """
        with open(env.input_path('yaml1.yaml')) as f:
            y1 = yaml.safe_load(f)
            self.assertEqual(17, y1['f1'])
        with open(env.input_path('yaml1.yaml')) as f:
            with self.assertRaises(ValueError):
                yaml.load(f, DupCheckYamlLoader)
        with open(env.input_path('yaml2.yaml')) as f:
            with self.assertRaises(ValueError):
                yaml.load(f, DupCheckYamlLoader)
        with open(env.input_path('schema1.yaml')) as f:
            s1 = yaml.load(f, DupCheckYamlLoader)
            self.assertEqual('schema1', s1['name'])

    def test_as_json(self):
        schema = yaml_loader.load(env.input_path('schema6.yaml'), SchemaDefinition)
        env.eval_single_file(env.expected_path('schema6.json'), as_json(schema), filtr=lambda s: s)


if __name__ == '__main__':
    unittest.main()