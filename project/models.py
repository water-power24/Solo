from django.db import models

class EverydayTask(models.Model):
    DAY_STATUS_CHOICES = [
        ('Sports', 'Спорт'),
        ('Mental growth and recovery', 'Прокачка интелекта и востановление'),
        ('Relaxation', 'отдых'),
        ('Professional skill-building', 'Прокачка професиональных навыков'),
        ('Theoretical study', 'теория'),
        ('adaptation','адаптация')
    ]

    day = models.PositiveBigIntegerField(unique=True, default=1)
    quote_1 = models.TextField(null=True, blank=True)  
    quote_2 = models.TextField(null=True, blank=True)  
    tasks = models.JSONField(default=list, blank=True)  
    quantity_task = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='static/img', blank=True, null=True)
    image_2 = models.ImageField(upload_to='static/img', blank=True, null=True)  
    image_3 = models.ImageField(upload_to='static/img', blank=True, null=True)
    trailer_video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Видео")  
    status = models.CharField(
        max_length=40,
        choices=DAY_STATUS_CHOICES,
        default='planned',
        verbose_name="Статус дня"
    )
    

    def __str__(self):
        return f"День {self.day}: {self.get_status_display()}"

    class Meta:
        verbose_name = "Ежедневное задание"
        verbose_name_plural = "Ежедневные задания"
        ordering = ['day']

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.username