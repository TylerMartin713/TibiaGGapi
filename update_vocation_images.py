#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaGGproject.settings")
django.setup()

from TibiaGGapi.models import Vocation

# Default Tibia vocation image URLs
vocation_images = {
    "sorcerer": "https://static.wikia.nocookie.net/tibia/images/e/e5/Sorcerer_Banner.png/revision/latest?cb=20241120235908&path-prefix=en",
    "druid": "https://static.wikia.nocookie.net/tibia/images/8/8f/Druid_Banner.png/revision/latest?cb=20241121000008&path-prefix=en",
    "knight": "https://static.wikia.nocookie.net/tibia/images/d/d1/Knight_Banner.png/revision/latest?cb=20241120235951&path-prefix=en",
    "paladin": "https://static.wikia.nocookie.net/tibia/images/2/22/Paladin_Banner.png/revision/latest?cb=20241120235931&path-prefix=en",
    "none": "https://static.tibia.com/images/global/vocations/vocation_none.png",
}

print("Updating vocation images...")

for vocation in Vocation.objects.all():
    vocation_name = vocation.name.lower()

    if vocation_name in vocation_images:
        vocation.image_url = vocation_images[vocation_name]
        vocation.save()
        print(f"Updated {vocation.name} with image URL")
    else:
        # Try to match partial names
        for key, url in vocation_images.items():
            if key in vocation_name:
                vocation.image_url = url
                vocation.save()
                print(f"Updated {vocation.name} with {key} image URL")
                break
        else:
            print(f"No image found for: {vocation.name}")

print("Done updating vocation images!")
