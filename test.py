import unittest
import mock
import os

import valet as v


class TestAbstractRule(unittest.TestCase):
    def test_init(self):
        path = '~/Dropbox/Notes/tasks/Tasks.taskpaper'
        rule = v.Rule(path)
        fpath = os.path.expanduser(path)
        self.assertEquals(rule.fullpath, fpath)
        self.assertEquals(rule.extension, 'taskpaper')
        self.assertEquals(rule.name, 'Tasks')


class TestWhens(unittest.TestCase):
    def setUp(self):
        self.rule = v.Rule('~/Dropbox/Images/Me and i.png')

    def test_name_contains(self):
        self.assertTrue(self.rule.name_contains('me'))
        self.assertFalse(self.rule.name_contains('Images'))

    def test_name_contains_all(self):
        self.assertTrue(self.rule.name_contains_all('me', 'and', 'i'))
        self.assertFalse(self.rule.name_contains_all('me', 'and', 'cobalt'))

    def test_name_contains_any(self):
        self.assertTrue(self.rule.name_contains_any('me', 'and', 'i'))
        self.assertTrue(self.rule.name_contains_any('me', 'and', 'cobalt'))
        self.assertFalse(self.rule.name_contains_all('him'))

    def test_extension_in(self):
        self.assertTrue(self.rule.extension_in('png', 'jpg'))
        self.assertTrue(self.rule.is_image())
        self.assertFalse(self.rule.extension_in('mov', 'mp4'))


class TestWhats(unittest.TestCase):

    @mock.patch('valet.shutil')
    @mock.patch('valet.os.path.exists', lambda p: '3' not in p)
    @mock.patch('valet.os.makedirs')
    def test_move(self, mock_makedirs, mock_shutil):
        v.Rule('~/Desktop/vt/t.txt').move(
            '~/Desktop/vt/q'
        )
        mock_shutil.move.assert_called_with(
            os.path.expanduser('~/Desktop/vt/t.txt'),
            os.path.expanduser('~/Desktop/vt/q/t3.txt')
        )

    @mock.patch('valet.shutil')
    def test_rename(self, mock_shutil):
        v.Rule('~/Desktop/t.txt').rename(
            't2'
        )
        mock_shutil.move.assert_called_with(
            os.path.expanduser('~/Desktop/t.txt'),
            os.path.expanduser('~/Desktop/t2.txt')
        )

    @mock.patch('valet.shutil')
    @mock.patch('valet.os.path.getctime', lambda _: 0)
    def test_add_ctimestamp(self, mock_shutil):
        v.Rule('~/Desktop/t.txt').add_ctimestamp()
        mock_shutil.move.assert_called_with(
            os.path.expanduser('~/Desktop/t.txt'),
            os.path.expanduser('~/Desktop/1970-01-01 t.txt')
        )


class TestRunner(unittest.TestCase):
    @mock.patch('valet.os.listdir', lambda _: ['1.png', '2.png'])
    def test_run_paths(self):
        class MockRule(v.Rule):
            did_run_on = set()

            def do(self):
                self.did_run_on.add(self.fullpath)

        v.run_rules('~/dir/', ['~/dir2/3.txt'])
        self.assertEqual(
            MockRule.did_run_on,
            {
                os.path.expanduser('~/dir/1.png'),
                os.path.expanduser('~/dir/2.png'),
                os.path.expanduser('~/dir2/3.txt'),
            }
        )


if __name__ == '__main__':
    unittest.main()
