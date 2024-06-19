from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

import time
import os
import math

# 잡코리아 자동팝업 닫기 사용자정의 함수
def popup_close():
    driver.find_element_by_xpath('/html/body/div[7]/div/button').click()
    time.sleep(2)
    return

# 기본 변수 선언
query_no = int(input('''
1. 경영사무      2. 마케팅/광고홍보     3. 무역유통          4. 영업/고객상담
5. IT인터넷      6. 생산제조            7. 연구개발/설계     8. 디자인
9. 미디어       10. 건설               11. 서비스           12. 교육 
13. 의료        14. 전문/특수직

직무를 선택하세요: '''))

query_arry = ['0', '10012','10013','10014','10015', '10016','10017','10018','10019',
              '10020','10021','10022','10023', '10024','10025']
query_arry = [int(i) for i in query_arry]

query_txt_list = ['0', '경영사무', '마케팅홍보', '무역유통', '영업고객상담',
                  'IT인터넷', '생산제조', '연구개발_설계', '디자인',
                  '미디어', '건설', '서비스', '교육', '의료', '전문특수직']
query_txt_list = [str(i) for i in query_txt_list]

query_no2 = query_arry[query_no]      # 사용자 입력값과 직무코드 연결
query_txt = query_txt_list[query_no]  # 사용자 입력값과 직무명 연결

# 엘리먼트 클릭 불가, 사용자입력값과 링크 xpath 값 매칭을 위한 배열 선언
xpath1_arry = ['0','1','1','1','2','1','2','2','1','3','3','2','2','3','3']
xpath1_arry = [int(i) for i in xpath1_arry]

xpath2_arry = ['0','1','2','5','1','3','4','3','4','3','1','2','5','2','4']
xpath2_arry = [int(i) for i in xpath2_arry]


f_dir = input('저장폴더(예시 c:\\temp\\) : ')
cnt = int(input('검색 건수를 입력하세요 : '))
id_txt = input('잡코리아 아이디를 입력하세요 : ')
pw_txt = input('잡코리아 패스워드를 입력하세요 : ')

# 저장될 파일 이름과 저장위치 지정
n = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)

os.makedirs(f_dir + s + '-' + query_txt)
os.chdir(f_dir + s + '-' + query_txt)

ff_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.txt'
fc_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.csv'
fx_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.xlsx'

# Step 1. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
path = "c:/py_temp/chromedriver.exe"

driver = webdriver.Chrome(path)

s_time = time.time()  # 크롤링 시작 시간을 위한 타임 스탬프를 찍습니다

driver.get("http://www.jobkorea.co.kr/starter/passassay")
time.sleep(3)
popup_close()  # 팝업창 닫기

# 로그인
driver.find_element_by_class_name('btnMyOpen').click()
element1 = driver.find_element_by_id("M_ID")
element1.send_keys(id_txt)

element2 = driver.find_element_by_id("M_PWD")
element2.send_keys(pw_txt)

driver.find_element_by_class_name('btLoin').click()
time.sleep(1)

driver.get("http://www.jobkorea.co.kr/starter/passassay")
time.sleep(2)
# popup_close() #팝업창 닫기 (팝업이 뜰 경우 활성화)

# 지원분야 선택

for i in range(1,16):
    if query_no == i:
        xpath1_arry_r = xpath1_arry[i]
        xpath2_arry_r = xpath2_arry[i]
        query_arry_r = query_arry[i]

        driver.find_element_by_xpath(
            '//*[@id="container"]/div[2]/div[2]/div/div[1]/div/dl[1]/dd[1]/div/div[1]/div/ul[%s]/li[%s]'
            %(xpath1_arry_r, xpath2_arry_r)).click()

        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="g_%s"]/ul[1]/li[1]/label' %query_arry_r).click() # 세부분야 전체 클릭

        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/div/div[1]/div/dl[2]/dd/div/div[1]/div/ul/li[1]/label').click() # 신입클릭

# 조건검색 버튼 클릭
driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/div/div[2]/button').click()
time.sleep(1)
# popup_close() #팝업창 닫기 (팝업이 뜰 경우 활성화)


# 검색건수 확인하기
html = driver.page_source
soup = bs(html, 'html.parser')

search_cnt_1 = soup.select('div > h4 > span')
search_cnt_2 = search_cnt_1[1].get_text().replace(",", "")
print('%s 검색어로 검색된 결과는 총 %s 건입니다' %(query_txt, search_cnt_2))

page_cnt = math.ceil(cnt / 20)  # 크롤링 할 페이지 수
print("=" * 120)
print('%s 키워드로 전체 검색 결과 %s 건 중에서 %s건의 정보 수집을 시작합니다.' %(query_txt, search_cnt_2, cnt))
print("=" * 120)

# 저장리스트 선언
no2 = []  # 게시글 번호 컬럼
cont_cpny = []  # 기업명
cont_subject = []  # 제목
cont_pass = []  # 합격자정보 컬럼
cont_answer = []  # 답변컬럼

no = 1  # 번호 초기화

for x in range(1, page_cnt + 1):
    print("%s 페이지 내용 수집 시작합니다. =====" % x)

    for y in range(1, 21):
        f = open(ff_name, 'a', encoding='UTF-8')

        # 각 게시글 제목 클릭
        driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[5]/ul/li[%s]/div[1]/p/a' % y).click()
        time.sleep(2)

        html = driver.page_source
        soup = bs(html, 'html.parser')

        # 각 게시글의 제목 추출
        title1 = soup.find('div', 'viewTitWrap')
        title2 = title1.find('a').get_text()
        title3 = title1.find('em').get_text()
        print('\n')
        print("번호: %s - %s - %s" % (no, title2, title3))

        no2.append(no)
        cont_cpny.append(title2)
        cont_subject.append(title3)

        # 합격자 스펙 가져오기
        p_info1 = soup.find('ul', class_='specLists').find_all('li')
        p_info2 = [t.text for t in p_info1]
        p_info2 = p_info2[:-1]  # 가져온 값의 마지막 정보인 '조회수'는 제거
        p_info3 = ', '.join(p_info2)
        cont_pass.append(p_info3)
        print(p_info3)

        # 합격 자소서 가져오기
        a_info = soup.select('div.tx > b')
        for z in a_info:
            a_txt = z.get_text().replace("\n", "")
            cont_answer.append(a_txt)
            f.write(str(a_txt) + "\n")
            print(a_txt)
        print('\n')

        driver.back()
        time.sleep(2)
        f.close()
        # popup_close()   #팝업창 닫기 (팝업이 뜰 경우 활성화)

        no += 1

        if no > cnt:
            break

    x += 1

    if x > page_cnt:
        break

    try :
        driver.find_element_by_link_text("""%s""" %x).click() # 다음 페이지번호 클릭
    except :
        continue

# 출력 결과를 다양한 형식으로 저장하기
df = pd.DataFrame()

df['번호'] = no2
df['회사명'] = cont_cpny
df['제목'] = cont_subject
df['합격자정보'] = cont_pass
# df['자소서'] = cont_answer

# csv 및 엑셀 형태로 저장하기
df.to_csv(fc_name, encoding="utf-8-sig", index=False)
df.to_excel(fx_name,index=False,engine='xlsxwriter')

e_time = time.time()
t_time = e_time - s_time

print("\n")
print("=" * 80)
print("크롤링을 요청한 총 %s 건 중에서 %s 건의 데이터를 수집 완료 했습니다" % (cnt, no - 1))
print("총 소요시간은 %s 초 입니다 " % round(t_time, 1))
print("파일 저장 완료: txt 파일명 : %s " % ff_name)
print("파일 저장 완료: csv 파일명 : %s " % fc_name)
print("파일 저장 완료: xlsx 파일명 : %s " % fx_name)
print("=" * 80)

driver.close()

