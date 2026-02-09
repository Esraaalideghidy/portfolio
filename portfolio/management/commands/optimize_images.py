import os
import glob
from PIL import Image
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Convert and resize all existing media images to WebP format and update database paths'

    def handle(self, *args, **options):
        media_root = str(settings.MEDIA_ROOT)
        extensions = ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG')
        converted = 0

        # Step 1: Convert files on disk
        for ext in extensions:
            for filepath in glob.glob(os.path.join(media_root, '**', ext), recursive=True):
                try:
                    img = Image.open(filepath)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')

                    # Resize if wider than 1200px
                    if img.width > 1200:
                        ratio = 1200 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((1200, new_height), Image.LANCZOS)

                    # Save as WebP
                    webp_path = os.path.splitext(filepath)[0] + '.webp'
                    img.save(webp_path, 'WEBP', quality=80)

                    # Remove old file
                    os.remove(filepath)

                    new_size = os.path.getsize(webp_path)
                    self.stdout.write(f'  {os.path.basename(filepath)} -> {os.path.basename(webp_path)} ({new_size // 1024}KB)')
                    converted += 1
                except Exception as e:
                    self.stderr.write(f'  Error: {filepath} - {e}')

        self.stdout.write(self.style.SUCCESS(f'\nConverted {converted} image files to WebP.'))

        # Step 2: Update database paths
        from portfolio.models import Profile, PortfolioItem, PortfolioImage
        updated = 0

        for Model in [Profile, PortfolioItem, PortfolioImage]:
            for obj in Model.objects.all():
                if obj.image and not obj.image.name.endswith('.webp'):
                    new_name = os.path.splitext(obj.image.name)[0] + '.webp'
                    Model.objects.filter(pk=obj.pk).update(image=new_name)
                    self.stdout.write(f'  DB: {obj.image.name} -> {new_name}')
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f'Updated {updated} database paths to .webp.'))
        self.stdout.write(self.style.SUCCESS(f'\nDone!'))
