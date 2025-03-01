from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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

class CustomUser(AbstractUser):
    level = models.PositiveIntegerField(default=1)
    max_pushups = models.PositiveIntegerField(null=True, blank=True, verbose_name="Максимум в отжиманиях")
    max_pullups = models.PositiveIntegerField(null=True, blank=True, verbose_name="Максимум в подтягиваниях")
    max_run_1km = models.FloatField(null=True, blank=True, verbose_name="Время на 1 км (мин)")

    def __str__(self):
        return self.username
    
class UserProgress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_completed_day = models.PositiveIntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habit = models.CharField(max_length=255)
    completed_days = models.IntegerField(default=0)  
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit} ({self.completed_days}/21)"

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    day = models.IntegerField()  
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'day')  

    def __str__(self):
        return f"{self.habit.habit} - День {self.day}: {'Выполнено' if self.completed else 'Не выполнено'}"
