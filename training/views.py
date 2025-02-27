from django.shortcuts import render, get_object_or_404
from .models import Lesson


def lessons_display(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons_display.html', {'lessons': lessons})

def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

