from django.db import models

# Модель для каруселі
class CarouselImage(models.Model):
    SLIDE_TYPE_CHOICES = [
        ('#catalog', 'Каталог'),
        ('#about-sadhu', 'Про садху'),
        ('#about-us', 'Про нас'),
    ]

    title = models.CharField(max_length=200, verbose_name="Текст")  # Заголовок слайду
    button = models.CharField(max_length=200, verbose_name="Текст кнопки")  # Опис слайду
    image = models.ImageField(upload_to='carousel/', verbose_name="Зображення")  # Зображення
    order = models.PositiveIntegerField(default=0, unique=True,  verbose_name="Порядок відображення")  # Порядок
    is_active = models.BooleanField(default=True, verbose_name="Активний")  # Відображати чи ні
    slide_type = models.CharField(
        max_length=12,
        choices=SLIDE_TYPE_CHOICES,
        default='#catalog',
        verbose_name="Тип слайду"
    )

    class Meta:
        ordering = ['order']  # Сортування за полем order

    def __str__(self):
        return self.title


# Модель для футера
class FooterInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    instagram_link = models.URLField(blank=True, verbose_name="Instagram")

    def __str__(self):
        return f"Контакти: {self.phone}, {self.instagram_link}"
