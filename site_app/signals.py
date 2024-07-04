from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AlumniProfile, AlumniCommittee, Slider, AlbumPhoto, AboutUs, NewsPost, EventsPost, JobPosting, Responsibility
from django.conf import settings
from PIL import Image
# from .validators import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AlumniProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.alumniprofile.save()


# Resize Images Start

@receiver(post_save, sender=AlumniCommittee)
def resize_alumni_committee_image(sender, instance, created, **kwargs):
    if instance.committee_profile_picture:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['alumni_committee']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.committee_profile_picture.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.committee_profile_picture.path)


@receiver(post_save, sender=Slider)
def resize_alumni_slider_image(sender, instance, created, **kwargs):
    if instance.image:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['slider']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.image.path)


@receiver(post_save, sender=EventsPost)
def resize_alumni_event_image(sender, instance, created, **kwargs):
    if instance.image:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['event']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.image.path)


@receiver(post_save, sender=JobPosting)
def resize_alumni_job_image(sender, instance, created, **kwargs):
    if instance.company_logo:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['job']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.company_logo.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.company_logo.path)


@receiver(post_save, sender=Responsibility)
def resize_alumni_responsibility_image(sender, instance, created, **kwargs):
    if instance.image:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['responsibility']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.image.path)


@receiver(post_save, sender=AlumniProfile)
def resize_alumni_testimonial_image(sender, instance, created, **kwargs):
    if instance.profile_picture:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['testimonial']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.profile_picture.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.profile_picture.path)


@receiver(post_save, sender=NewsPost)
def resize_alumni_news_image(sender, instance, created, **kwargs):
    if instance.image:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['news']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.image.path)


@receiver(post_save, sender=AboutUs)
def resize_alumni_about_image(sender, instance, created, **kwargs):
    if instance.welcome_note_image:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['about_welcome_note_image']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.welcome_note_image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.welcome_note_image.path)

    else:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['about_other_image']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.description_image.path)
        mission_image = Image.open(instance.mission_image.path)
        vision_image = Image.open(instance.vision_image.path)
        achivements_image = Image.open(instance.achivements_image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.description_image.path)

        if mission_image.width != accepted_width or mission_image.height != accepted_height:
            mission_image = mission_image.resize(
                (accepted_width, accepted_height))
            mission_image.save(instance.mission_image.path)
        if vision_image.width != accepted_width or vision_image.height != accepted_height:
            vision_image = vision_image.resize(
                (accepted_width, accepted_height))
            vision_image.save(instance.vision_image.path)
        if achivements_image.width != accepted_width or achivements_image.height != accepted_height:
            achivements_image = achivements_image.resize(
                (accepted_width, accepted_height))
            achivements_image.save(instance.achivements_image.path)


@receiver(post_save, sender=AlbumPhoto)
def resize_alumni_gallery_image(sender, instance, created, **kwargs):
    if instance.photo:  # Check if image exists
        # Get the accepted dimensions from settings
        required_image_size_settings = settings.IMAGE_SIZES['gallery']

        accepted_width = required_image_size_settings['max_width']
        accepted_height = required_image_size_settings['max_height']
        # Open the uploaded image
        img = Image.open(instance.photo.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.photo.path)
