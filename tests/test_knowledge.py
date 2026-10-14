import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from portable.knowledge import KnowledgeIndex


class KnowledgeTests(unittest.TestCase):
    def test_index_retrieve_and_reload_chinese_english(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'documents'; source.mkdir()
            (source / 'thermal.md').write_text('封裝的熱阻量測須定義接面溫度、環境條件以及功率；比較兩個散熱方案時必須使用相同邊界條件。', encoding='utf-8')
            (source / 'bonding.txt').write_text('Hybrid bonding requires accurate alignment and control of contamination. Inspect the bonding interface before evaluating electrical continuity.')
            (source / '.secrets.md').write_text('This hidden file must never enter the local reference index.')
            output = root / 'index.json'
            tool = Path(__file__).resolve().parents[1] / 'tools/index-documents.py'
            result = subprocess.run([sys.executable, str(tool), '--source', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(output.read_text())['documents']), 2)
            retriever = KnowledgeIndex(output)
            self.assertEqual(retriever.search('封裝的熱阻量測')[0]['source'], 'thermal.md')
            self.assertEqual(retriever.search('hybrid bonding alignment')[0]['source'], 'bonding.txt')
            self.assertEqual(retriever.search('steam locomotive piston'), [])
            output.write_text('{bad json')
            self.assertEqual(retriever.search('hybrid bonding'), [])

    def test_empty_import_preserves_previous_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'empty'; source.mkdir()
            output = root / 'index.json'; output.write_text('previous index')
            tool = Path(__file__).resolve().parents[1] / 'tools/index-documents.py'
            result = subprocess.run([sys.executable, str(tool), '--source', str(source), '--output', str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'previous index')

    def test_valid_json_with_invalid_shape_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'index.json'
            retriever = KnowledgeIndex(path)
            for doc in [[], 'not an index', None, {'version': 1, 'chunks': 'invalid'},
                        {'version': 1, 'chunks': [{'source': 'a' * 501, 'page': 1, 'text': 'thermal bonding alignment'}]},
                        {'version': 1, 'chunks': [{'source': 'course.pdf', 'page': {'bad': 'page'}, 'text': 'thermal bonding alignment'}]}]:
                path.write_text(json.dumps(doc))
                self.assertEqual(retriever.search('thermal bonding'), [])
