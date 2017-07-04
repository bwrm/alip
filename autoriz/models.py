from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    company = models.CharField(max_length=40, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    street_number = models.CharField(max_length=10, null=True, blank=True)
    route = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=40, null=True, blank=True)
    administrative_area_level_1 = models.CharField(max_length=100, null=True, blank=True)
    administrative_area_level_2 = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self):
        return reverse('autoriz:plainuser-profile')


class Producer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, blank=True, primary_key=True)
    public_name = models.CharField(max_length=30)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    location = models.CharField(max_length=40, null=True, blank=True)
    street_number = models.CharField(max_length=10, null=True, blank=True)
    route = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=40, null=True, blank=True)
    administrative_area_level_1 = models.CharField(max_length=100, null=True, blank=True)
    administrative_area_level_2 = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    postal_delivery = models.BooleanField(default=False)
    pickup_delivery = models.BooleanField(default=False)
    canprintinvoce = models.BooleanField(default=False)
    delivery_time = models.PositiveSmallIntegerField(default=3, verbose_name='days')
    is_cncmill = models.BooleanField(default=True)
    is_3d = models.BooleanField(default=False)
    is_cnclaser = models.BooleanField(default=False)
    another_equipment = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.public_name


class TypeServices(models.Model):
    services = models.CharField(max_length=35)


class CncService(models.Model):
    name = models.CharField(max_length=50)
    lenx = models.CharField(max_length=10)
    leny = models.CharField(max_length=10)
    lenz = models.CharField(max_length=10)
    mincost = models.CharField(max_length=10)
