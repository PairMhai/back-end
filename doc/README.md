# Index of document
This API using [REST architectural style](REST-description.md) and API framework, I choose [Django REST framework](http://www.django-rest-framework.org).

# Testing guideline
[guide](TEST_GUIDE.md)

# Membership
WIP

# Alert Error
1. I didn't implement account and admin user so `api-auth/` will not found before login.
2. I not sure that I upload the database with superuser or not
  - if yes:
    - username will be `admin` and password is `password123`
  - if no:
    - run `python|python3 manage.py createsuperuser`
