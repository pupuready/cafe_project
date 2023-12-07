import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from pandas.tseries.offsets import DateOffset

#define_X 함수로 모델 학습에 사용할 독립변수 설정.
def define_X(day_option=False,region=False,month=False,season=False,kospi=False,kosdaq=False,college=False):
    merge = None

    if day_option:
        if day_option == 1:
            day_off = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/day_off1", index_col=0)
        elif day_option == 2:
            day_off = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/day_off2", index_col=0)
        elif day_option == 3:
            day_off = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/day_off3", index_col=0)
        else:
            print("The options are one of 1, 2, 3")
            return None
        merge = day_off if merge is None else pd.merge(merge, day_off, left_index=True, right_index=True, how='inner')

    if region!=False:
        if region=="서울":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Seoul_rain',index_col=0)
        elif region=="부산":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Busan_rain',index_col=0)
        elif region=="인천":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Incheon_rain',index_col=0)
        elif region=="울산":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Ulsan_rain',index_col=0)
        elif region=="대구":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Daegu_rain',index_col=0)
        elif region=="대전":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Daejeon_rain',index_col=0)
        elif region=="광주":
            rain_day=pd.read_csv('https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/Gwangju_rain',index_col=0)
        else:
            print("The options are one of 특별시, 광역시")
        merge = rain_day if merge is None else pd.merge(merge, rain_day, left_index=True, right_index=True, how='inner')
    
    if season!=False:
        season_data = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/season", index_col=0)
        merge = season_data if merge is None else pd.merge(merge, season_data, left_index=True, right_index=True, how='inner')
    if month!= False:
        month_data = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/month", index_col=0)
        merge = month_data if merge is None else pd.merge(merge, month_data, left_index=True, right_index=True, how='inner')
    if kospi!= False:
        kospi_data = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/kospi", index_col=0)
        merge = kospi_data if merge is None else pd.merge(merge, kospi_data, left_index=True, right_index=True, how='inner')
    if kosdaq!= False:
        kosdaq_data = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/kosdaq", index_col=0)
        merge = kosdaq_data if merge is None else pd.merge(merge, kosdaq_data, left_index=True, right_index=True, how='inner')
    if college!= False:
        college_data = pd.read_csv("https://raw.githubusercontent.com/pupuready/cafe_project/main/Data/college", index_col=0)
        merge = college_data if merge is None else pd.merge(merge, college_data, left_index=True, right_index=True, how='inner')
    
    return merge


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from pandas.tseries.offsets import DateOffset

def ModelTrainer(X, y):
    # models에 각 메뉴별 모델 저장
    models = {}
    # mape_scores에 각 메뉴별 모델의 정확도 저장
    mape_scores = {}
    # 다음 달 메뉴별 수요 예측값 저장
    next_month_predictions = {}

    # X와 y의 인덱스를 datetime 타입으로 변환
    X.index = pd.to_datetime(X.index)
    y.index = pd.to_datetime(y.index)

    # X와 y의 인덱스 교집합 계산
    common_indices = X.index.intersection(y.index)
    X_common = X.loc[common_indices]
    y_common = y.loc[common_indices]

    # 시계열 교차 검증을 위한 TimeSeriesSplit 객체 생성
    tscv = TimeSeriesSplit(n_splits=5)

    for menu_item in y_common.columns:
        mape_scores[menu_item] = []

        for train_index, test_index in tscv.split(X_common):
            X_train, X_test = X_common.iloc[train_index], X_common.iloc[test_index]
            y_train, y_test = y_common[menu_item].iloc[train_index], y_common[menu_item].iloc[test_index]

            model = LinearRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            mape_score = mean_absolute_percentage_error(y_test, y_pred) * 100
            mape_scores[menu_item].append(mape_score)

        models[menu_item] = model
        mape_scores[menu_item] = 100 - round(sum(mape_scores[menu_item]) / len(mape_scores[menu_item]), 1)

    # 다음 달을 위한 예측 수행
    last_date = pd.to_datetime(y_common.index[-1])
    next_month = (last_date + DateOffset(months=1)).strftime('%Y-%m')
    if next_month in X.index:
        X_next_month = X.loc[[next_month]]

        for menu_item in models:
            next_month_pred = models[menu_item].predict(X_next_month)[0]
            next_month_predictions[menu_item] = int(next_month_pred)

    # 결과 데이터프레임 생성
    results_df = pd.DataFrame({
        'Predictions': next_month_predictions,
        'Accuracy': mape_scores
    })

    return results_df

