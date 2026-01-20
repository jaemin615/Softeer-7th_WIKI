## W4M1
공식문서 내용을 참조함

https://spark.apache.org/docs/latest/configuration.html
https://spark.apache.org/docs/latest/spark-standalone.html
https://spark.apache.org/docs/latest/monitoring.html

### Dockerfile
- stable releases 중 가장 최신 버전인 Spark 4.1.1 버전 사용
- python library: pyspark, pandas, pyarrow 설치
- 루트가 아닌 유저 생성
-  ENTRYPOINT로 entry.sh 실행

### docker-compose.yml
- spark-master 컨테이너 1개 , spark-worker 컨테이너 2개, spark-history 컨테이너 1개 설정
#### environment
- entry.sh에서 마스터노드, 워커 노드 구분을 위해 각각 SPARK_MODE=master, SPARK_MODE=worker 설정
#### volume
- ./jobs:/opt/spark/jobs  
- ./data:/opt/spark/data
- ./logs:/opt/spark/logs
- ./spark-events:/opt/spark/spark-events
### conf
- 필요한 설정들 명시
### entry.sh

- 마스터 노드:  $SPARK_HOME/sbin/start-master.sh  실행
- 워커 노드:  $SPARK_HOME/sbin/start-worker.sh $MASTER-SPARK-URL 실행
- 히스토리 노드: SPARK_HOME/sbin/start-history-server.sh 실행
## W4M2

W4M1의 파일 재활용

### Dockerfile 
-  주피터 랩 관련 라이브러리 추가 설치
### docker-compose.yml
- 주피터랩 실행 컨테이너 추가
### entry.sh
- 주피터랩 실행 명령 추가

###  NYC 택시 데이터 스키마

#### 1. 시간 및 거리 (Time & Distance)
- **`tpep_pickup_datetime`**: 승객이 택시에 탄(승차) 날짜와 시간
-  **`tpep_dropoff_datetime`**: 승객이 목적지에 도착한(하차) 날짜와 시간
- **`trip_distance`**: 택시 미터기에 기록된 총 주행 거리
####  2. 위치 및 인원 (Location & Passengers)
- **`PULocationID` (Pick-Up)**: 승차한 지역의 택시 존(Zone) ID
- **`DOLocationID` (Drop-Off)**: 하차한 지역의 택시 존 ID
- **`passenger_count`**: 차량에 탑승했던 승객 수
#### 3. 요금 상세 (Fares & Fees)
- **`fare_amount`**: 미터기에 기록된 기본 요금(시간/거리 기반)
- **`extra`**: 피크 시간대(러시아워)나 야간 추가 요금
- **`mta_tax`**: MTA(뉴욕 교통 공사) 세금
- **`tip_amount`**: 신용카드로 결제된 팁 금액
- **`tolls_amount`**: 통행료 합계
- **`improvement_surcharge`**: 인프라 개선을 위해 부과되는 추가금
- **`congestion_surcharge`**: 맨해튼 혼잡 구역 통과 시 부과되는 혼잡 통행료
- **`airport_fee`**: 공항 이용 시 발생하는 추가 비용
- **`total_amount`**: 승객이 지불한 최종 합계 금액
#### 4. 기타 식별자 (Metadata)
- **`VendorID`**: 데이터를 제공한 업체 코드 (1: Creative Mobile Technologies, 2: VeriFone Inc).
- **`RatecodeID`**: 적용된 요금제 코드입니다. (1: 표준, 2: JFK 공항, 3: Newark, 4: Nassau/Westchester 등)
- **`store_and_fwd_flag`**: 차량 서버에 연결되지 않았을 때 데이터를 메모리에 저장했다가 나중에 전송했는지 여부 (Y: 저장 후 전송, N: 즉시 전송).
- **`payment_type`**: 결제 방식 코드 (1: 신용카드, 2: 현금, 3: 무상, 4: 분쟁 중 등)

### 날씨 데이터 스키마

- meteostat 라이브러리 사용
#### 1. 시간 및 기온 (Time & Temperature)
- **`time`**: 기상 관측이 이루어진 날짜와 시간
- **`temp` (Temperature)**: 기온(°C).
- **`dwpt` (Dew Point)**: 이슬점 온도(°C)
- **`rhum` (Relative Humidity)**: 상대 습도(%)
#### 2. 강수 및 적설 (Precipitation & Snow)
- **`prcp` (Precipitation)**: 강수량(mm)
- **`snow` (Snow Depth)**: 적설량(mm)
####  3. 바람 (Wind)
- **`wdir` (Wind Direction)**: 풍향 (0°: 북풍, 90°: 동풍, 180°: 남풍, 270°: 서풍)
- **`wspd` (Wind Speed)**: 평균 풍속(km/h)
- **`wpgt` (Wind Peak Gust)**: 최대 순간 풍속(km/h)
#### 4. 기압 및 기타 (Pressure & Others)
- **`pres` (Pressure)**: 해면 기압(hPa)
- **`tsun` (Total Sunshine)**: 일조 시간(min)
- **`coco` (Condition Code)**: 기상 상태 코드, 날씨의 상태(맑음, 흐림, 비 등)를 숫자로 분류한 값(예: 1: 맑음, 3: 구름 조금, 5: 안개 등)

해당 데이터들을 pyspark로 분석

https://spark.apache.org/docs/latest/api/python/user_guide/index.html

Pyspark userguide 참조하며 진행

분석 과정에서 sql 관련 작업을 할때 pyspark.sql.functions 라이브러리를 활용할 수도 있고 
spark.sql로 직접 쿼리를 날릴 수도 있다는 것을 알았음
