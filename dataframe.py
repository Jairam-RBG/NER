from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
import re
import pandas as pd


# setting up the cuda device
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0")
device = torch.device("cuda" if use_cuda else "cpu")
print("Device: ", device)


class Computing_Dataframe:

    def merging_dictionary_values(final_dict, lang_code):

        """
        :param final_dict: concatenated dictionary.
        :param lang_code: The initial language code passed i.e. ['ta','ml',...]
        :return: A dictionary in which the values are joined using '&&&'.
        """

        temp_dict = dict()
        for key, value in final_dict.items():
            temp_dict[key] = key
            value = "&&&".join(str(i) for i in value)
            temp_dict[key] = value
        Computing_Dataframe.initializing_dataframe(temp_dict, lang_code)

        return temp_dict

    def initializing_dataframe(temp_dict, lang_choice):

        """
        :param lang_choice: The initial language code passed i.e. ['ta','ml',...]
        :return: The initial dataframe
        """

        base_df = pd.DataFrame.from_dict(temp_dict.items())  # creating dataframe from dictionary
        base_df.columns = ["tag", "resource"]

        def non_english_words(word):
            result = re.findall(r"[A-Za-z0-9]+", word)
            return " ".join(result)

        base_df["is_english"] = base_df["tag"].apply(lambda x: "yes" if (x == non_english_words(x)) else "no")
        Computing_Dataframe.tag_translation(base_df, lang_choice)

        return base_df

    def tag_translation(base_df, lang_choice):

        """
        :param lang_choice: The initial language code passed i.e. ['ta','ml',...]
        :return: updated dataframe after translating the non-english tag name
        """

        model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
        tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
        model.to(device)

        def translation(word, lang_code):

            tokenizer.src_lang = lang_choice + "_IN"
            encoded_ln = tokenizer(word, return_tensors="pt").to(device)
            generated_tokens = model.generate(**encoded_ln)
            result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

            return result

        translation_list = []
        for i, j in zip(base_df["is_english"], base_df["tag"]):
            if i != "yes":
                translating_words = translation(j, lang_choice)
                translation_list.append(translating_words)
            else:
                translation_list.append(j)

        base_df["translated_tag"] = translation_list
        Computing_Dataframe.creating_dataframe(base_df, lang_choice)

    def creating_dataframe(base_df, lang_choice):

        base_df["translated_tag"] = base_df["translated_tag"].str.strip("[''.]")
        tag_res_dict = dict(zip(base_df.translated_tag, base_df.resource))
        tag_res_df = pd.DataFrame.from_dict(tag_res_dict.items())
        tag_res_df.columns = ["tags", "resource"]
        tag_res_df["short_resource"] = tag_res_df["resource"].astype(str).str.split("&&&").str[0:2]
        tag_res_df.drop("resource", axis=1, inplace=True)
        tag_res_df.to_csv(lang_choice + ".csv")

        return tag_res_df
