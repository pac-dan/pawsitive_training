from training.models import Training
for t in Training.objects.order_by('-pk')[:3]:
    print(t.pk, t.title, t.video_file.name, bool(t.video_file.name))
