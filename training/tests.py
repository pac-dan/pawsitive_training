from django.test import TestCase
from .models import Training, TrainingCategory


class TrainingModelTest(TestCase):
    """Test cases for Training and TrainingCategory models"""

    def setUp(self):
        self.category = TrainingCategory.objects.create(
            name='Basic Training'
        )

    def test_training_category_creation(self):
        """Test creating a training category"""
        self.assertEqual(str(self.category), 'Basic Training')
        self.assertEqual(self.category.slug, 'basic-training')

    def test_training_creation(self):
        """Test creating a training lesson"""
        training = Training.objects.create(
            title='Sit Command',
            description='Teaching your dog to sit',
            category=self.category,
            is_free=True
        )
        self.assertEqual(str(training), 'Sit Command')
        self.assertTrue(training.is_free)
        self.assertEqual(training.category, self.category)

    def test_training_ordering(self):
        """Test that trainings are ordered correctly"""
        training1 = Training.objects.create(
            title='First Lesson',
            description='First',
            order=1
        )
        training2 = Training.objects.create(
            title='Second Lesson',
            description='Second',
            order=2
        )
        trainings = Training.objects.all()
        self.assertEqual(trainings[0], training1)
        self.assertEqual(trainings[1], training2)
