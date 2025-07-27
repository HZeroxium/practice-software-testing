"""
Abstract base generator and individual generators for each database table.
Implements SOLID principles with separation of concerns.
"""

import csv
import random
from abc import ABC, abstractmethod
from datetime import datetime, UTC
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any, Set
from pathlib import Path

import ulid
from faker import Faker
from slugify import slugify

from .models import (
    UserModel,
    CategoryModel,
    BrandModel,
    ProductImageModel,
    ProductModel,
    FavoriteModel,
    InvoiceModel,
    InvoiceItemModel,
    PaymentModel,
)
from .config import GenerationConfig, UserRole, PaymentMethod, PaymentStatus
from .providers import ECommerceProvider, HardwareToolProvider


class BaseGenerator(ABC):
    """Abstract base class for all data generators."""

    def __init__(self, config: GenerationConfig, faker_instance: Faker):
        self.config = config
        self.fake = faker_instance
        self.used_identifiers: Set[str] = set()

    @abstractmethod
    def generate(self, count: int, **kwargs) -> List[Dict[str, Any]]:
        """Generate data records."""
        pass

    def generate_ulid(self) -> str:
        """Generate a unique ULID."""
        while True:
            new_id = ulid.new().str
            if new_id not in self.used_identifiers:
                self.used_identifiers.add(new_id)
                return new_id

    def generate_unique_slug(self, name: str, used_slugs: Set[str]) -> str:
        """Generate unique slug with fallback numbering."""
        base_slug = slugify(name)
        if base_slug not in used_slugs:
            used_slugs.add(base_slug)
            return base_slug

        counter = 1
        while f"{base_slug}-{counter}" in used_slugs:
            counter += 1

        final_slug = f"{base_slug}-{counter}"
        used_slugs.add(final_slug)
        return final_slug

    def current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(UTC).isoformat(sep=" ")

    def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> None:
        """Save data to CSV file."""
        if not data:
            print(f"⚠️  No data to save for {filename}")
            return

        output_path = Path(self.config.output_directory)
        output_path.mkdir(exist_ok=True)

        filepath = output_path / filename

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

        print(f"  ▶ Saved {len(data)} rows to {filepath}")


class UserGenerator(BaseGenerator):
    """Generator for user data."""

    def generate(self, count: int, **kwargs) -> List[Dict[str, Any]]:
        """Generate user records."""
        users = []
        used_emails = set()

        print(f"🔄 Generating {count} users...")

        for i in range(count):
            # if i % 100 == 0:
            #     print(f"  Progress: {i}/{count} users generated")

            uid = self.generate_ulid()
            first = self.fake.first_name()
            last = self.fake.last_name()
            role = self.fake.user_role()

            # Generate unique email
            email_attempts = 0
            while email_attempts < 10:
                try:
                    email = self.fake.business_email(first, last)
                    if email not in used_emails:
                        used_emails.add(email)
                        break
                except:
                    email = self.fake.unique.email()
                    break
                email_attempts += 1
            else:
                email = self.fake.unique.email()

            # Realistic date generation
            created = self.fake.date_time_between(start_date="-2y", end_date="now")
            updated = self.fake.date_time_between(start_date=created, end_date="now")

            # Role-based customization
            enabled = (
                True
                if role == UserRole.ADMIN
                else self.fake.boolean(
                    chance_of_getting_true=int(
                        self.config.user_enabled_probability * 100
                    )
                )
            )
            failed_attempts = 0 if enabled else self.fake.random_int(0, 3)

            # TOTP settings
            if role in [UserRole.ADMIN, UserRole.MANAGER]:
                totp_enabled = self.fake.boolean(
                    chance_of_getting_true=int(self.config.admin_totp_probability * 100)
                )
            else:
                totp_enabled = self.fake.boolean(
                    chance_of_getting_true=int(self.config.user_totp_probability * 100)
                )

            totp_secret = (
                self.fake.hexify(text="^^^^^^^^^^^^^^^^") if totp_enabled else None
            )
            totp_verified = (
                self.fake.date_time_between(start_date=created, end_date="now")
                if totp_enabled
                else None
            )

            # Social login provider
            provider = None
            uid_field = None
            if self.fake.boolean(
                chance_of_getting_true=int(
                    self.config.social_provider_probability * 100
                )
            ):
                provider = self.fake.random_element(
                    ["google", "facebook", "github", "microsoft"]
                )
                uid_field = self.fake.uuid4()

            user = UserModel(
                id=uid,
                uid=uid_field,
                provider=provider,
                first_name=first,
                last_name=last,
                street=self.fake.street_address(),
                city=self.fake.city(),
                state=(
                    self.fake.state()
                    if self.fake.country_code() in ["US", "CA", "AU"]
                    else None
                ),
                country=self.fake.country_code(),
                postal_code=self.fake.postcode(),
                phone=self.fake.phone_number(),
                dob=self.fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat(),
                email=email,
                password=(
                    "$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi"
                    if self.fake.boolean(
                        chance_of_getting_true=int(
                            self.config.password_probability * 100
                        )
                    )
                    else None
                ),
                role=role,
                enabled=enabled,
                failed_login_attempts=failed_attempts,
                totp_secret=totp_secret,
                totp_enabled=totp_enabled,
                totp_verified_at=(
                    totp_verified.isoformat(sep=" ") if totp_verified else None
                ),
                created_at=created.isoformat(sep=" "),
                updated_at=updated.isoformat(sep=" "),
            )

            users.append(user.model_dump())

        print(f"✅ Generated {len(users)} users")
        return users


class CategoryGenerator(BaseGenerator):
    """Generator for category data with hierarchical structure."""

    def generate(self, count: int, **kwargs) -> List[Dict[str, Any]]:
        """Generate category records with proper hierarchy."""
        try:
            categories = []
            used_slugs = set()
            root_categories = []  # Store (id, name) tuples for root categories only
            all_categories = (
                []
            )  # Store (id, name) tuples for all categories for parenting

            print(f"🔄 Generating {count} categories...")

            # Phase 1: Generate root categories
            from .constants import TOOL_CATEGORIES

            root_category_names = list(TOOL_CATEGORIES.keys())
            for category_name in root_category_names:
                if len(categories) >= count:
                    break

                cid = self.generate_ulid()
                slug = self.generate_unique_slug(category_name, used_slugs)

                category = CategoryModel(
                    id=cid,
                    name=category_name,
                    slug=slug,
                    parent_id=None,
                    created_at=self.current_timestamp(),
                    updated_at=self.current_timestamp(),
                )

                categories.append(category.model_dump())
                root_categories.append((cid, category_name))
                all_categories.append((cid, category_name))

            print(f"  ▶ Generated {len(categories)} root categories")

            # Phase 2: Generate subcategories
            remaining = count - len(categories)
            if remaining > 0:
                subcategory_count = 0
                for parent_id, parent_name in root_categories:
                    if subcategory_count >= remaining:
                        break

                    # Ensure parent_name exists in TOOL_CATEGORIES
                    if parent_name not in TOOL_CATEGORIES:
                        continue

                    subcategories = TOOL_CATEGORIES[parent_name]["subcategories"]
                    for subcat_name in subcategories.keys():
                        if subcategory_count >= remaining:
                            break

                        cid = self.generate_ulid()
                        slug = self.generate_unique_slug(subcat_name, used_slugs)

                        category = CategoryModel(
                            id=cid,
                            name=subcat_name,
                            slug=slug,
                            parent_id=parent_id,
                            created_at=self.current_timestamp(),
                            updated_at=self.current_timestamp(),
                        )

                        categories.append(category.model_dump())
                        all_categories.append((cid, subcat_name))
                        subcategory_count += 1

                print(f"  ▶ Generated {subcategory_count} subcategories")

            # Phase 3: Generate additional specialized categories if needed
            remaining = count - len(categories)
            if remaining > 0:
                specialized_count = 0
                max_attempts = remaining * 3  # Prevent infinite loops
                attempts = 0

                while specialized_count < remaining and attempts < max_attempts:
                    attempts += 1
                    parent_id, parent_name = self.fake.random_element(all_categories)

                    # Generate variations
                    variations = self.fake.generate_category_variations(parent_name, 3)
                    for variation in variations:
                        if specialized_count >= remaining:
                            break
                        if variation == parent_name:  # Skip if same as parent
                            continue

                        # Check if variation already exists
                        if any(cat["name"] == variation for cat in categories):
                            continue

                        cid = self.generate_ulid()
                        slug = self.generate_unique_slug(variation, used_slugs)

                        category = CategoryModel(
                            id=cid,
                            name=variation,
                            slug=slug,
                            parent_id=parent_id,
                            created_at=self.current_timestamp(),
                            updated_at=self.current_timestamp(),
                        )

                        categories.append(category.model_dump())
                        all_categories.append((cid, variation))
                        specialized_count += 1

                print(f"  ▶ Generated {specialized_count} specialized categories")

            print(f"✅ Generated {len(categories)} categories total")
            return categories

        except Exception as e:
            print(f"❌ Error generating categories: {e}")
            print(f"   Available TOOL_CATEGORIES keys: {list(TOOL_CATEGORIES.keys())}")
            raise


class BrandGenerator(BaseGenerator):
    """Generator for brand data."""

    def generate(self, count: int, **kwargs) -> List[Dict[str, Any]]:
        """Generate brand records."""
        brands = []
        used_slugs = set()

        print(f"🔄 Generating {count} brands...")

        # Use real tool brands and generate additional ones
        from .providers import ECommerceProvider

        base_brands = ECommerceProvider.TOOL_BRANDS.copy()

        for i in range(count):
            if i < len(base_brands):
                brand_name = base_brands[i]
            else:
                # Generate fictional brands for additional count
                brand_name = (
                    f"{self.fake.company().replace(',', '').replace('.', '')} Tools"
                )

            bid = self.generate_ulid()
            slug = self.generate_unique_slug(brand_name, used_slugs)

            brand = BrandModel(
                id=bid,
                name=brand_name,
                slug=slug,
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            brands.append(brand.model_dump())

        print(f"✅ Generated {len(brands)} brands")
        return brands


class ProductImageGenerator(BaseGenerator):
    """Generator for product image data with Pixabay API integration."""

    def __init__(self, config: GenerationConfig, faker_instance: Faker):
        super().__init__(config, faker_instance)
        self.pixabay_service = None
        self._setup_pixabay_service()

    def _setup_pixabay_service(self) -> None:
        """Setup Pixabay service if API key is provided."""
        if (
            self.config.enable_pixabay_integration
            and hasattr(self.config, "pixabay_api_key")
            and self.config.pixabay_api_key
        ):

            try:
                from .pixabay_service import create_pixabay_service
                from pathlib import Path

                cache_dir = (
                    Path(self.config.output_directory) / "cache" / "pixabay"
                    if self.config.pixabay_cache_enabled
                    else None
                )
                self.pixabay_service = create_pixabay_service(
                    api_key=self.config.pixabay_api_key, cache_dir=cache_dir
                )
                print(
                    "🎨 Pixabay API integration enabled - fetching realistic product images"
                )
            except ImportError:
                print(
                    "⚠️ Pixabay service not available, using fallback image generation"
                )
        else:
            print("ℹ️ Using synthetic image URLs (set pixabay_api_key for real images)")

    def generate(
        self, count: int, categories: List[Dict] = None, **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate product image records with realistic images from Pixabay when possible."""
        images = []
        pixabay_images_used = 0
        fallback_images_used = 0

        print(f"🔄 Generating {count} product images...")

        # If categories are provided, we can use them for better image matching
        available_categories = categories or []

        # Prefetch images for all categories to improve cache hit ratio
        if self.pixabay_service and available_categories:
            category_names = [cat["name"] for cat in available_categories]
            self.pixabay_service.prefetch_category_images(
                category_names, images_per_category=30
            )

        for i in range(count):
            iid = self.generate_ulid()

            # Select a random category if available for image context
            category_context = None
            if available_categories:
                category_context = self.fake.random_element(available_categories)
                category_name = category_context["name"]
            else:
                # Use tool subcategory from providers as fallback
                category_name = self.fake.tool_subcategory_name()

            # Try to get real image from Pixabay
            pixabay_image = None
            if self.pixabay_service:
                try:
                    pixabay_image = self.pixabay_service.get_image_for_category(
                        category_name=category_name
                    )
                except Exception as e:
                    print(f"⚠️ Pixabay API error: {e}")

            if pixabay_image:
                # Use real Pixabay image data
                pixabay_images_used += 1

                # Extract file extension from URL
                url_parts = pixabay_image.web_format_url.split(".")
                extension = f".{url_parts[-1]}" if len(url_parts) > 1 else ".jpg"

                # Generate meaningful filename based on tags and category
                primary_tag = (
                    pixabay_image.tags.split(",")[0].strip()
                    if pixabay_image.tags
                    else category_name
                )
                filename = self.fake.product_image_filename(primary_tag)

                # Use actual Pixabay metadata
                photographer = pixabay_image.user
                photographer_url = f"https://pixabay.com/users/{pixabay_image.user}-{pixabay_image.user_id}/"
                source = "Pixabay"
                source_url = pixabay_image.web_format_url
                title = f"{primary_tag.title()} - Professional Tool Photography"

            else:
                # Use fallback synthetic data
                fallback_images_used += 1

                photographer = self.fake.photographer_name()
                source = self.fake.photo_source()

                # Generate realistic image title
                title = f"{category_name} - Professional Tool Photography"

                filename = self.fake.product_image_filename(category_name)
                source_url = self.fake.photo_url(source, filename)
                photographer_url = self.fake.photographer_url(photographer, source)

            image = ProductImageModel(
                id=iid,
                by_name=photographer,
                by_url=photographer_url,
                source_name=source,
                source_url=source_url,
                file_name=filename,
                title=title,
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            images.append(image.model_dump())

        # Print generation summary
        print(f"✅ Generated {len(images)} product images")
        if self.pixabay_service:
            print(f"  📸 Real Pixabay images: {pixabay_images_used}")
            print(f"  🎭 Fallback images: {fallback_images_used}")

            # Show performance stats
            stats = self.pixabay_service.get_performance_stats()
            if stats["total_requests"] > 0:
                print(
                    f"  📊 API efficiency: {stats['cache_hit_ratio']}% cache hit ratio"
                )

        return images


class ProductGenerator(BaseGenerator):
    """Generator for product data."""

    def generate(
        self,
        count: int,
        categories: List[Dict],
        brands: List[Dict],
        images: List[Dict],
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """Generate product records."""
        products = []

        print(f"🔄 Generating {count} products...")

        for i in range(count):
            # if i % 100 == 0:
            #     print(f"  Progress: {i}/{count} products generated")

            pid = self.generate_ulid()

            # Select random category, brand, and image
            category = self.fake.random_element(categories)
            brand = self.fake.random_element(brands)
            image = self.fake.random_element(images)

            # Generate product name and description
            product_name = self.fake.product_name(category["name"], brand["name"])
            description = self.fake.product_description(category["name"])

            # Generate price
            price = Decimal(
                self.fake.random.uniform(self.config.min_price, self.config.max_price)
            )
            price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # Generate stock and availability
            in_stock = self.fake.boolean(
                chance_of_getting_true=int(
                    self.config.product_in_stock_probability * 100
                )
            )
            stock = (
                self.fake.random_int(self.config.min_stock, self.config.max_stock)
                if in_stock
                else 0
            )

            # Special product types
            is_location_offer = self.fake.boolean(
                chance_of_getting_true=int(
                    self.config.product_location_offer_probability * 100
                )
            )
            is_rental = self.fake.boolean(
                chance_of_getting_true=int(self.config.product_rental_probability * 100)
            )

            product = ProductModel(
                id=pid,
                name=product_name,
                description=description,
                price=str(price),
                is_location_offer=is_location_offer,
                is_rental=is_rental,
                category_id=category["id"],
                brand_id=brand["id"],
                product_image_id=image["id"],
                in_stock=in_stock,
                stock=stock,
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            products.append(product.model_dump())

        print(f"✅ Generated {len(products)} products")
        return products


class FavoriteGenerator(BaseGenerator):
    """Generator for favorite data."""

    def generate(
        self, count: int, users: List[Dict], products: List[Dict], **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate favorite records."""
        favorites = []
        used_combinations = set()

        print(f"🔄 Generating {count} favorites...")

        attempts = 0
        max_attempts = count * 3  # Prevent infinite loops

        while len(favorites) < count and attempts < max_attempts:
            user = self.fake.random_element(users)
            product = self.fake.random_element(products)

            # Ensure unique user-product combination
            combination = (user["id"], product["id"])
            if combination in used_combinations:
                attempts += 1
                continue

            used_combinations.add(combination)

            fid = self.generate_ulid()

            favorite = FavoriteModel(
                id=fid,
                user_id=user["id"],
                product_id=product["id"],
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            favorites.append(favorite.model_dump())
            attempts += 1

        print(f"✅ Generated {len(favorites)} favorites")
        return favorites


class InvoiceGenerator(BaseGenerator):
    """Generator for invoice data."""

    def generate(self, count: int, users: List[Dict], **kwargs) -> List[Dict[str, Any]]:
        """Generate invoice records."""
        invoices = []
        used_invoice_numbers = set()

        print(f"🔄 Generating {count} invoices...")

        for i in range(count):
            # if i % 100 == 0:
            #     print(f"  Progress: {i}/{count} invoices generated")

            iid = self.generate_ulid()
            user = self.fake.random_element(users)

            # Generate unique invoice number
            current_year = datetime.now().year
            invoice_year = self.fake.random_int(current_year - 1, current_year)
            sequence = i + 1

            invoice_number = self.fake.invoice_number(invoice_year, sequence)
            while invoice_number in used_invoice_numbers:
                sequence += count
                invoice_number = self.fake.invoice_number(invoice_year, sequence)
            used_invoice_numbers.add(invoice_number)

            # Generate invoice date
            invoice_date = self.fake.date_between(
                start_date=f"-{365}d", end_date="today"
            )

            # Billing address (can be different from user address)
            billing_address = self.fake.street_address()
            billing_city = self.fake.city()
            billing_country = self.fake.country_code()
            billing_state = (
                self.fake.state() if billing_country in ["US", "CA", "AU"] else None
            )
            billing_postcode = self.fake.postcode()

            # Total will be calculated by invoice items generator
            total = Decimal("0.00")

            invoice = InvoiceModel(
                id=iid,
                invoice_number=invoice_number,
                invoice_date=invoice_date.isoformat(),
                billing_address=billing_address,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_country=billing_country,
                billing_postcode=billing_postcode,
                user_id=user["id"],
                total=str(total),  # Will be updated after items are generated
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            invoices.append(invoice.model_dump())

        print(f"✅ Generated {len(invoices)} invoices")
        return invoices


class InvoiceItemGenerator(BaseGenerator):
    """Generator for invoice item data."""

    def generate(
        self, count: int, invoices: List[Dict], products: List[Dict], **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate invoice item records."""
        invoice_items = []
        invoice_totals = {}

        print(f"🔄 Generating {count} invoice items...")

        # Distribute items across invoices
        items_per_invoice = count // len(invoices)
        remaining_items = count % len(invoices)

        item_count = 0
        for i, invoice in enumerate(invoices):
            # Determine how many items for this invoice
            num_items = items_per_invoice
            if i < remaining_items:
                num_items += 1

            # Ensure minimum items per invoice
            num_items = max(num_items, self.config.min_invoice_items)
            num_items = min(num_items, self.config.max_invoice_items)

            invoice_total = Decimal("0.00")

            for j in range(num_items):
                if item_count >= count:
                    break

                iid = self.generate_ulid()
                product = self.fake.random_element(products)

                quantity = self.fake.random_int(
                    self.config.min_quantity_per_item, self.config.max_quantity_per_item
                )

                # Use product price as unit price with small variation
                base_price = Decimal(product["price"])
                price_variation = self.fake.random.uniform(0.9, 1.1)  # ±10% variation
                unit_price = (base_price * Decimal(str(price_variation))).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

                line_total = unit_price * quantity
                invoice_total += line_total

                item = InvoiceItemModel(
                    id=iid,
                    invoice_id=invoice["id"],
                    product_id=product["id"],
                    quantity=quantity,
                    unit_price=str(unit_price),
                    created_at=self.current_timestamp(),
                    updated_at=self.current_timestamp(),
                )

                invoice_items.append(item.model_dump())
                item_count += 1

            invoice_totals[invoice["id"]] = str(invoice_total)

        print(f"✅ Generated {len(invoice_items)} invoice items")

        # Update invoice totals (this would be done in the main orchestrator)
        return invoice_items, invoice_totals


class PaymentGenerator(BaseGenerator):
    """Generator for payment data."""

    def generate(
        self, count: int, invoices: List[Dict], **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate payment records."""
        payments = []

        print(f"🔄 Generating {count} payments...")

        # Generate payments for invoices (some invoices might have multiple payments)
        selected_invoices = self.fake.random_elements(
            elements=invoices, length=count, unique=False
        )

        for i, invoice in enumerate(selected_invoices):
            # if i % 100 == 0:
            #     print(f"  Progress: {i}/{count} payments generated")

            pid = self.generate_ulid()

            # Select payment method based on weights
            method = random.choices(
                list(PaymentMethod),
                weights=[60, 25, 10, 5],  # CREDIT_CARD, BANK_TRANSFER, COD, BNPL
                k=1,
            )[0]

            # Select payment status based on weights
            status = random.choices(
                list(PaymentStatus),
                weights=[85, 10, 5],  # SUCCESS, PENDING, FAILED
                k=1,
            )[0]

            # Generate payment reference ID
            payment_reference_id = None
            if status in [PaymentStatus.SUCCESS, PaymentStatus.PENDING]:
                payment_reference_id = self.fake.payment_reference_id(method.value)

            payment = PaymentModel(
                id=pid,
                invoice_id=invoice["id"],
                method=method.value,
                status=status.value,
                payment_reference_id=payment_reference_id,
                created_at=self.current_timestamp(),
                updated_at=self.current_timestamp(),
            )

            payments.append(payment.model_dump())

        print(f"✅ Generated {len(payments)} payments")
        return payments
