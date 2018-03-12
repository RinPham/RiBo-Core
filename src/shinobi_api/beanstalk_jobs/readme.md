**Add new worker**

```
1. Create new worker same as email.py
2. Register in the __init__.py
```

** Start queue **

```
python manage.py beanstalk_worker -w 5
```