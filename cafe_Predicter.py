import pandas as pd
import numpy as np

# 다음달 재고수요를 예측하는 함수
def predicter(prediction_df, recipe_df):

    # 레시피 데이터를 재료와 양을 기준으로 구분한다.
    recipe_df=pd.read_excel(recipe_df)
    recipe_df['레시피'] = recipe_df['레시피'].apply(lambda x: [i.split('.') for i in x.split(',')])

    #총 재고수요를 저장할 딕셔너리 선언
    total_requirements = {}

    #prediction에 iterrows 메서드를 수행
    for index, row in prediction_df.iterrows():
        menu_name = index
        predicted_demand = row['Predictions']

        # prediction_df의 메뉴명과 recipe_df의 메뉴명의 교집합
        recipe = recipe_df[recipe_df['메뉴명'] == menu_name]['레시피'].values
        if len(recipe) > 0:
            recipe = recipe[0]

            # 다음달 판매량에서 다음달 재고수요로 변환
            for ingredient, quantity in recipe:
                if ingredient not in total_requirements:
                    total_requirements[ingredient] = 0
                total_requirements[ingredient] += int(quantity) * predicted_demand

        #데이터프레임으로 변환
        df = pd.DataFrame(list(total_requirements.items()), columns=['메뉴명', '예측한 수요'])
        df.index=df['메뉴명']
        df=df.drop("메뉴명",axis=1)
    return df