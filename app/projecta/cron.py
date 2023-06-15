from project_a.settings import MEDIA_ROOT
import os


def delete_excel_files():
    dir = os.path.join(MEDIA_ROOT, 'excel')
    for file in os.scandir(dir):
        os.remove(file.path)

    return None
