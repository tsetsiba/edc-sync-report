from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Generates sync verification report then send an email to the monitoring group.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            dest='send',
            default=False,
            help='send sync verification report.',
        )

    def handle(self, *args, **options):
        if options['send']:
            self.stdout.write(self.style.SUCCESS(
                'Preparing a sync verification this might take a while.'))