import pandas as pd
from datetime import datetime
import os

from dart_crawling import dart_crawling
from kind_crawling import kind_crawling


def load_datas():
    datas = os.listdir('data')
    data_path = [s for s in datas if '.csv' in s]
    
    kind_path = [s for s in data_path if 'kind' in s][0]
    dart_path = [s for s in data_path if 'dart' in s][0]

    kind_path = os.path.join('data', kind_path)
    dart_path = os.path.join('data', dart_path)

    kind_df = pd.read_csv(kind_path, names=["stock_code", "corp_name"], header=0, dtype=str)
    dart_df = pd.read_csv(dart_path)
    
    return kind_df, dart_df

def join_datas(kind_df, dart_df):
    joined_df = kind_df.merge(dart_df, on=['stock_code', 'corp_name'], how='inner')
    return joined_df

def df_to_csv(df):
    today = datetime.today().strftime("%Y-%m-%d")
    folder = 'data'
    file_name = 'company-'+today+'.csv'
    file_path = os.path.join(folder, file_name)

    df.to_csv(file_path, encoding='utf-8', index=False)

def main():
    kind_crawling()
    dart_crawling()
    kind_df, dart_df = load_datas()
    joined_df = join_datas(kind_df, dart_df)
    df_to_csv(joined_df)

if __name__ == "__main__":
    main()

