A [website](https://adenchen27.pythonanywhere.com/index/) for practicing English reading ability

Backend: Python + Django
Frontend: Html(bootstrap5) + css + JS
Hosted on [pythonanywhere](https://www.pythonanywhere.com/)

[Definitions](https://github.com/skywind3000/ECDICT) and [word to lemma mapping](https://github.com/skywind3000/lemma.en) from [Linwei](https://github.com/skywind3000)



TODO:
- [ ] users
    - [x] 3.27 user model
    - [x] 3.29 login/register page
    - [x] 3.29 login/register control
    - [x] 3.30 login control panel
    - [ ] user info page
    - [ ] upload passage page
    - [ ] edit page
    - [ ] error report page
- [ ] test page show answer function
- [ ] 3.29 titles
- [ ] author page
    - [x] 3.28 main
    - [x] 3.28 CTB proj
    - [ ] js func plot proj
    - [ ] imgs
    - [ ] translations

quiz page
- [ ] 2 col

style
- [ ] logo
- [ ] bootstrap sass
- [ ] main.css structure

performance
- [ ] dynamic word freq
- [ ] cProfile
- [ ] .gitignore


- [x] 3.26 multi-language support
- [x] 3.26 visit counter
- [x] 3.27 info/help
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



