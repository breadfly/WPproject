윈도우로 같은 과정을 수행하셔도 됩니다.

1. 파이썬3 설치 : sudo apt install python3
2. pip 설치 : sudo apt install python3-pip
3. django 설치 : pip3 install django
4. 해당 과제물을 다운 받은 후, mysite 폴더(해당 readme.txt가 존재하는 폴더)에서 python3 manage.py runserver 로 서버 실행
5. 웹브라우저로 localhost:8000 접속

Django 내부 DB를 사용하였기 때문에, 데이터베이스 데이터도 함께 들어있습니다.

localhost:8000/admin으로 들어가면 책 추가, 카테고리 추가, 회원 추가 등을 할 수 있습니다. 아이디와 비밀번호는 admin / admin입니다.
이는 django 기본 기능으로, 제가 구현한 것이 아니기 때문에 레포트에 추가하지는 않았습니다. 다만 테스트할 때 도움이 되기에 참고하시면 좋을 것 같습니다.