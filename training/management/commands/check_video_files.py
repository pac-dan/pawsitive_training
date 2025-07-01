from django.core.management.base import BaseCommand
from django.conf import settings
from training.models import Training
import os

class Command(BaseCommand):
    help = 'Check the status of video files in the training app'

    def handle(self, *args, **options):
        self.stdout.write("=== Video File Status Check ===")
        
        # Check media directory
        media_dir = settings.MEDIA_ROOT
        video_dir = os.path.join(media_dir, 'training', 'videos')
        
        self.stdout.write(f"Media root: {media_dir}")
        self.stdout.write(f"Video directory: {video_dir}")
        
        if os.path.exists(video_dir):
            video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
            self.stdout.write(f"Found {len(video_files)} video files in directory")
            for video in video_files[:5]:  # Show first 5
                self.stdout.write(f"  - {video}")
        else:
            self.stdout.write("❌ Video directory does not exist!")
        
        # Check database records
        trainings = Training.objects.all()
        self.stdout.write(f"\nFound {trainings.count()} training records in database")
        
        for training in trainings:
            self.stdout.write(f"\nTraining: {training.title}")
            self.stdout.write(f"  Video file: {training.video_file}")
            if training.video_file:
                full_path = os.path.join(media_dir, str(training.video_file))
                if os.path.exists(full_path):
                    self.stdout.write(f"  ✅ File exists at: {full_path}")
                else:
                    self.stdout.write(f"  ❌ File missing at: {full_path}")
            else:
                self.stdout.write("  ⚠️  No video file assigned")
        
        # Check URL configuration
        self.stdout.write(f"\n=== URL Configuration ===")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        if not settings.DEBUG:
            self.stdout.write("Production mode detected")
            if hasattr(settings, 'AWS_ACCESS_KEY_ID') and settings.AWS_ACCESS_KEY_ID:
                self.stdout.write("✅ AWS S3 configured")
            else:
                self.stdout.write("⚠️  AWS S3 not configured - using local media files") 