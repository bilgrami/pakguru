import os

from django.core import signing
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        fixture_folder_path = '../../pakguru_app/fixtures/enc'
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root = os.path.join(BASE_DIR, fixture_folder_path)

        if not os.path.exists(root):
            raise CommandError('Folder "%s" does not exist' % root)
        else:
            print(f'Found folder: {root}')
            output_folder = os.path.join(root, '../')
            for filename in os.listdir(root):
                if filename.endswith(".enc"):
                    json_file_path = os.path.join(root, filename)
                    output_file = filename.replace('.enc', '')
                    output_file_path = os.path.join(output_folder, output_file)
                    enc_json_data = open(json_file_path, 'r').read()
                    json_data = signing.loads(enc_json_data)
                    with open(output_file_path, "w") as enc_file:
                        enc_file.write(json_data)
