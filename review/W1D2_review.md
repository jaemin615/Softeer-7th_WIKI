## <회고>
- keep
	- 출근해 있는 시간 동안 딴생각 최소화하고 집중하기

- problem
	- sql 과제 하는 과정에서  실행할 예제 쿼리문 양이 많아 중반부 이후에는 example 실행할 때 사이트에 있는 쿼리문을 복붙해서 입력한 점이 문제 같다.

- try
	- 그룹 미션 답안 좀더 고민해보기

## 1. W1M2 - sql 학습

sqlite3 라이브러리로 sqlite db 활용
로컬에 db파일 생성 후 연결, cursor로 db 조작

https://github.com/uwla/sample_mysql_database
해당 레포에서 w3school sql example에 쓰이는 데이터를 csv파일로 다운받은 후
쿼리에 사용된 테이블을 생성

cursor.execute() -> sql 쿼리 실행
sqlite에는 datetime 타입이 없음 -> TEXT로 저장후 sqlite 내장함수로 계산

csv 파일 읽어서 테이블에 insert
Pragma table_info -> 테이블 스키마 정보 확인
cursor.executemany() -> 같은 스키마의 데이터들을 삽입할때 데이터를 execute보다 빠른속도로 처리
cursor.discription -> 각 필드 특징 알아보기

쿼리 결과 출력할때 표 형태로 출력해보기 위해 tabulate 라이브러리 사용

### 쿼리 실행 중 특이사항

drop table이나 전체 레코드 delete 와 같이 다음 쿼리에 영향을 주는 쿼리문은 실행하지 않음
wildcard 같은 경우 sqlite가 % 혹은 _ 밖에 지원하지 않아 나머지 와일드카드 쿼리문은 실행하지 않음
any 나 all 키워드도 sqlite에 구현되어 있지 않음 
select into 를 create table as select 로 대체
PROCEDURE 도 sqlite에는 없는 기능



## 2. W1M3

파이썬 request 모듈로  해당 위키백과 페이지에 GET 요청
-> 요청 헤더에 User-agent 설정 필요

응답 결과 의 body(html 코드)를  bs4로 파싱
해당 페이지에서 개발자 도구로 국가별 gdp 표 부분 태그 확인
테이블 태그에 클래스 검색으로 gdp표 부분 가져오기

gdp 표를 pandas로 데이터프레임으로 만들고 필요한 부분만 취합하고 문제 상황에 맞게 단위 변환





