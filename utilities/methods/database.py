from rest_framework.authtoken.models import Token
from membership.models import Customer, User


def get_customer_from_user_id(uid):
    return Customer.objects.get(user_id=uid)


def get_user_id_by_token(token):
    return Token.objects.get(key=token).user_id


def get_user_by_token(token):
    return get_user_by_id(get_user_id_by_token(token))


def get_user_by_id(userid):
    return User.objects.get(id=userid)


def get_user_by_username(username):
    return User.objects.get(username=username)


def get_customer_by_token(token):
    return Customer.objects.get(user=get_user_by_token(token))


def get_customer_by_uid(userid):
    return Customer.objects.get(user_id=userid)


def get_customer_by_cid(customerid):
    return Customer.objects.get(id=customerid)


def get_customer_by_username(username):
    return Customer.objects.get(user=get_user_by_username(username))


def get_token_by_user_id(userid):
    return Token.objects.get(user_id=userid)


def get_token_by_user(user):
    return Token.objects.get(user=user)


def get_token_by_customer_id(customerid):
    return get_token_by_customer(get_customer_by_cid(customerid))


def get_token_by_customer(customer):
    return Token.objects.get(user=customer.user)


def update_all_status_promotions(list_of_promotion):
    from django.utils.timezone import now

    sets = list_of_promotion.filter(start_date__lt=now(), end_date__gt=now())
    for q in sets:
        q.change_status(True)
    return sets.filter(status=True)


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    from django.shortcuts import get_object_or_404 as _get_object_or_404
    from django.core.exceptions import ValidationError
    from django.http import Http404

    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404
