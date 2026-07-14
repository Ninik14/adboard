from django.core.exceptions import ValidationError
import os

def validate_image_upload(image):
    extension = os.path.splitext(image.name)[1].lower()
    allowed_extensions = [".jpg", ".jpeg", ".png"]

    if extension not in allowed_extensions:
        raise ValidationError(
            "Only JPG, JPEG and PNG images are allowed."
        )
    
    max_size = 5 * 1024 * 1024

    if image.size > max_size:
        raise ValidationError(
            "Image size must be less than 5 MB."
        )