import os
from django.conf import settings
from cloudinary.uploader import upload
from delivery.models import Restaurant, Item

# Local directories
RESTAURANT_DIR = os.path.join(settings.BASE_DIR, "media/delivery/restaurant_images")
ITEM_DIR = os.path.join(settings.BASE_DIR, "media/delivery/item_images")

def upload_restaurant_images():
    print("Uploading Restaurant images...")
    for r in Restaurant.objects.all():
        filename = r.picture.name if r.picture else None

        if not filename:
            continue

        local_path = os.path.join(settings.BASE_DIR, filename)

        if not os.path.exists(local_path):
            print("Missing:", local_path)
            continue

        result = upload(local_path)
        r.picture = result["url"]
        r.save()
        print("Uploaded:", r.name)

def upload_item_images():
    print("Uploading Item images...")
    for i in Item.objects.all():
        filename = i.picture.name if i.picture else None

        if not filename:
            continue

        local_path = os.path.join(settings.BASE_DIR, filename)

        if not os.path.exists(local_path):
            print("Missing:", local_path)
            continue

        result = upload(local_path)
        i.picture = result["url"]
        i.save()
        print("Uploaded:", i.name)

def run_all():
    upload_restaurant_images()
    upload_item_images()
    print("DONE — All images moved to Cloudinary!")
