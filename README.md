English reading ability training [website](https://adenchen27.pythonanywhere.com/index/)

Backend: Python + Django
Frontend: Html(bootstrap5) + css + JS
Hosted on [pythonanywhere](https://www.pythonanywhere.com/)

[Definitions](https://github.com/skywind3000/ECDICT) and [word to lemma mapping](https://github.com/skywind3000/lemma.en) from [Linwei](https://github.com/skywind3000)



TODO:
- [ ] passage Flesch–Kincaid readability Level
- [ ] users
    - [ ] user model
    - [ ] login page
    - [ ] register page
- [ ] author page
- [ ] test page show answer function

- [ ] bootstrap sass
- [ ] main.css structure
- [ ] info/help
- [ ] upload passage page
- [ ] edit page
- [ ] error model
- [ ] error report page

- [ ] dynamic word freq

- [x] 3.26 multi-language support
- [x] 3.26 visit counter
- [x] 3.27 word select


quick actions
```
./manage.py makemigrations;./manage.py migrate

./manage.py makemessages -l zh_hans
./manage.py makemessages -d djangojs -l zh_Hans
./manage.py compilemessages; ./manage.py runserver 127.0.0.1:7227

./manage.py runserver 127.0.0.1:7227
```