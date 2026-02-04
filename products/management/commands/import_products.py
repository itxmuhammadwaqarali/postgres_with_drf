import json
import os
from decimal import Decimal
from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django.apps import apps

try:
    import requests
except ImportError:
    requests = None


class Command(BaseCommand):
    help = 'Import products from a JSON file into the Product model. Supports optional image download.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='products/seed_products.json', help='Path to JSON file (relative to project root).')
        parser.add_argument('--download-images', action='store_true', help='Download images from URLs and attach to ImageField.')
        parser.add_argument('--dry-run', action='store_true', help='Parse and show what would be created without saving.')

    def handle(self, *args, **options):
        Product = apps.get_model('products', 'Product')

        file_path = options['file']
        download_images = options['download_images']
        dry_run = options['dry_run']

        if download_images and requests is None:
            raise CommandError('requests is required to download images. Install it and try again.')

        # Resolve path
        if not os.path.isabs(file_path):
            base = settings.BASE_DIR
            file_path = os.path.join(base, file_path)

        if not os.path.exists(file_path):
            raise CommandError(f'JSON file not found: {file_path}')

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created = 0
        for item in data:
            name = item.get('name')
            description = item.get('description', '')
            size = item.get('size', '')
            available = item.get('available', True)
            rating = item.get('rating')
            image_url = item.get('image')
            color = item.get('color', '')
            created_at = item.get('created_at')

            # Normalize rating
            if rating in (None, ''):
                rating_val = None
            else:
                try:
                    rating_val = Decimal(str(rating))
                except Exception:
                    rating_val = None

            defaults = {
                'description': description,
                'size': size,
                'available': available,
                'rating': rating_val,
                'color': color,
            }

            if dry_run:
                self.stdout.write(self.style.NOTICE(f"Would create/update product: {name} ({defaults}) image={image_url}"))
                continue

            product, created_flag = Product.objects.update_or_create(
                name=name,
                defaults=defaults,
            )

            # Optionally download image
            if download_images and image_url:
                try:
                    resp = requests.get(image_url, stream=True, timeout=15)
                    resp.raise_for_status()
                    parsed = urlparse(image_url)
                    filename = os.path.basename(parsed.path)
                    if not filename:
                        filename = f"product_{product.pk}.jpg"
                    media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
                    os.makedirs(media_dir, exist_ok=True)
                    local_path = os.path.join(media_dir, filename)
                    with open(local_path, 'wb') as out_file:
                        for chunk in resp.iter_content(chunk_size=8192):
                            out_file.write(chunk)
                    # Attach to model
                    with open(local_path, 'rb') as fobj:
                        product.image.save(filename, File(fobj), save=True)
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f"Failed to download image {image_url}: {e}"))

            # Set created_at if provided and possible
            if created_at:
                try:
                    # created_at is auto_now_add; to set it we must update directly
                    from django.utils.dateparse import parse_datetime
                    dt = parse_datetime(created_at)
                    if dt is not None:
                        Product.objects.filter(pk=product.pk).update(created_at=dt)
                except Exception:
                    pass

            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Import finished. {created} new products created.'))
