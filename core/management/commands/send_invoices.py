from django.core.management.base import BaseCommand
from core.service import stark_svc


class Command(BaseCommand):
    help = 'Your costum command description'

    def handle(self, *args, **kwargs):
        stark_svc.send_invoices()
