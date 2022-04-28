import pandas as pd
import glob


class Master_Dataframe:

    """A class representing the master dataframe"""

    def merging_csv(files):
        """
        :param files: A directory consists all languages csv files.
        :return: Returns cancatenated dataframe.
        """

        file_extension = '.csv'
        filenames = [i for i in glob.glob(f"*{file_extension}")]
        print(filenames)
        final_df = pd.concat([pd.read_csv(f, delimiter=',') for f in filenames])
        final_df.drop('Unnamed: 0', axis=1, inplace=True)
        Master_Dataframe.tag_counts(final_df)
        return final_df

    def tag_counts(final_df):
        """
        :return: Dictionary representing the repeated tag names with the count.
        """

        count_dict = {}
        for tag in final_df['tags']:
            if tag not in count_dict:
                count_dict[tag] = 1
            else:
                count_dict[tag] = count_dict[tag] + 1
        Master_Dataframe.master_dataframe(count_dict, final_df)
        return count_dict

    def master_dataframe(count_dict, final_df):
        """
        :return: Returns the final master dataframe
        """

        count_df = pd.DataFrame.from_dict(count_dict.items())
        count_df.columns = ['tags', 'counts']
        temp_dict = dict(zip(final_df.tags, final_df.short_resource))
        temp_df = pd.DataFrame.from_dict(temp_dict.items())
        temp_df.columns = ['tags', 'resource']
        temp_df['counts'] = pd.Series(count_df['counts'])
        temp_df.to_csv('master.csv')
        print(len(temp_df))

        return 'success'
