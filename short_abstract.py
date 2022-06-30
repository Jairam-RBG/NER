import os
import gdown
import os.path
import shutil
from config import short_abstract_url
import glob
import pandas as pd
import re
from zipfile import ZipFile
from dataframe import Computing_Dataframe


def language_choice(lang_code):
    lang_support = ["ta", "ml", "mr", "te", "hi", "gu", "bn"]
    if lang_code in lang_support:
        d = data_download(lang_code)
        reg = extracting_zip(d, lang_code)
    else:
        print("Invalid Language Choice")

    return 'done'


def data_download(lang_code):
    destination_folder = "data/short_abstract/zip/"
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
        if lang_code not in short_abstract_url.keys():
            print("File Exists")
        else:
            link = f"https://drive.google.com/uc?id={short_abstract_url.get(lang_code)}"
            output = destination_folder + lang_code + '.zip'
            file = gdown.download(link, output, quiet=False)

    return file_path


def extracting_zip(file, lang_code):
    with ZipFile("data/short_abstract/zip/" + file, "r") as text_data:
        text_data.extractall("data/short_abstract/unzip")
        text_files = glob.glob(f"data/short_abstract/unzip/{lang_code}/*.txt", recursive=True)
        print(text_files)
        tag_resource_extraction(text_files, lang_code)

    return text_files


def tag_resource_extraction(text_files, lang_code):
    dict_list = list()
    for text in text_files:
        initial_dict = dict()
        with open(text, encoding='utf-8') as keyfile:
            keyword = ['@' + lang_code]
            pattern = re.compile('|'.join(keyword))
            for line in keyfile:
                if not pattern.search(line):
                    continue
                temp_data = line.split('>')
                resource_id = temp_data[0] + '>'
                resource = temp_data[2]
                # res = re.sub(r"_]", "", resource, flags=re.I)
                initial_dict[resource_id] = resource
            dict_list.append(initial_dict)
            combining_dictionaries(dict_list, lang_code)


def combining_dictionaries(dict_list, lang_code):
    """
    :param lang_code: The initial language code passed i.e. ['ta','ml',...]
    :param dict_list: list of dictionaries returns from tag_resource_extraction function.
    :return: combines all dictionaries into one single dictionary.
    """

    final_dict = dict()
    for dicts in dict_list:
        for key, value in dicts.items():
            if key not in final_dict:
                final_dict[key] = [value]
            else:
                final_dict[key].append(value)
    dataframe(final_dict, lang_code)
    # Computing_Dataframe.merging_dictionary_values(final_dict, lang_code)


# def merging_dictionary_values(final_dict, lang_code):
#     """
#         :param final_dict: concatenated dictionary.
#         :param lang_code: The initial language code passed i.e. ['ta','ml',...]
#         :return: A dictionary in which the values are joined using '&&&'.
#         """
#
#     temp_dict = dict()
#     for key, value in final_dict.items():
#         temp_dict[key] = key
#         value = "&&&".join(str(i) for i in value)
#         temp_dict[key] = value
#     dataframe(temp_dict, lang_code)
#
#     return temp_dict


def dataframe(temp_dict, lang_code):
    df = pd.DataFrame(temp_dict.items(), columns=['resource_id', 'short_abstract'])
    # df["short_resource"] = df["short_abstract"].astype(str).str.split("&&&")
    # df['short_abstract'] = df['short_abstract'].astype(str).str.split('@ta')
    # df['short_abstract'] = df['short_abstract'].astype(str).str.replace('.\n', '', regex=True)
    # df['short_abstract'] = df['short_abstract'].astype(str).str.replace('[', '', regex=True)
    # df['short_abstract'] = df['short_abstract'].astype(str).str.replace('"', '', regex=True)
    # df['short_abstract'] = df['short_abstract'].astype(str).str.replace(']', '', regex=True)
    # df['short_abstract'] = df['short_abstract'].astype(str).str.replace('.\n', '')
    df.to_csv(lang_code + '.csv')


language_choice('te')
