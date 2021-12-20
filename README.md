# MovieAPI

## 소개

영화 정보 및 리뷰 API

YTS에서 제공하는 영화 정보를 기반으로 만들어진 영화 정보 및 리뷰 API

## 모델링

<img width="1054" alt="스크린샷 2021-12-21 오전 2 51 17" src="https://user-images.githubusercontent.com/5153352/146810713-0027575f-5c5e-4a04-8559-bb44bf02405e.png">
<br>
<br>
<br>

## API Document

[Postman Document](https://documenter.getpostman.com/view/13670333/UVRBkki7)
<br>
<br>
<br>

## 실행방법

```bash
$ git clone https://github.com/miranaky/Movie_Info_API.git && cd Movie_Info_API
$ pip install -r requirements.txt
# Django Secret Key 설정
$ export DJANGO_SECRET_KEY=9-uu5+qa*wgtlsj27jvmta04cqim7kd@1zuz4^+rd7j5@
# DB migrate
$ python manage.py migrate
# 서버 실행
$ python manage.py runserver 0.0.0.0:8800
# YTS 사이트에서 영화 정보 수집 및 저장
$ python manage.py get_movies
```

## 기능 구현 내용

### Movie(영화)

1. Movie(영화) 리스트 조회 API
   - pagination 기능
   - 검색 기능(year,genres,title)
   - 평점(rating) 별 오름차순,내림차순 정렬
2. Movie(영화) 디테일 조회 API
   - 영화 정보(id,title,year,rating,genres,summary,reviews(list)) 반환
3. Movie(영화) 생성 API
   - 영화 생성(title,year,genres,summary)

### Movie Review(영화리뷰)

4. Movie Review(영화리뷰) 디테일 조회 API
   - 영화리뷰 정보(id,text,rating,created_at,updated_at,vote)
5. Movie Review(영화리뷰) 생성 API
   - 영화리뷰 생성(text,rating,movie_id)
6. Movie Review(영화리뷰) 수정 API
   - 영화리뷰 수정(text,rating)
7. Movie Review(영화리뷰) 삭제 API
   - 영화리뷰 id로 삭제

### Movie Review Vote(영화리뷰추천)

8. Movie Review Vote(영화리뷰추천) 생성 API
   - 영화리뷰추천 생성(review_id)
9. Movie Review Vote(영화리뷰추천) 삭제 API

- 영화리뷰추천 id로 삭제

### 기타

10. Test Code
11. YTS 사이트에서 영화 정보 수집 및 저장

    ```bash
    #get_movies 사용법
    $ python manage.py get_movies --help
    usage: manage.py get_movies [-h] [--limit LIMIT] [--max_page MAX_PAGE]

    This command creates movies from yts.mx

    optional arguments:
    -h, --help            show this help message and exit
    --limit LIMIT         The limit of movie results per page that has been set
    --max_page MAX_PAGE   Page to explore as much as possible
    # 사용 예
    $ python manage.py get_movies --limit=30 --max_page=5
    ```
