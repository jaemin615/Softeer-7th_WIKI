## 강의

문제 해결에 있어서 엔지니어링 측면 만을 보기보다는 어떤 상황/누구의 문제를 해결하려는지에 대한 고민 필요
### spark
밑의 각 용어들에 대해서 구분할 수 있어야 된다.
#### deploy option
local / Standalone Cluster / Using a Cluster Manager
#### delpoy mode
local / Cluster / Client

## Team-mini-project

1. 희귀병 환자 임상시험 매칭 플랫폼
2. 실시간 서울 인구 혼잡도 및 주차공간 기반 장소 추천 서비스

팀원들끼리 논의 후 2번이 문제 정의, 왜 만드는 것인지 등이 불분명하나 개인 미션을 생각할 때 1번 구현이 목요일까지 안될 것 같다고 하여 일단 2번으로 시작해서 데이터를 가져오는 과정을 각자 진행해보기로 함

### 실시간 서울 인구 혼잡도 및 주차공간 기반 장소 추천 서비스
#### Pre-totype
수집한 데이터로 Streamlit 라이브러리를 활용하여 간단하게 대시보드를 구축해보았다.

<img width="820" height="833" alt="congestion_pre-totype" src="https://github.com/user-attachments/assets/3db3fb45-6efe-46cb-8470-aa937fefcef9" />

서울시에서 제공하는 공공데이터 중 실시간 인구 데이터 api를 활용하여 아래와 같이 pre-totype을 구현해봤는데 다노님이 말씀해주신 여러 질문에 대한 답을 내기는 어려울 것 같음. 

### 희귀병 환자 임상시험 매칭 플랫폼

다른 팀원들이 2번 구현해보는 동안 1번 희귀병 관련 주제도 조금 더 탐색해보고자 다노님 피드백대로 추가 조사를 해봄

#### 시나리오.  8살 소아 뇌종양 환아의 아빠 A씨

A씨의 딸 DIPG(뇌간에 발생하는 소아뇌종양의 일종) 환자 8살 딸 B양은  최근 국내에서 방사선 치료를 마쳤으나 더 이상 쓸 수 있는 약이 없다는 판정을 받았다. 해당 질환은 진단 이후 환자의 생존기간 중앙 값이 약 2년 정도이다.
#####  A씨가 취할 수 있는 액션
- 국내 단체 문의: 한국희귀·난치성질환연합회에 문의해 희귀질환 정보 공유. 한국백혈병소아암협회에서 소아암 치료비 지원과 전문 상담을 신청
- 커뮤니티 탐색: 네이버 카페 - 소아암 경험자들의 소아암 이야기
- 임상시험 정보 검색- ClinicalTrials.gov에서 참여 가능한 시험을 확인 
- 해외 치료 고려- 해외 병원 탐색
##### 해외 임상정보 검색 시 생길 수 있는 문제 시나리오

A씨는 검색을 통해 미국 다나파버 암연구소에서 특정 유전자 변이(H3K27M)를 타겟으로 한 신약 임상 1상이 진행 중이라는 소식을 들었다.
A씨는 영문 'Inclusion Criteria(참여 조건)' 과 'Exclusion Criteria(제외 조건)' 의 내용이 딸의 방사선 치료 결과/혈액 수치와 부합하는지 확신할 수 없다. 병원에 직접 메일을 보냈으나 서류를 모두 갖춰 정식 접수하라는 원론적인 답변만 받은 상태이다.

##### 매칭 플랫폼 활용 시나리오
1. B양의 질병/ 변이 명과 같은 질병 관련 기본 정보와 관련 서류(유전자 검사 결과지와 최근 진료 기록 등)를 플랫폼에 업로드
2. 플랫폼은 매칭되는 임상을 찾고, 해당 임상의 'Exclusion Criteria(제외 조건)'인 '스테로이드 투여 용량 제한'과 B양의 현재 투약 상태를 자동 비교 분석
3. 참여 가능성이 높다고 분석되면,  해당 연구팀에 B양의 데이터를 비식별화하여 전달, "현재 모집 인원이 남아 있으며, 서류 검토 가능함"이라는 예비 확답을 빠른 시간 내에 받기
##### pre-totype
LLM(v0)으로 프롬프팅을 통해 리액트 코드 생성한후 시나리오 설정 후 탐색 과정에서 본 내용으로 텍스트를 임의로 채워넣었다. 

<img width="1296" height="798" alt="trialmatch_pre-totype_dashboard" src="https://github.com/user-attachments/assets/655b022a-2617-4e06-b7e9-702cfb6f4706" />

<img width="875" height="794" alt="trialmatch_pre-totype_detail_page" src="https://github.com/user-attachments/assets/f74205b2-0f51-4f15-9dbc-70c7ba78c7ef" />

일단 개인 미션 수행하며 시간이 얼마나 걸릴지 파악해보기로 했다.
## W4M1

Dockerfile 작성
스파크를 standalone cluster로 구축할때는 하둡과 달리 ssh 설정이 필요없다.

스파크는 RPC(Remote Procedure Call) 통신 방식을 사용할 수 있다.
마스터가 특정 포트(기본 7077)를 열고 대기하면 
워커는 실행될 때 마스터의 주소를 전달받아 직접 마스터에게 등록(Registration)을 요청하는 방식

```yaml
spark-master:
	command: ./bin/spark-class org.apache.spark.deploy.master.Master
	
spark-worker-1:
	command: ./bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077	
```

