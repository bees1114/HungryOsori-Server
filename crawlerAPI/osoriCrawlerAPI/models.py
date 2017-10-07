from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError('No user Email, Give me Email!!')
        if not name:
            raise ValueError('No user name, Give me name!!')
        if not password:
            raise ValueError('No user password, Give me password!!')

        user = self.model(email=self.normalize_email(email), name=name, password=make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, password=password, name=name)
        user.is_admin=True
        user.save(using=self._db)
        return user



'''Models for user profile'''
class UserProfile(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', primary_key=True, max_length=100)
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_auth = models.CharField(max_length=100, default='False')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'password',]
    def is_authenticated(self):
        if self.is_auth is 'False':
            return False
        else:
            return True
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return UserProfile(value)

    def to_python(self, value):
        if isinstance(value, UserProfile):
            return value
        if value is None:
            return value
        return UserProfile(value)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ('created',)

'''Models for Crawler'''
class Crawler(models.Model):
    crawler_id=models.CharField(max_length=100, primary_key= True)
    thumbnail_url = models.CharField(max_length=100)
    link_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Crawler(value)

    def to_python(self, value):
        if isinstance(value, Crawler):
            return value
        if value is None:
            return value
        return Crawler(value)

    class Meta:
        ordering = ('title', 'created', 'crawler_id',)

'''Models for Information of who subscript which crawlers'''
class Subscription(models.Model):
    user_id = models.ForeignKey('UserProfile', on_delete=models.CASCADE,)
    crawler_id = models.CharField(max_length=100)
    latest_pushtime = models.DateField(auto_now_add=True)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Subscription(value)

    def to_python(self, value):
        if isinstance(value, Subscription):
            return value
        if value is None:
            return value
        return Subscription(value)

    class Meta:
        ordering=('user_id', 'crawler_id',)
        unique_together = (('user_id', 'crawler_id'),)

'''Models for user and who`s device token'''
class PushToken(models.Model):
    user_id = models.ForeignKey('UserProfile', on_delete=models.CASCADE,)
    push_token = models.CharField(max_length=100)
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return PushToken(value)

    def to_python(self, value):
        if isinstance(value, PushToken):
            return value
        if value is None:
            return value
        return PushToken(value)
    
    class Meta:
        ordering=('user_id',)
        unique_together = (('user_id', 'push_token'),)
