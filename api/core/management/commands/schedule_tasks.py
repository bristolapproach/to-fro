from django.core.management.base import BaseCommand, CommandError
from core.scheduler import setup


class Command(BaseCommand):
    help = 'Schedules repeated tasks'

    def handle(self, *args, **options):
        setup()
