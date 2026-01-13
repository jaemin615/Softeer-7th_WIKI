### W3M2a

https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html

공식 문서 내용 우선 읽고 시작

문서 내용 확인하여 하둡 config 파일들 작성

m1의 도커파일 활용하여 MasterNode(NameNode)와 WorkerNode(DataNode) 2개 생성하는 도커 컴포즈 파일 작성

도커 컴포즈에서 네트워크 설정

컨테이너 실행 후 작동 테스트
localhost:9870 , localhost:8088에 접속 확인

모든 노드가 Master에서 돌아가고 있어 해결 방법 검색 중
설정 파일 중 workers에 localhost 값만 있어서 그렇다는 문제 확인 

로컬의 config 폴더에 worker 노드의 이름을 작성한 해당 파일 추가 후 도커 빌드 과정에서 복사되도록 함, 해당 과정에서 JAVA_HOME 환경 변수가 포함된 hadoop-env.sh 파일도 도커파일에서 echo로 값을 추가하는 방식에서 config 폴더 밑에 관리하는 방식으로 변경

맵 리듀스 작업 실행을 위해 하둡 맵리듀스 예제 파일을 탐색
find / -name "hadoop-mapreduce-examples-\*.jar"

etc 폴더 밑 모든 xml 파일을 hdfs에 올리고 
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.2.jar grep input output 'dfs[a-z.]+' 해당 명령어를 통해 Grep 명령어로 'dfs'로 시작하는 특정 단어를 찾는 작업 실행

결과
1       dfsadmin
1       dfs.replication
1       dfs.namenode.name.dir
1       dfs.datanode.data.dir

### W3M2b

컨테이너 내부에서 파이썬 스크립트 실행을 위해
도커 파일에 파이썬 설치 명령 추가

 Change fs.defaultFS to hdfs://namenode:9000 과 같은 설정 파일의 변경에 맞추어 도커 컴포즈 파일에서 마스터 노드 hostname 변경

 - 설정 변경 스크립트
	 - xml 조작에 xml.etree.ElementTree 모듈 사용
	 - 파일 조작에 shutil 모듈 사용
	 - subprocess 모듈로 하둡 명령어 실행

yarn-site.xml에서의 yarn.resourcemanager.hostname도 기존 이름에서 namenode로 변경이 필요했는데 변경을 안하고 실행해서 설정 변경 스크립트의 하둡 재시동 과정에서 에러가 발생했었다. 

- 설정 검증 스크립트
	- subprocess 모듈로 하둡 명령어 실행


설정 파일에서 namenode로 값을 모두 바꾼후 설정이 꼬였는지 자꾸 에러가 나서 설정 변경 스크립트를 실행하기 전에 namenode로 hostname를 설정하고 두 가지 스크립트를 실행하니 실행이 되었다.

### idea

생각나는 아이디어를  우선 해결책은 생각하지 않고
누구의, 문제 정의 부분만 팀페이지에 적는 중

