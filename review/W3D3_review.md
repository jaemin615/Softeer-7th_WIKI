## W3M2

미션 b 수행과정에서 설정을 변경하고 하둡을 재시동하기 전에, 

변경한 xml 파일들의 내용이 master 노드 뿐만 아니라 worker 노드에 반영이 되지 않고 있다는 것을 파악했다.

그래서 scp로 변경 내용을 각 워커 노드들에게 전송해 주도록 코드를 추가로 작성했다.
## W3M3

M2에서 구성해놓은 하둡 클러스터 사용

> [!note]
> **Hadoop Streaming**
> 
> Hadoop MapReduce에서 Java가 아닌 다른 언어의 스크립트를 매퍼와 리듀서로 사용할 수 있게 해주는 기능,
> stdin/stdout만으로 데이터를 교환하는 범용 인터페이스를 제공한다



https://www.gutenberg.org/ 에서 ebook 다운로드

파이썬으로 mapper.py reducer.py 작성

stdin 으로 읽어보고 stdout으로 결과를 내보내도록(print 하도록)
코드 작성)

### W3M4

긍정/부정 키워드 구축

https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
해당 사이트의 Opinion Lexicon (or Sentiment Lexicon) 
[A list of English positive and negative opinion words or sentiment words](http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar) (around 6800 words)

트윗 내용에 포함된 negatvie_word와 positive word의 개수를 비교하여 더 많은쪽으로 라벨링, 개수가 동일하면 neutral로 라벨링

### 아이디어

생각한 아이디어를 팀 노션에 쓰는 중인데 팀원들이랑 이야기 해보니까 각 아이디어를 구현한 서비스가 1개이상은 존재하는 것 같아서 고민이 된다.

제출한 아이디어 중 하나가 팀원들과의 논의 끝에 Top2로 되긴 했는데 솔직히 그 아이디어가 좋다고 생각하진 않아서 팀원의 아이디어로 가거나 다른 아이디어를 더 생각해봐야 될 거 같다.


