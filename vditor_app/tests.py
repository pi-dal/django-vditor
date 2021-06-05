from django.test import TestCase     
from .models import VditorTest

class ModelTest(TestCase):

    def setUp(self):
        VditorTest.objects.create(name='hello-world', content='# hello-world')

    def test_model(self):
        result = VditorTest.objects.get(name='hello-world', content='# hello-world')