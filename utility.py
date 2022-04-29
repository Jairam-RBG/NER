import glob
import re
from zipfile import ZipFile
from dataframe import Computing_Dataframe


class Regular_Expression:

    def extracting_zip(file, lang_code):

        """
        :param lang_code: The initial language code passed i.e. ['ta','ml',...]
        :rtype: text files
        """

        with ZipFile("data/zip/" + file, "r") as text_data:
            text_data.extractall("data/unzip")
            text_files = glob.glob(f"data/unzip/{lang_code}/*.txt", recursive=True)
            print(text_files)
            Regular_Expression.tag_resource_extraction(text_files, lang_code)

        return text_files

    def tag_resource_extraction(text_files, lang_code):

        """
        :param lang_code: The initial language code passed i.e. ['ta','ml',...]
        :param text_files: Extracted text files returns from the extracting zip function
        :return: returns list of dictionaries for text files
        """

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
                    resource_id, tags, resources = temp_data[0] + '>', temp_data[1], temp_data[2]
                    re_tag, re_resource = "dbpedia.org/property/([\w\W]+)", "[^[a-zA-Z\\'\"@#&,:;=.""]+"
                    keys = re.findall(re_tag, tags)
                    if not keys:
                        continue
                    key = keys[0]
                    values = re.findall(re_resource, resources)
                    value = " ".join([value for value in values if len(value.strip()) > 0])
                    if len(value) <= 1:
                        continue
                    if key not in initial_dict:
                        initial_dict[key] = [value + "<re_id>" + resource_id]
                    else:
                        initial_dict[key].append(value + "<re_id>" + resource_id)

                dict_list.append(initial_dict)
                Regular_Expression.combining_dictionaries(dict_list, lang_code)

        return dict_list, lang_code

    def combining_dictionaries(dict_list, lang_code):

        """
        :param lang_code: The initial language code passed i.e. ['ta','ml',...]
        :param dict_list: list of dictionaries returns from the tags_resource_extraction function
        :return: combines all dictionaries into one single dictionary
        """

        final_dict = dict()
        for dicts in dict_list:
            for key, value in dicts.items():
                if key not in final_dict:
                    final_dict[key] = value
                else:
                    final_dict[key].append(value)
        print(len(final_dict))
        Computing_Dataframe.merging_dictionary_values(final_dict, lang_code)

        return final_dict, lang_code
