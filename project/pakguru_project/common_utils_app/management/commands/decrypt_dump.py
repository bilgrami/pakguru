import os

from django.core import signing
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
            fixture_folder_path = f'../../{app}/fixtures/enc'
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: E501
            root = os.path.join(BASE_DIR, fixture_folder_path)

            if not os.path.exists(root):
                raise CommandError('Folder "%s" does not exist' % root)
            else:
                print(f'[{app}] Found folder to decrypt: {root}')
                output_folder = os.path.join(root, '../')
                for filename in os.listdir(root):
                    if filename.endswith(".enc"):
                        json_file_path = os.path.join(root, filename)
                        output_file = filename.replace('.enc', '')
                        output_file_path = os.path.join(output_folder,
                                                        output_file)
                        enc_json_data = open(json_file_path, 'r').read()
                        json_data = signing.loads(enc_json_data)
                        with open(output_file_path, "w") as enc_file:
                            enc_file.write(json_data)
