import os
import logging

class TempFolderCleaner:
    def __init__(self):
        self.temp_folder = os.environ.get('TEMP')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def clean_temp_folder(self):
        if self.temp_folder:
            logging.info(f"Очистка папки Temp: {self.temp_folder}")
            for root, dirs, files in os.walk(self.temp_folder):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        logging.error(f"Ошибка при удалении {file}: {e}")
            logging.info("Папка Temp очищена.")
        else:
            logging.warning("Папка Temp не найдена.")

if __name__ == "__main__":
    cleaner = TempFolderCleaner()
    cleaner.clean_temp_folder()