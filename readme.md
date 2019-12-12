웹 프로젝트 안내문
=======


진행 현황
--------

#### 참고사항
* index
	* 첫화면
	* 로고 나올 때.. 애니메이션 효과넣음.. 걍 넣고 싶어서..
* login
	* 로그인페이지
	* 아이디/패스워드 제한인 20자 이상 못써넣게 해놓음
	* 로그인 세션 유지됨
		* 유지시간 1시간
		* 로그인 세션 유지되고 있으면 index 및 login은 처음에 건너뛰게 만듦
		* 로그인 되어있지 않으면 상품 페이지 등 못 보게 함(성균인의 플리마켓에 로그인 안된사람이 들어오면 쓰겠습니까??)
* register
	* 회원가입 페이지
	* 서버단에서 validation함
		* 아디, 비번, 이름, 전화번호 글자수
		* 아디, 비번, 이름 : 숫자와 영어만 사용, 전화번호 : 숫자만 사용
		* 아이디 데베와 연동해서 중복체크
		* 비번에 숫자랑 영문 반드시 하나 이상 들어가야함
		* valid하지 않으면 문구가 화면에 표시됨
* welcome
	* 회원가입 성공 후 나오는 페이지
* market
	* 중고장터 페이지, 로그인 후 메인페이지이기도 함
	* 옆에 navigation은 로그인 후 다른 페이지에서도 계속 공통적으로 보였으면 함
	* Sell - Wishlist - My Items / Flea Market - Auction / My account - Logout 색깔 각각 달랐으면 좋겠음 -> 색깔 변경 완료
	* 상단 카테고리 디자인
	* 사이드 navigation 스크롤해도 고정되게 함
	* table 크기 및 정렬
	* 반응형페이지로 화면이 가로로 좁아지면 이미지만 보이게 설정, 각 요소들 겹치지 않게 조정
	
* sell
	* 사진 대체 어케 올림???? 돌겠노ㅁㄴㅇㄹ
	* 사이드 navigation 추가함
	* form css 작성 -> 카테고리 형식으로 입력받는 애들이 적용이안된당ㅠㅠ
	* 반응형페이지로 만듦
* auction
	* 경매 페이지
* detail
	* 상품 상세 페이지
	* 걍 옥션이랑 마켓이랑 html 같이 쓰고 상세페이지에서 무조건 bid하게 하기 (설명을.. 읽어보고 사야지..~~)
* myitems
	* 내가 판매하는 물품 목록
* search
	* nav에서 바로 서치되게 하고 싶음 (auction이나 market 중에 골라서)
	* 드롭박스로 추가 완료
* 아 왤케할거많아 진짜 이런거 낸 조교=제정신X

추가하면 좋을 기능 정리
================
1. auction이더라도 바로 낙찰할 수 있는 가격 / highest 구매자가 너무 맘에 들어서 이 가격 써내면 바로 낙찰됨
	* 약간 까다로울듯
2. 최저가 설정도 하게 하기
	* 할만할듯
3. 언제까지 팔 건지 시간 선택 가능.
	* 할만할듯
4. 카테고리
	* 구현함
5. 다양한 정렬 기능 (방금 입찰된 것, 가장 많이 입찰된 것 등등)
	* 할만하지만 조금 귀찮음
6. 판매자 평가 기능(낙찰자만 가능)
	* 할거 많아짐
7. 입찰한 사람이 아무도 없을 경우에만 expire 늘릴 수 있음
	* 좀 많이 귀찮음
8. 낙찰 알림페이지
	* 있으면 좋겠지만..



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