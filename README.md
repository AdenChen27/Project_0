A [website](https://adenchen27.pythonanywhere.com/index/) for practicing English reading ability

Backend: Python + Django
Frontend: Html(bootstrap5) + css + JS
Hosted on [pythonanywhere](https://www.pythonanywhere.com/)

[Definitions](https://github.com/skywind3000/ECDICT) and [word to lemma mapping](https://github.com/skywind3000/lemma.en) from [Linwei](https://github.com/skywind3000)



TODO:
- [ ] author page
    - [x] main
    - [ ] CTB proj
    - [ ] js func plot
    - [ ] link from index page
- [ ] users
    - [x] 3.27 user model
    - [ ] login page
    - [ ] register page
- [ ] test page show answer function

- [ ] bootstrap sass
- [ ] main.css structure
- [ ] info/help
- [ ] upload passage page
- [ ] edit page
- [ ] error report page
- [ ] cProfile

- [ ] dynamic word freq
- [ ] .gitignore for better performance on server

- [x] 3.26 multi-language support
- [x] 3.26 visit counter
- [x] 3.27 word select
- [x] 3.28 passage Flesch–Kincaid readability Level

quick actions
```
./manage.py makemigrations;./manage.py migrate

./manage.py makemessages -l zh_hans
./manage.py makemessages -d djangojs -l zh_Hans
./manage.py compilemessages; ./manage.py runserver 127.0.0.1:7227

./manage.py runserver 127.0.0.1:7227

```

deploy
```
./manage.py dumpdata test > db.json

cd Project_0
git clean -d -f
git pull
python3 manage.py loaddata db.json

pip install -r requirements.txt
```



