from django.db import models

class Training(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='training/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='training/thumbnails/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or "Untitled Lesson"
    
    class Meta:
        db_table = 'training_lesson'  # This is the original table name for Lesson
        verbose_name = "Training"
        verbose_name_plural = "Training"