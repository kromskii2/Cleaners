import os
import unittest
from unittest.mock import patch, MagicMock
from src.main import TempFolderCleaner

class TestCleanTempFolder(unittest.TestCase):

    @patch('src.main.os.environ.get')
    @patch('src.main.os.walk')
    @patch('src.main.os.remove')
    def test_clean_temp_folder(self, mock_remove, mock_walk, mock_get_env):
        # Настройка тестовой среды
        mock_get_env.return_value = '/mock/temp'
        mock_walk.return_value = [
            ('/mock/temp', ('subdir',), ('file1.txt', 'file2.txt')),
            ('/mock/temp/subdir', (), ('file3.txt',))
        ]

        cleaner = TempFolderCleaner()
        cleaner.clean_temp_folder()

        # Проверка, что os.remove был вызван для каждого файла
        mock_remove.assert_any_call('/mock/temp/file1.txt')
        mock_remove.assert_any_call('/mock/temp/file2.txt')
        mock_remove.assert_any_call('/mock/temp/subdir/file3.txt')
        self.assertEqual(mock_remove.call_count, 3)

    @patch('src.main.os.environ.get')
    @patch('src.main.os.walk')
    @patch('src.main.os.remove')
    def test_clean_temp_folder_with_errors(self, mock_remove, mock_walk, mock_get_env):
        # Настройка тестовой среды
        mock_get_env.return_value = '/mock/temp'
        mock_walk.return_value = [
            ('/mock/temp', ('subdir',), ('file1.txt', 'file2.txt')),
            ('/mock/temp/subdir', (), ('file3.txt',))
        ]
        mock_remove.side_effect = [None, Exception("Ошибка удаления"), None]

        cleaner = TempFolderCleaner()
        cleaner.clean_temp_folder()

        # Проверка, что os.remove был вызван для каждого файла и обработка ошибок
        mock_remove.assert_any_call('/mock/temp/file1.txt')
        mock_remove.assert_any_call('/mock/temp/file2.txt')
        mock_remove.assert_any_call('/mock/temp/subdir/file3.txt')
        self.assertEqual(mock_remove.call_count, 3)

    @patch('src.main.os.environ.get')
    def test_temp_folder_not_found(self, mock_get_env):
        # Настройка тестовой среды
        mock_get_env.return_value = None

        cleaner = TempFolderCleaner()
        with self.assertLogs(level='WARNING') as log:
            cleaner.clean_temp_folder()
            self.assertIn('Папка Temp не найдена.', log.output[0])

if __name__ == '__main__':
    unittest.main()