from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or "Untitled Lesson"