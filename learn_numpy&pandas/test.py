import pandas as pd
from string import ascii_uppercase

def get_tidy_data(path:str)->pd.DataFrame:
    #  讀入試算表為資料框
    df = pd.read_excel(path,skiprows=[0, 1, 3, 4])
    # 获得候選人
    column_nams = list(df.columns)
    candidate_numbers_names = column_nams[3:6]
    # 給定欄位名
    column_nams = ['district', 'village','office'] + candidate_numbers_names + list(ascii_uppercase[:8])
    df.columns = column_nams
    # 填補行政區缺失
    df['district'] = df['district'].fillna(method='ffill')
    # 清理行政區的空字串
    df['district'].str.replace('\u3000','').str.strip()
    # 刪除得票數小計、總計列
    tidy_df = df.dropna().reset_index(drop= True)

    return tidy_df

def main():
    path = f'./總統-各投票所得票明細及概況(Excel檔)/總統-A05-4-候選人得票數一覽表-各投開票所(臺北市).xls'
    df = get_tidy_data(path)
    print(df)
    print(type(df))

main()