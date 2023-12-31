import pandas as pd
import numpy as np
import warnings
import re
# openpyxl의 기본 스타일 경고 메시지 끄기
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles")

def IceplusHot(idx):
    idx = idx.lower()
    # 특수 문자 제거
    idx = re.sub(r'[\[\]]', '', idx)
    # 공백 제거
    idx = idx.strip()
    if "ice" in idx:
        return idx.replace("ice","").strip()
    else:
        return idx.strip()
    
def MergeRaw(*Raws):
    import pandas as pd
        
    merged_df = None
    
    for file in Raws:
        df = pd.read_excel(file)
        df.index=df['상품명']
        
        #불필요한 칼럼 제거
        df = df.drop(['상품명','대분류', '중분류', '소분류', '바코드', '총수량', '총매출',
                      '순매출', 'NET매출', '부가세', '할인', '비율(%)'], axis=1)
        
        #불필요한 row 제거
        df = df.drop([df.index[0], df.index[-1]])
        
        #불필요한 칼럼 제거
        df = df.loc[:, ~df.columns.str.contains('Unnamed')]
        
        #ICE 문자열 제거
        df.index = df.index.map(IceplusHot)
        
        #같은 index명을 가진 row 통합
        df=df.groupby(df.index).sum()
        
        
        if merged_df is not None:
            merged_df = pd.merge(merged_df, df,on='상품명')

        else:
            merged_df = df
        
    return merged_df.T

def Del_menu(df,*menus):
    for menu in menus:
        df=df.drop(menu,axis=1)
    return df
