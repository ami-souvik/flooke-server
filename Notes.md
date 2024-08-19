NOTE:
1. Since we are using custom user model we needed to do [these changes](https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory)

2. In order to rollback all the migrations run the following script
```
python manage.py migrate --fake myappname zero
```
Also, In order to rollback to a specific point run the following script
```
python manage.py migrate --fake myappname 0005
```