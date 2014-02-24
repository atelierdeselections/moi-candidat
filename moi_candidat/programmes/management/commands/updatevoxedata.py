from django.conf import settings
from django.core.management.base import BaseCommand

import voxe


class Command(BaseCommand):
    help = 'Update data from voxe.org API'

    def handle(self, *args, **options):
        # Set cache_disabled to force update
        voxe.Election(settings.VOXE_ELECTION_ID, cache_disabled=True)
        self.stdout.write('Data successfully updated.')
