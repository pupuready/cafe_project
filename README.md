# Cafe Demand Forecast
![image](https://github.com/pupuready/cafe_project/assets/130034324/4dcaadc1-3ec5-4111-9030-6713a710299f)

## Topic 
카페 재고 수요 예측하기

## Motivation
카페에서 매니저로 일할 때 재고가 부족하여 팔지 못했던 메뉴가 많았다.
  
이것은 매출이 줄어드는 데 기여했고, 재고 소진을 예측할 수 있는 프로그램을 개발하게된 동기가 되었다.

## Library
<img src="https://img.shields.io/badge/python-3.11.1-3776AB"/> <img src="https://img.shields.io/badge/numpy-1.26.0-EE4C2C"/> <img src="https://img.shields.io/badge/pandas-2.1.1-EE4C2C"/> <img src="https://img.shields.io/badge/scikitlearn-1.3.2-EE4C2C"/> <img src="https://img.shields.io/badge/openpyxl-3.1.2-EE4C2C"/> 
  
## System design
<img width="800" alt="image" src="https://github.com/pupuready/cafe_project/assets/130034324/b40feb71-6dc5-4b71-93f6-eb4f78510110">

## cafe Preprocessor
### 주요 함수

#### 1) MergeRaw(2021_Excel_data, 2022_Excel_data,…)
  
* 기능 : 입력 받은 raw 데이터(Excel)를 Cafe_Model(X,y)의 종속변수 y로 사용할 수 있도록 전처리함.​
  
  
Input : 카페의 월간 메뉴별 판매 데이터 (raw data, Excel)
  
Output : 카페의 월간 메뉴별 판매 데이터 (preprocessed data, DataFrame)

#### 2) Del_menu(DataFrame, Menu1, Menu2,…)
  
* 기능: 입력 받은 메뉴를 데이터 프레임에서 삭제
  
  
Input : MergeRaw()를 통해 생성된 DataFrame, 삭제하고자 하는 메뉴의 이름​ str
  
Output: 선택한 메뉴가 삭제된 DataFrame​
  

## cafe Model Trainer
### 주요 함수

#### 1) define_X(region="서울",  day_option=1, month=True, ...)
  
* 기능 : Cafe_Model(X,y)의 독립변수 X를 생성
  
  
Input : 원하는 독립변수 Argument 선택
  
Output : Cafe_Model(X,y)의 독립변수 X DataFrame

#### 활용할 수 있는 독립변수 
  
region : 지역별 강수량 (특별시, 광역시)
  
day_option : 월간 카페의 휴일 수 (1: 일요일 + 공휴일, 2: 공휴일, 3: 연중무휴)
  
그외 : month, season, kospi, kosdaq (True, False)
  

#### 2) Cafe_Model(X,y)
  
* 기능: 다음달 메뉴별 판매량 예측
  
  
Input : define_X로 생성한 독립변수 X, cafe Preprocessor로 생성한 종속변수 y
  
Output: Predictions(다음달 예측 판매량), Accuracies(정확도[100-MAPE])을 포함한 DataFrame
  
  
## cafe Predict
### 주요 함수
#### 1) pridicter(Prediction, Recipe data)
  
* 기능 : 메뉴별 판매량을 재고수요로 변환
  
  
recipe data(Excel)의 형식
<br>
<img width="278" alt="image" src="https://github.com/pupuready/cafe_project/assets/130034324/a2676aeb-4b9e-45c9-8009-e617df1ff56d">
<br>
<Br>
Input : Cafe_Model로 생성된 DataFrame, 메뉴별 recipe data
<br>
Output : 다음달 재고수요 DataFrame
