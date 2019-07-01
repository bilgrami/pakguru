import os

from django.core import signing
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        fixture_folder_path = '../../pakguru_app/fixtures'
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root = os.path.join(BASE_DIR, fixture_folder_path)

        if not os.path.exists(root):
            raise CommandError('Folder "%s" does not exist' % root)
        else:
            print(f'Found folder: {root}')
            for filename in os.listdir(root):
                if filename.endswith(".json"):
                    input_file_path = os.path.join(root, filename)
                    output_file = os.path.join(root, 'enc', filename + '.enc')
                    json_data = open(input_file_path, 'r').read()
                    enc_json_data = signing.dumps(json_data)
                    with open(output_file, "w") as enc_file:
                        enc_file.write(enc_json_data)
