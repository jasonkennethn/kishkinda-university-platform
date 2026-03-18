from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('university_admin', 'University Admin'),
        ('college_admin', 'College Admin'),
        ('registrar', 'Registrar'),
        ('exam_controller', 'Exam Controller'),
        ('finance_admin', 'Finance Admin'),
        ('hod', 'Head of Department'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    @property
    def is_super_admin_user(self): return self.role == 'super_admin'
    
    @property
    def is_university_admin_user(self): return self.role == 'university_admin'
    
    @property
    def is_college_admin_user(self): return self.role == 'college_admin'
    
    @property
    def is_registrar_user(self): return self.role == 'registrar'
    
    @property
    def is_exam_controller_user(self): return self.role == 'exam_controller'
    
    @property
    def is_finance_admin_user(self): return self.role == 'finance_admin'
    
    @property
    def is_hod_user(self): return self.role == 'hod'
    
    @property
    def is_faculty_user(self): return self.role == 'faculty'
    
    @property
    def is_student_user(self): return self.role == 'student'
