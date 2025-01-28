import os

def clean_temp_folder():
    temp_folder = os.environ.get('TEMP')
    if temp_folder:
        print(f"Cleaning Temp folder: {temp_folder}")
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
        print("Temp folder has been cleaned.")
    else:
        print("Temp folder not found.")

if __name__ == "__main__":
    clean_temp_folder()