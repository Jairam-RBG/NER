import glob
import re
from zipfile import ZipFile
from dataframe import Constructing_Dataframe


class Regular_Expression:

    def extracting_zip(file, lang_choice):
        """
        :param lang_choice: The initial language code passed ['ta','ml',...]
        :rtype: text files
        """

        with ZipFile("data/zip/" + file, "r") as text_data:
            text_data.extractall("data/unzip")
            text_files = glob.glob(f"data/unzip/{lang_choice}/*.txt", recursive=True)
            print(text_files)
            Regular_Expression.tags_resource_extraction(text_files, lang_choice)
        return text_files

    def tags_resource_extraction(text_files, lang_choice):
        """
        :param lang_choice: The initial language code passed ['ta','ml',...]
        :param text_files: Extracted text files returns from the extracting zip function
        :return: returns list of dictionaries for text files
        """

        all_dict = []
        for text in text_files:
            initial_dict = {}
            with open(text, encoding='utf-8') as keyfile:
                keyword = ['@' + lang_choice]
                pattern = re.compile('|'.join(keyword))
                for line in keyfile:
                    if not pattern.search(line):
                        continue
                    temp_data = line.split('>')
                    res_id, tag, res = temp_data[0] + '>', temp_data[1], temp_data[2]
                    re_tag, re_res = "dbpedia.org/property/([\w\W]+)", "[^[a-zA-Z\\'\"@#&,:;=.""]+"
                    keys = re.findall(re_tag, tag)
                    if not keys:
                        continue
                    key = keys[0]
                    values = re.findall(re_res, res)
                    value = " ".join([value for value in values if len(value.strip()) > 0])
                    if len(value) <= 1:
                        continue
                    if key not in initial_dict:
                        initial_dict[key] = [value + "<re_id>" + res_id]
                    else:
                        initial_dict[key].append(value + "<re_id>" + res_id)

                all_dict.append(initial_dict)
                Regular_Expression.combining_dictionaries(all_dict, lang_choice)

        return all_dict, lang_choice

    def combining_dictionaries(all_dict, lang_choice):
        """
        :param lang_choice: The initial language code passed ['ta','ml',...]
        :param all_dict: list of dictionaries returns from the tags_resource_extraction function
        :return: combines all dictionaries into one single dictionary
        """

        final_dict = {}
        for dicts in all_dict:
            for key, value in dicts.items():
                if key not in final_dict:
                    final_dict[key] = value
                else:
                    final_dict[key].append(value)
        print(len(final_dict))
        Constructing_Dataframe.generating_dataframe(final_dict, lang_choice)
        return final_dict, lang_choice
