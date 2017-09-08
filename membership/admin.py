from django.contrib import admin
from .models import Customer, Class, User

# -------------------------------------
# custom auth user
# -------------------------------------

from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'telephone', 'address', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'telephone', 'address', 'password', 'date_of_birth', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('firstname', 'lastname', 'email', 'is_active', 'is_staff')
    list_filter = ('firstname', 'email', 'telephone')
    fieldsets = (
        (None,                      {'fields': ('username', 'password')}),
        ('Personal info',            {'fields': ('first_name', 'last_name', 'email')}),
        ('Addition personal info',  {'fields': ('date_of_birth', 'telephone','address')}),
        ('Permissions',             {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates',         {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('firstname','lastname','email')}),
        ('Addition personal info', {'fields': ('date_of_birth', 'telephone','address')})
    )
    search_fields = ('firstname', 'telephone', 'address', 'email')
    ordering = ('firstname', 'email')

admin.site.register(User, UserAdmin)

# -------------------------------------
# other
# -------------------------------------

class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        model = Customer

class ClassAdmin(admin.ModelAdmin):
    class Meta:
        model = Class


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Class, ClassAdmin)
