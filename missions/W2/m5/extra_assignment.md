### Word Cloud 작동 방법

[WordCloud Repo](https://github.com/amueller/word_cloud)
해당 레포의 word_cloud/wordcloud/wordcloud.py  내용을 참고함

- 텍스트 전처리 및 빈도수 계산 (`process_text`) 
	- input: text: str / output: words: dict
	- 긴 텍스트로부터 단어 분리, 전처리를 통한 정규화
	- 각 단어 개수 카운트
	- 단어의 빈도 수를 0~1사이의 값으로 정규화하여  {word: frequency} 형식으로 반환 
	
- 공간 점유 관리 (`IntegralOccupancyMap`)
	-  적분 이미지를 활용하여 텍스트 배치가 확정될때 마다 캔버스의 점유 상태 업데이트, 수학적인 누적합을 이용하여 단어가 들어갈 공간이 비어있는지를 체크
    
- 단어 배치 전략 짜기 (`generate_from_frequencies`)
	- input: frequencies: dict {word: frequency}
	- 입력받은 단어들을 빈도 수 순으로 내림차순 정렬 (가장 빈도수 높은 단어 부터 배치)
	- 가장 빈도가 높은 단어 크기를 정하고 나머지 단어들도 `relative_scaling` 설정에 따라 크기 설정
	-  각 단어 배치
		-  위치 선정 후 다른 단어와 겹치는지 위의 `IntegralOccupancyMap` 함수 사용하여 확인
		-  자리가 없는 경우 단어를 90도 회전시키거나 폰트 크기 1단계 줄이기
		-  단어 배치 확정 후 적분 이미지 데이터 갱신하여 해당 영역이 사용 중임을 표시

- 최종 렌더링 (`to_image`)
	- 배치가 완료된 단어들의 정보(텍스트, 좌표, 크기, 방향, 색상)는 
	 `self.layout_` 속성에 저장되어 있음
	- 해당 속성 바탕으로 Pillow 라이브러리의 실제 이미지 표시

### 추가 학습거리

[Predicting Election Results from Twitter Using Machine Learning Algorithms](https://www.researchgate.net/publication/343310126_Predicting_Election_Results_from_Twitter_Using_Machine_Learning_Algorithms) 
해당 글의 요약본에 대한 소감

SNS와 같은 디지털에 남겨진 흔적들이 여론을 나름대로 정확하게 반영할 수도 있다는 것이 인상 깊었다.

전화와 같은 기존 여론 조사 방식이 과연 효율적일까라는 생각을 평소에 가지고 있었고, SNS를 활용할 수 있겠다는 막연한 생각은 했었지만 구체적인 방법에 대해서는 깊이 생각해 본 적이 없었다. 그런 면에서 우선 트위터의 포스트를 수집해 감성 분석(Sentiment Analysis)을 도입하고, 이를 통해 후보자에 대한 대중의 호감도를 수치화한 것이 구체적이고 괜찮은 시도였다고 느꼈다.

결론 단에서 제안된 모델이 2019년에 시행된 선거 결과를 기존 기준선 대비 94.2%의 정확도로 예측하여 실제 선거 결과와 매우 근접하였다는 점을 보고, 이러한 기법을 기존 여론조사와 융합하여 보완한다면 응답률 저하나 표본의 편향성 문제를 해결할 수 있는 대안 중 하나가 될 것이라는 생각이 들었다.

또한 데이터 분석이 단순히 과거를 기록하는 것을 넘어, 실시간으로 추가되는 데이터를 통해 미래를 예측하는 도구로도 쓰일 수 있음을 실감했다. 이러한 데이터 분석이 여러 상황에 확장되어 쓰일 수 있다는 점을 고려할 때, 본문에 나온대로 앞으로 데이터가 사회의 여러 문제르 해결하는데 핵심적인 역할을 할 것 같다.
