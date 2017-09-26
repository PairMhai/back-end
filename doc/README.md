# Index of document
This API using [REST architectural style](REST-description.md) and API framework, I choose [Django REST framework](http://www.django-rest-framework.org).

# Testing guideline
[guide](TEST_GUIDE.md)

# Membership (WIP)
1. ^membership/password/reset/$ [name='rest_password_reset']
2. ^membership/password/reset/confirm/$ [name='rest_password_reset_confirm']
3. ^membership/login/$ [name='rest_login']
4. ^membership/logout/$ [name='rest_logout']
5. ^membership/user/$ [name='rest_user_details']
6. ^membership/password/change/$ [name='rest_password_change']
7. ^membership/register/

# Alert Error
1. I didn't implement account and admin user so `api-auth/` will not found before login.
2. I not sure that I upload the database with superuser or not
  - if yes:
    - username will be `admin` and password is `password123`
  - if no:
    - run `python|python3 manage.py createsuperuser`
