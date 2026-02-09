import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def convert_to_webp(image_field, max_width=1200, quality=80):
    """Convert an uploaded image to WebP format and resize it."""
    if not image_field:
        return

    img = Image.open(image_field)

    # Convert RGBA/P to RGB (WebP doesn't always support transparency well)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize if wider than max_width
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # Save as WebP
    buffer = BytesIO()
    img.save(buffer, format='WEBP', quality=quality)
    buffer.seek(0)

    # Generate new filename with .webp extension
    old_name = os.path.splitext(image_field.name)[0]
    new_name = f"{old_name}.webp"

    return ContentFile(buffer.read(), name=os.path.basename(new_name))
