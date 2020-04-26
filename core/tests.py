from core.notifications import EmailSender
from django.test import TestCase

# Create your tests here.
class CoreTestCase(TestCase):

    def test_send_email(self):
        subject = "TestSubject"
        message = "TestMessage"
        recipients = ["charlie.gillions@gmail.com"]
        EmailSender.send(subject, message, recipients)
