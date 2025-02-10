from django.db import models

# Create your models here.
class BotUsers(models.Model):
    SLIDE_TYPE_CHOICES = [
        ('super', 'Супер'),
        ('admin', 'Адміністратор'),
        ('delivery', 'Доставник'),
    ]

    name = models.CharField(max_length=255, verbose_name="Ім'я")
    access_level = models.CharField(
        max_length=12,
        choices=SLIDE_TYPE_CHOICES,
        default='admin',
        verbose_name="Рівень доступу"
    )
    user_id = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name="ID користувача")

    def __str__(self):
        return f'[{self.user_id}] {self.name} з рівнем досткпу {self.access_level}'
