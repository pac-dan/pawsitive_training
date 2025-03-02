from django.db import models
from django.utils.text import slugify

class TrainingCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
class Training(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='training/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='training/thumbnails/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    # New field for categorizing training lessons:
    category = models.ForeignKey(
        TrainingCategory,
        on_delete=models.SET_NULL,
        related_name="trainings",
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'training_lesson'  # This is the original table name for Lesson
        verbose_name = "Training"
        verbose_name_plural = "Training"