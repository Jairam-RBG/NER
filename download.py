from config import url
from utility import Regular_Expression
import os
import gdown
import os.path
import shutil


class Data:

    """
    Downloading the data and saving it in described folder.
    """

    def language_code(lang_choice):
        lang = ["ta", "ml", "mr", "te", "hi", "gu", "bn"]
        if lang_choice in lang:
            d = Data.data_download(lang_choice)
            Regular_Expression.extracting_zip(d, lang_choice)
        else:
            print("Invalid Language Choice")
        return 'done'

    def data_download(lang_choice):
        des_folder = "data/zip/"
        check_folder = os.path.isdir(des_folder)
        if check_folder:
            print("Directory Exists")
        else:
            os.makedirs(des_folder)

        data_files = os.listdir(des_folder)
        file_path = lang_choice + ".zip"
        file = os.path.isfile(file_path)
        if file:
            os.path.join(file_path)
            shutil.move(file_path, des_folder)
            print('File Exists and Moved to Destination Folder')

        elif file_path not in data_files:
            if lang_choice not in url.keys():
                print("File Exists")
            else:
                link = f"https://drive.google.com/uc?id={url.get(lang_choice)}"
                output = des_folder + lang_choice + '.zip'
                file = gdown.download(link, output, quiet=False)
        return file_path
