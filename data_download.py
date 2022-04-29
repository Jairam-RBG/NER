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

    def language_choice(lang_code):

        lang_support = ["ta", "ml", "mr", "te", "hi", "gu", "bn"]
        if lang_code in lang_support:
            d = Data.data_download(lang_code)
            Regular_Expression.extracting_zip(d, lang_code)
        else:
            print("Invalid Language Choice")
        return 'done'

    def data_download(lang_code):

        destination_folder = "data/zip/"
        check_folder = os.path.isdir(destination_folder)

        if check_folder:
            print("Directory Exists")
        else:
            os.makedirs(destination_folder)

        data_files = os.listdir(destination_folder)
        file_path = lang_code + ".zip"
        file = os.path.isfile(file_path)

        if file:
            os.path.join(file_path)
            shutil.move(file_path, destination_folder)
            print('File Exists and Moved to Destination Folder')

        elif file_path not in data_files:
            if lang_code not in url.keys():
                print("File Exists")
            else:
                link = f"https://drive.google.com/uc?id={url.get(lang_code)}"
                output = destination_folder + lang_code + '.zip'
                file = gdown.download(link, output, quiet=False)
        return file_path
