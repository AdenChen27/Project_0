A [website](https://adenchen27.pythonanywhere.com/index/) for practicing English reading ability

Backend: Python + Django
Frontend: Html(bootstrap5) + css + JS
Hosted on [pythonanywhere](https://www.pythonanywhere.com/)

[Definitions](https://github.com/skywind3000/ECDICT) and [word to lemma mapping](https://github.com/skywind3000/lemma.en) from [Linwei](https://github.com/skywind3000)



TODO:
- [ ] user points
    tests taken cnt
    words studied cnt

- [ ] users
    - [ ] user info page
    - [ ] upload passage page
    - [ ] edit page
    - [ ] error report page

- [ ] author page
    - [ ] js func plot proj
    - [ ] imgs
    - [ ] translations

dictionary
- [ ] edict data
- [ ] ajax

quiz page
- [ ] act style
- [ ] show answer
- [ ] passage info

style
- [ ] bootstrap sass
- [ ] main.css structure

performance/code style
- [ ] dynamic word freq
- [ ] cProfile
- [ ] jQuery
- [ ] local bootstrap

quick actions
```
python3.10 ./manage.py collectstatic; python3.10 ./manage.py runserver 127.0.0.1:7227

python3.10 ./manage.py makemigrations; python3.10 ./manage.py migrate

python3.10 ./manage.py makemessages -l zh_hans
python3.10 ./manage.py makemessages -d djangojs -l zh_Hans
python3.10 ./manage.py compilemessages; ./manage.py runserver 127.0.0.1:7227

python3.10 ./manage.py runserver 127.0.0.1:7227

python3.10 ./manage.py runprofileserver --use-cprofile --prof-path=/tmp/my-profile-data 127.0.0.1:7227

```

deploy
```
cd Project_0
git clean -d -f
git reset --hard
git pull
python3 manage.py collectstatic

pip install -r requirements.txt



git clone 
cd Project_0 https://github.com/AdenChen27/Project_0
mkvirtualenv Project_0

pip install django
pip install django-bootstrap-v5
pip install django-mysql
pip install django-jsonfield
pip install nltk

python
improt nltk
nltk.download('stopwords')
nltk.download('punkt')
```



