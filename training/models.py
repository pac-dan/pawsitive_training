from django.db import models
from django.utils.text import slugify
from django.core.files.storage import default_storage

class TrainingCategory(models.Model):
    """
    Model to store training categories for organizing video lessons.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        """
        Automatically generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Training Categories"
class Training(models.Model):
    """
    Model to store training video lessons with optional subscription requirement.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(
        upload_to='training/videos/',
        storage=default_storage,
        blank=True,
        null=True,
        help_text="Upload training video file"
    )
    thumbnail = models.ImageField(
        upload_to='training/thumbnails/',
        storage=default_storage,
        blank=True,
        null=True,
        help_text="Upload video thumbnail image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    category = models.ForeignKey(
        TrainingCategory,
        on_delete=models.SET_NULL,
        related_name="trainings",
        null=True,
        blank=True
    )

    is_free = models.BooleanField(
        default=False,
        help_text="Mark this video as free to view without a subscription"
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'training_lesson'
        verbose_name = "Training"
        verbose_name_plural = "Training"
        ordering = ['order', 'title']