"""Real-analyzer regression: member calls must not become Swift declarations."""
from pathlib import Path
import tempfile
import unittest

from tde_runtime.complexity import analyze


class SwiftAnalyzerBoundaryTests(unittest.TestCase):
    def test_delegating_initializer_keeps_both_declarations_and_following_method(self):
        source = '''class Example {
    convenience init() { self.init(value: 1) }
    init(value: Int) {
        if value > 0 { print(value) }
    }
    func following() { print("following") }
}
'''
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Example.swift').write_text(source, encoding='utf-8')
            result = analyze(root)
            self.assertEqual('VALID', result['status'], result.get('limitations'))
            symbols = result['symbols']
            self.assertEqual([(2, 2), (3, 5), (6, 6)],
                             [(item['line'], item['endLine']) for item in symbols])
            self.assertEqual([1, 2, 1], [item['complexity'] for item in symbols])

    def test_init_reference_and_member_call_do_not_swallow_later_method(self):
        source = '''struct Example {
    func mapValue(_ value: Int?) -> Example? {
        value.map(Example.init)
    }
    init(value: Int) { print(value) }
    func following() { print("following") }
}
'''
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Example.swift').write_text(source, encoding='utf-8')
            result = analyze(root)
            self.assertEqual('VALID', result['status'], result.get('limitations'))
            self.assertEqual([(2, 4), (5, 5), (6, 6)],
                             [(item['line'], item['endLine']) for item in result['symbols']])
