import os
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_image_dimensions(image, required_width, required_height):
    width = image.width
    height = image.height
    if width != required_width or height != required_height:
        raise ValidationError("The image dimensions must be exactly {}x{} pixels.".format(
            required_width, required_height))
        
 

def validate_alumni_committee_image(image):
    image_settings = settings.IMAGE_SIZES['alumni_committee'] 
    validate_image_dimensions(image, image_settings['max_width'], image_settings['max_height'])

  # for more validation during upload add more function