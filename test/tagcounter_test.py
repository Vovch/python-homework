import argparse
import unittest
from unittest.mock import patch, Mock, ANY

from tagcounter import tagcounter


class TestTagcounter(unittest.TestCase):
    @patch('tagcounter.tagcounter.view')
    @patch('tagcounter.tagcounter.save')
    @patch('tagcounter.tagcounter.argparse.ArgumentParser')
    def test_arguments(self, parser, save, view):
        add_arg = Mock()
        parser.return_value.add_argument = add_arg

        tagcounter.main()

        add_arg.assert_called_with('--view', help=ANY)

    @patch('tagcounter.tagcounter.view')
    @patch('tagcounter.tagcounter.save')
    @patch('tagcounter.tagcounter.argparse.ArgumentParser')
    def test_call_save(self, parser, save, view):
        parser.return_value.parse_args = Mock(return_value=argparse.Namespace(get='youtube.com', view=''))

        tagcounter.main()

        save.assert_called_with('youtube.com')

    @patch('tagcounter.tagcounter.view')
    @patch('tagcounter.tagcounter.save')
    @patch('tagcounter.tagcounter.argparse.ArgumentParser')
    def test_call_view(self, parser, save, view):
        parser.return_value.parse_args = Mock(return_value=argparse.Namespace(get='', view='youtube.com'))

        tagcounter.main()

        view.assert_called_with('youtube.com')

    @patch('tagcounter.tagcounter.view')
    @patch('tagcounter.tagcounter.save')
    @patch('tagcounter.tagcounter.argparse.ArgumentParser')
    def test_get_symomyms(self, parser, save, view):
        parser.return_value.parse_args = Mock(return_value=argparse.Namespace(get='ydx', view=''))

        tagcounter.main()

        save.assert_called_with('yandex.ru')

    @patch('tagcounter.tagcounter.view')
    @patch('tagcounter.tagcounter.save')
    @patch('tagcounter.tagcounter.argparse.ArgumentParser')
    def test_view_symomyms(self, parser, save, view):
        parser.return_value.parse_args = Mock(return_value=argparse.Namespace(get='', view='ggl'))

        tagcounter.main()

        view.assert_called_with('google.com')


class TestSave(unittest.TestCase):
    @patch('tagcounter.tagcounter.datetime')
    @patch('tagcounter.tagcounter.get_site_name')
    @patch('tagcounter.tagcounter.get_address')
    @patch('tagcounter.tagcounter.parse_site')
    @patch('tagcounter.tagcounter.db')
    def test_save(self, db, parse_site, get_address, get_site_name, datetime):
        datetime.now.return_value = 'now'
        get_address.return_value = 'get_address'
        get_site_name.return_value = 'get_site_name'
        parse_site.return_value = 'link'
        add_info_mock = Mock()
        db.add_info = add_info_mock

        tagcounter.save('initial_link')

        add_info_mock.assert_called_with('get_address', 'get_site_name', 'now', 'link')


class TestView(unittest.TestCase):
    @patch('tagcounter.tagcounter.db')
    def test_save(self, db):
        tagcounter.view('view_link')

        db.view_info.assert_called_with('view_link')


class TestParseSite(unittest.TestCase):
    @patch('tagcounter.tagcounter.get_address')
    @patch('tagcounter.tagcounter.urllib.request.urlopen')
    def test_save(self, urlopen, get_address):
        get_address.return_value = 'get_address'
        urlopen.return_value.__enter__.return_value.read.return_value = '<div><span class="test"></span></div>'

        result = tagcounter.parse_site('view_link')

        self.assertEqual(result, '{"div": 1, "span": 1}')


if __name__ == '__main__':
    unittest.main()
