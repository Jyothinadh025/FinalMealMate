# delivery/seed_data.py
from pathlib import Path
from django.core.files import File
from django.db import transaction

# import models inside function to avoid import-time errors when running manage.py commands
def run(wipe_existing=False):
    """
    Restore sample restaurants & items from images in your repo.
    Run from: python manage.py shell
        >>> from delivery.seed_data import run
        >>> run()
    Set wipe_existing=True to delete existing restaurants/items first (use with caution).
    """
    print("Restoring restaurants and menu items...")

    # compute repository root and candidate static paths
    # file is at: <repo>/delivery/seed_data.py
    repo_root = Path(__file__).resolve().parent.parent  # <repo>
    # Candidate static locations (common layouts)
    candidate_paths = [
        repo_root / "delivery" / "static" / "delivery",   # delivery/static/delivery/...
        repo_root / "static" / "delivery",                # static/delivery/...
        repo_root / "delivery" / "static",                # delivery/static/...
        repo_root / "static",                             # static/...
    ]

    # restaurant & item subfolders we expect
    restaurant_subdirs = ["restaurant_images", "restaurant_images", "images", "restaurant_images"]
    item_subdirs = ["item_images", "item_images", "item_images", "item_images"]

    # pick the first candidate that exists
    static_base = None
    for cand in candidate_paths:
        if cand.exists():
            static_base = cand
            break

    if static_base is None:
        # fallback: look for delivery/static/delivery/restaurant_images specifically
        alt = repo_root / "delivery" / "static" / "delivery"
        print("⚠️ Could not find a static base in candidates. Will still try common subfolders relative to repo root.")
        static_base = repo_root  # we'll build full paths below

    print("Using static base:", static_base)

    # helper to resolve possible locations (if static_base is repo root, try multiple)
    def resolve_restaurant_folder():
        tries = [
            static_base / "restaurant_images",
            static_base / "delivery" / "restaurant_images",
            repo_root / "delivery" / "restaurant_images",
            repo_root / "delivery" / "static" / "delivery" / "restaurant_images",
            repo_root / "static" / "delivery" / "restaurant_images",
        ]
        for p in tries:
            if p.exists():
                return p
        return tries[0]  # last fallback

    def resolve_item_folder():
        tries = [
            static_base / "item_images",
            static_base / "delivery" / "item_images",
            repo_root / "delivery" / "item_images",
            repo_root / "delivery" / "static" / "delivery" / "item_images",
            repo_root / "static" / "delivery" / "item_images",
        ]
        for p in tries:
            if p.exists():
                return p
        return tries[0]

    restaurant_folder = resolve_restaurant_folder()
    item_folder = resolve_item_folder()

    print("Restaurant image folder:", restaurant_folder)
    print("Item image folder:", item_folder)

    # import models now (after repo root computed)
    from delivery.models import Restaurant, Item

    # If you want to wipe existing restaurants/items first (use with care)
    if wipe_existing:
        print("Wiping existing Restaurant and Item records (you chose wipe_existing=True)...")
        with transaction.atomic():
            Item.objects.all().delete()
            Restaurant.objects.all().delete()

    # -------------------------
    # 1) Create Restaurants
    # -------------------------
    restaurants = [
        ("Dominos", "dominos.jpg", "Pizza, Fast Food", 5.0),
        ("KFC", "kfc.jpg", "Chicken, Burgers, Soft Drinks", 4.7),
        ("Hyderabad DumBiryani", "Hyderabad_Dum_Biryani.jpg", "Biryani, Non-Veg", 4.8),
        ("Truffles", "truffles.jpg", "Pizza, Garlic bread, Cold drink", 4.5),
        ("5 STAR", "5_star.jpg", "Special Dishes", 4.6),
    ]

    created_restaurants = {}

    for name, filename, cuisine, rating in restaurants:
        image_path = restaurant_folder / filename
        if not image_path.exists():
            print(f"⚠ Image not found: {image_path}  (restaurant: {name}) — creating restaurant without picture")
            rest = Restaurant.objects.create(name=name, cuisine=cuisine, rating=rating)
        else:
            rest = Restaurant.objects.create(name=name, cuisine=cuisine, rating=rating)
            with open(image_path, "rb") as f:
                rest.picture.save(filename, File(f), save=True)
            print(f"✔ Created restaurant with image: {name} -> {filename}")

        created_restaurants[name] = rest

    # -------------------------
    # 2) Add Menu Items
    # -------------------------
    menu = {
        "Dominos": [
            ("cheese burst pizza", "full of cheese", 249.0, "dominos.jpg"),
            ("garlic bread", "crispy and cheesy", 149.0, "garlic_bread.jpg"),
            ("Chicken Cheese Pizza", "full of cheese", 249.0, "dominos.jpg"),
        ],
        "KFC": [
            ("Spicy Wings", "Hot and Juicy", 199.0, "kfc.jpg"),
            ("Grilled Chicken Wings", "Very Hot and Special", 299.0, "kfc.jpg"),
            ("Coca Cola", "Soft Drink", 99.0, "kfc.jpg"),
        ],
        "Hyderabad DumBiryani": [
            ("Hyderabad Special Biryani", "Special Home Made Biryanis", 399.0, "Hyderabad_Dum_Biryani.jpg"),
        ],
        "Truffles": [
            ("Truffles Special", "Pizza, Garlic bread, Cold drink", 299.0, "truffles.jpg"),
        ],
        "5 STAR": [
            ("5 Star Special Biryani", "Yummy and Taste", 399.0, "5_star.jpg"),
        ],
    }

    for rest_name, items in menu.items():
        restaurant = created_restaurants.get(rest_name)
        if not restaurant:
            print(f"⚠ Restaurant not created earlier: {rest_name}. Skipping its items.")
            continue

        for item_name, description, price, image_filename in items:
            image_path = item_folder / image_filename
            item = Item.objects.create(
                restaurant=restaurant,
                name=item_name,
                description=description,
                price=price
            )
            if image_path.exists():
                with open(image_path, "rb") as f:
                    item.picture.save(image_filename, File(f), save=True)
                print(f"   ➕ Added item with image: {item_name} -> {image_filename}")
            else:
                print(f"   ⚠ Item image not found: {image_path} (item: {item_name}) — item created without picture")

    print("\n✨ DONE — All restaurants & items restored successfully!")
