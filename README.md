A [website](https://adenchen27.pythonanywhere.com/index/) for practicing English reading ability

Backend: Python + Django
Frontend: Html(bootstrap5) + css + JS
Hosted on [pythonanywhere](https://www.pythonanywhere.com/)

[Definitions](https://github.com/skywind3000/ECDICT) and [word to lemma mapping](https://github.com/skywind3000/lemma.en) from [Linwei](https://github.com/skywind3000)



TODO:
- [ ] users
    - [ ] user info page
    - [ ] upload passage page
    - [ ] edit page
    - [ ] error report page
- [ ] author page
    - [ ] js func plot proj
    - [ ] imgs
    - [ ] translations

quiz page
- [ ] act style
- [ ] show answer
- [ ] passage info

style
- [ ] bootstrap sass
- [ ] main.css structure

performance
- [ ] dynamic word freq
- [ ] cProfile
- [ ] edict data

quick actions
```
./manage.py collectstatic

./manage.py makemigrations;./manage.py migrate

./manage.py makemessages -l zh_hans
./manage.py makemessages -d djangojs -l zh_Hans
./manage.py compilemessages; ./manage.py runserver 127.0.0.1:7227

./manage.py runserver 127.0.0.1:7227

```

deploy
```
./manage.py dumpdata test > db.json
python3 manage.py loaddata db.json

cd Project_0
git clean -d -f
git reset --hard
git pull
python3 manage.py collectstatic

pip install -r requirements.txt
```



