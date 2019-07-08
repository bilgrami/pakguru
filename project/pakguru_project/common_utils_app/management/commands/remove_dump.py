import os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'CSV list of app names \n'
        parser.add_argument('app_names', type=str, help=help_text)

    def handle(self, *args, **options):
        app_names = options['app_names']
        if not app_names:
            raise CommandError(f'App Names is required')

        apps = app_names.split(',')
        for app in apps:
            fixture_folder_path = f'../../{app}/fixtures'
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: E501
            root = os.path.join(BASE_DIR, fixture_folder_path)

            if not os.path.exists(root):
                raise CommandError('Folder "%s" does not exist' % root)
            else:
                print(f'[{app}] Found folder to remove files: {root}')
                for filename in os.listdir(root):
                    if filename.endswith(".json"):
                        input_file_path = os.path.join(root, filename)
                        os.remove(input_file_path)
                        print(f'Removed file: {input_file_path}')
