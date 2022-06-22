from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



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

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username', 'email']


    def __str__(self):
        """
        Строковое представление модели (отображается в консоли).
        String representation of the model (displayed in the console).
        """
        return self.username


# @admin.register(PostModel)
# class PostAdmin(admin.ModelAdmin):
#     ...
#     list_filter = (
#         ('is_visible', admin.BooleanFieldListFilter),
#         ('description', admin.EmptyFieldListFilter),
#     )