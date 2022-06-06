from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Создание модели пользователя.
    Creating a user model.   
    """
    email = models.EmailField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты'
    )
    username = models.CharField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=150,
        verbose_name="Уникальный юзернейм",
        help_text="Введите уникальный юзернейм"

    )
    first_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name="Имя",
        help_text="Введите имя"
    )
    last_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name="Фамилия",
        help_text="Введите фамилию"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']


    def __str__(self):
        """
        Строковое представление модели (отображается в консоли).
        String representation of the model (displayed in the console).
        """
        return self.username