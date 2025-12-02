from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from training.models import Training


class Command(BaseCommand):
    help = 'Test video streaming functionality'

    def handle(self, *args, **options):
        self.stdout.write("=== Testing Video Streaming ===")

        # Test with Django test client
        client = Client()

        # Get the first training video
        training = Training.objects.first()
        if not training:
            self.stdout.write("❌ No training videos found in database")
            return

        self.stdout.write(f"Testing with video: {training.title}")
        self.stdout.write(f"Video file: {training.video_file}")

        # Test the training detail page
        detail_url = reverse('training:training_detail', kwargs={'pk': training.pk})
        self.stdout.write(f"Testing detail page: {detail_url}")

        response = client.get(detail_url)
        if response.status_code == 200:
            self.stdout.write("✅ Training detail page loads successfully")
        else:
            self.stdout.write(f"❌ Training detail page failed: {response.status_code}")

        # Test direct video access
        if training.video_file:
            video_url = training.video_file.url
            self.stdout.write(f"Testing video URL: {video_url}")

            response = client.get(video_url)
            if response.status_code == 200:
                self.stdout.write("✅ Video file accessible via Django")
                self.stdout.write(f"Content-Type: {response.get('Content-Type', 'Not set')}")
                self.stdout.write(f"Content-Length: {response.get('Content-Length', 'Not set')}")
            else:
                self.stdout.write(f"❌ Video file not accessible: {response.status_code}")

        # Test streaming view
        if training.video_file:
            stream_url = reverse('training:stream_video', kwargs={'video_path': str(training.video_file)})
            self.stdout.write(f"Testing stream URL: {stream_url}")

            response = client.get(stream_url)
            if response.status_code == 200:
                self.stdout.write("✅ Video streaming view works")
                self.stdout.write(f"Content-Type: {response.get('Content-Type', 'Not set')}")
                self.stdout.write(f"Accept-Ranges: {response.get('Accept-Ranges', 'Not set')}")
            else:
                self.stdout.write(f"❌ Video streaming view failed: {response.status_code}")

        # Test with range request (simulate video seeking)
        if training.video_file:
            stream_url = reverse('training:stream_video', kwargs={'video_path': str(training.video_file)})
            headers = {'HTTP_RANGE': 'bytes=0-1023'}

            response = client.get(stream_url, **headers)
            if response.status_code == 206:
                self.stdout.write("✅ Range requests supported")
                self.stdout.write(f"Content-Range: {response.get('Content-Range', 'Not set')}")
            else:
                self.stdout.write(f"⚠️ Range requests not working: {response.status_code}")

        self.stdout.write("\n=== Video Streaming Test Complete ===")
