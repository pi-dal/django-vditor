from django.test import TestCase     
from .models import VditorTest

class ModelTest(TestCase):

    def setUp(self):
        VditorTest.objects.create(Text='#hello-world')

    def test_model(self):
        result = VditorTest.objects.get(Text="#hello-world")