from steam_scraper import SteamScraper
from data_handler import DataHandler

ss = SteamScraper("https://steamdb.info")
data_dicts = ss.process_table_data()

dh = DataHandler(data_dicts)
df_list = dh.save_tables()
