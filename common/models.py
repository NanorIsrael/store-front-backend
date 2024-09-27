from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator



# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given email and password.
#         """
#         if not email:
#             raise ValueError('The Email field must be set')

#         email = self.normalize_email(email)
#         username = extra_fields.get('username') or email  # Default to email as username if not provided
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractUser):
	username_validator = UnicodeUsernameValidator()

	email = models.EmailField(unique=True)
	# username = models.CharField(
	# 	_("username"),
	# 	max_length=250,
	# 	unique=True,
	# 	help_text=_(
	# 		"150 characters or fewer. Letters, digits and @/./+/-/_ only."
	# 	),
	# 	validators=[username_validator],
	# 	error_messages={
	# 		"unique": _("A user with that username already exists."),
	# 	},
	# 	blank=True,
	# 	null=True
	# )
	# USERNAME_FIELD = 'email'
	# REQUIRED_FIELDS = []
# objects = UserManager()