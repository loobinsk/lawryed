from time import sleep

from django.core.management.base import BaseCommand, CommandError
# from products.tasks import domain_check


# class Command(BaseCommand):
#     help = 'Check few site'
#
#     # def add_arguments(self, parser):
#     #     parser.add_argument('poll_ids', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         no_delay = True
#         for i in range(100):
#             res = domain_check(no_delay)
#             if res == -1:
#                 sleep(30)
#
#             self.stdout.write(self.style.SUCCESS(f'Updated sites: {res}'))
#         pass
