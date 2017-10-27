from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save
from django.dispatch import receiver

from payment.models import CreditCard

# Interesting library
# https://docs.python.org/3/library/doctest.html

# custom user that extend from django auth user


class User(AbstractUser):
    """customer information v1"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    # email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, default="0XXXXXXXXX")
    address = models.TextField(default="unknown")
    gender = models.CharField(max_length=20, default="unknown")
    # age = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True)

    def get_age(self):
        import datetime

        if self.date_of_birth is None:
            return 0
        # parse date_of_birth to date if it be string
        dob = self.date_of_birth
        tod = datetime.date.today()

        my_age = (tod.year - dob.year) - \
            int((tod.month, tod.day) < (dob.month, dob.day))
        return my_age

    def get_email(self):
        from allauth.account.models import EmailAddress
        emails = EmailAddress.objects.filter(user_id=self.id, primary=True)
        if emails is None or 0 == len(emails) or len(emails) > 1:
            return ""
        return emails[0]

    def set_email(self, email):
        from allauth.account.models import EmailAddress
        old_primary = EmailAddress.objects.get_primary(self)
        e = EmailAddress.objects.create(user_id=self.id, email=email)
        if old_primary is None:
            e.set_as_primary()

    def get_emails(self):
        from allauth.account.models import EmailAddress
        return EmailAddress.objects.filter(user_id=self.id)

    def clean(self):
        super(User, self).clean()

        from django.utils.dateparse import parse_date
        from django.core.exceptions import ValidationError

        # assume if telephone have - will have two of them at between number 3-4 and 6-7
        if self.telephone[3] != "-":
            if len(self.telephone) != 10:
                raise ValidationError(
                    {'telephone': 'telephone in thailand must be 10 digit.'})
            self.telephone = self.telephone[:3] + "-" + self.telephone[3:6] + "-" + self.telephone[6:]
        else:
            if len(self.telephone) != 12:
                raise ValidationError(
                    {'telephone': 'telephone in thailand must be 10 digit.'})

        # 0[8|9]xxxxxxxx
        if self.telephone[0] != "0" or (self.telephone[1] != "8" and self.telephone[1] != "9" and self.telephone[1] != "X"):
            raise ValidationError({'telephone': 'invalid telephone number.'})
        # gender must be either male or female or unknown
        if self.gender != 'male' and self.gender != "female":
            self.gender = "unknown"
        # date_of_birth must be date object
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = parse_date(self.date_of_birth)

        if self.get_age() < 0:
            raise ValidationError(
                {'date_of_birth': 'birthday must be pass not future'})

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username + ": " + self.first_name + " " + self.last_name


# merge django auth user to customer
class Customer(models.Model):
    """customer information v1"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    classes = models.ForeignKey(
        'Class',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user)


class Class(models.Model):
    """membership class v1"""
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.TextField()

    def __str__(self):
        return self.name
