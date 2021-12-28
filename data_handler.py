import pandas as pd
from pandas.core.frame import DataFrame
import os


class DataHandler():
    
    def __init__(self, table_dictionary):
        self.table_dicts = table_dictionary

    def convert_tables(self) -> list[pd.DataFrame]:
        data_frames = []
        for key in self.table_dicts.keys():
            data_frame = pd.DataFrame(self.table_dicts[key])
            data_frame.name = key
            data_frames.append(data_frame)
        return data_frames

    def save_tables(self):
        df_list = self.convert_tables()
        for df in df_list:
            file_name = df.name.lower().replace(" ", "-")
            try:
                df.to_csv(f"results/{file_name}.csv", index=False)
            except FileNotFoundError:
                os.mkdir("results")
            finally:
                df.to_csv(f"results/{file_name}.csv", index=False)
