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
        
        missing_files = 0
        for training in trainings:
            self.stdout.write(f"\nTraining: {training.title}")
            self.stdout.write(f"  Video file: {training.video_file}")
            if training.video_file:
                if settings.DEBUG:
                    # Only check local files in debug mode
                    full_path = os.path.join(media_dir, str(training.video_file))
                    if os.path.exists(full_path):
                        self.stdout.write(f"  ✅ File exists at: {full_path}")
                    else:
                        self.stdout.write(f"  ❌ File missing at: {full_path}")
                        missing_files += 1
                else:
                    # In production, assume S3 files exist if video_file is set
                    self.stdout.write("  ✅ Video file configured (production mode)")
            else:
                self.stdout.write("  ⚠️  No video file assigned")
                missing_files += 1
        
        # Check URL configuration
        self.stdout.write(f"\n=== Configuration Summary ===")
        self.stdout.write(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        
        if not settings.DEBUG:
            if hasattr(settings, 'AWS_ACCESS_KEY_ID') and settings.AWS_ACCESS_KEY_ID:
                self.stdout.write("✅ AWS S3 configured for media files")
            else:
                self.stdout.write("⚠️  AWS S3 not configured - check production media setup")
        
        # Summary
        if missing_files > 0:
            self.stdout.write(self.style.WARNING(f"\n⚠️  {missing_files} training(s) missing video files"))
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ All training videos configured correctly")) 