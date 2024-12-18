from bs4 import BeautifulSoup  # BeautifulSoup 라이브러리 임포트
import requests  # HTTP 요청을 위한 requests 라이브러리 임포트
import re  # 정규 표현식을 위한 re 라이브러리 임포트
import pandas as pd  # 데이터프레임 처리를 위한 pandas 라이브러리 임포트
import datetime  # 날짜 및 시간 처리를 위한 datetime 라이브러리 임포트

# 뉴스 카테고리 리스트
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# 빈 데이터프레임 생성
df_titles = pd.DataFrame()

# 각 카테고리에 대해 뉴스 제목을 크롤링
for i in range(6):
    # 각 카테고리의 URL 생성
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)  # URL에 GET 요청
    soup = BeautifulSoup(resp.text, 'html.parser')  # 응답 텍스트를 BeautifulSoup 객체로 변환
    title_tags = soup.select('.sa_text_strong')  # 제목 태그 선택
    titles = []  # 제목을 저장할 리스트 초기화

    # 선택한 제목 태그에서 텍스트 추출
    for title_tag in title_tags:
        title = title_tag.text  # 제목 텍스트 추출
        title = re.compile('[^가-힣 ]').sub(' ', title)  # 한글과 공백을 제외한 문자 제거
        titles.append(title)  # 정제된 제목을 리스트에 추가

    # 제목 리스트를 데이터프레임으로 변환
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]  # 카테고리 추가
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)  # 데이터프레임 합치기

# 크롤링한 데이터의 상위 5개 출력
print(df_titles.head())
df_titles.info()  # 데이터프레임 정보 출력
print(df_titles['category'].value_counts())  # 각 카테고리의 제목 수 출력

# 데이터프레임을 CSV 파일로 저장
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)  # 현재 날짜를 파일 이름에 포함