import pandas as pd
import glob


class Creating_Master_Dataframe:
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
        master_dataframe(final_df)

        return final_df


def master_dataframe(final_df):
    """
    :return: Returns the final master dataframe
    """

    temp_dict = dict(zip(final_df.resource_id, final_df.short_abstract))
    temp_df = pd.DataFrame.from_dict(temp_dict.items())
    temp_df.columns = ['resource_id', 'short_abstract']
    temp_df.to_csv('abstract_master.csv')

    return 'success'
