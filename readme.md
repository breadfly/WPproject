웹 프로젝트 안내문
=======


진행 현황
--------
본인이 하고 있는 일, 타인이 참고했으면 하는 사항을 자유롭게 적어주세요.

#### 강보영
* 12/6~8 html 작성
* 12/10~13 css, jquery 완성
* 12/14~15 마무리, 발표준비, 가다듬기

#### 김지혜
* DB 들으면서 짰던 django 프로젝트 일단 올려놓음. 실행해보길 권장함.
* 수정사항이나 추가하고 싶은 거 있으면 플젝 contributor로 해놨으니 바로 push하면 됨 (방법은 해당 문서 참고)
* 12/6~8 DB 스키마 작성, form 작성
* 12/9 html template form 적용. 대략적인 완성
* 12/14~15 마무리, 발표준비, 가다듬기

#### 임세아
* 12/6~8 html 작성
* 12/10~13 css, jquery 완성
* 12/14~15 마무리, 발표준비, 가다듬기

실행 가이드라인
--------

백엔드 짜는 법은 몰라도 실행은 해봅시다

#### 설치

django는 톰캣이나 이클립스나 mysql 같이 무겁고 짜증나는 것들을 안 깔아도 된다는 엄청난 장점이 있답니다. 적당한 에디터랑 django만 깔면 만사 OK (물론 파이썬 정도는 깔아야 하지만)

해당 가이드라인은 Win10 64bit, visual studio code를 기반으로 작성되었습니다. 다른 운영체제나 에디터를 사용해도 무방합니다 (다만 방법은 알아서 찾으시길...) 설치한 게 오래 전이라 저도 잘 모릅니다.. 막히는 부분이 있으면 구글링.. 그리고 이미 본인한테 깔려 있다 싶은 건 알아서 스킵하세요 파이썬이나 git 같은거..



1. 파이썬3 설치(혹시나 모르니 파이썬 3.6 이상으로 설치)
	* 반드시 Add python to PATH 항목을 선택
	* https://tutorial.djangogirls.org/ko/python_installation/

2. visual studio code의 python 익스텐션 설치
	* 1 끝내고 나서 visual studio code 들어와서 왼쪽 탭 네모 여러개 있는 거 선택 (extension)
	* 거기서 Python 검색 후 install

3. pip 설치
	* 내가 pip 설치 어케 했는지 기억이 안나.. 걍 visual studio code가 알아서 깔아줬던 것 같은데 아닐수도
	* https://docs.djangoproject.com/en/3.0/topics/install/ 이거 참고해서 pip 설치
	* 아나콘다 같은 거 패키지 매니저 깔려있으면 걍 스킵해도 됨. 4번 conda install django 어쩌구 하면 될걸 (아마)

4. django 설치
	* pip install django
	* pip install pylint_django

5. git 설치
	* 참고 링크 https://promobile.tistory.com/352
	* git 설치 하고 git bash 틀어서(프로그램 검색해보면 나옴) 다음 명령어 입력
	* git config --global user.name 깃허브아이디
	* git config --global user.email 적당한이메일
	* visual studio code가 아마 이거 끝나면 알아서 git 익스텐션 깔라고 하거나 깔아줄것임.



#### 실행



1. visual studio code에서 github repository랑 연결하는 법
	* 위에 거 다 끝내고 vs code 켠다
	* 왼쪽 탭 젤 위에 거(explorer) 누름. open folder해서 작업할 빈 폴더 암거나 만들기
	* 왼쪽 탭에 트리?처럼 생긴 거 있음 (동그라미 세개 이어진거) 그거 클릭 (source control)
		* 없으면 extension 들어가서 git 검색 후 install
	* '+' 클릭해서 뭔가 창 같은 거 뜰 텐데 걍 엔터
	* ctrl+` 눌러서 터미널 연다
	* git remote add origin https://github.com/breadfly/WPproject.git 입력
	* ... 누르고 pull from 누르고 엔터

	* 수정하고는 commit(체크 버튼)누르고 ...에서 push to 찾아서 하면 업로드됨
	* 작업 시작하기 전에 pull from 부터 무조건 하기(다른 사람들 수정한 거 다운받는 것임)
	* conflict 발생하면 적당히 잘 고쳐서 merge하든가 rebase하든가 아님 아예 새로 짜든가 등등..

2. 서버 켜는 법
	* 해당 readme.md가 존재하는 폴더에서 터미널(ctrl+`)에 python manage.py runserver 입력. 그러면 서버 실행됨
	* 웹브라우저 주소창에 localhost:8000 넣으면 접속됨