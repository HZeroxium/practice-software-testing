"""
Enhanced Faker providers for realistic e-commerce data generation.
"""

import random
from typing import List, Dict, Any, Optional
from faker import Faker
from faker.providers import BaseProvider
from .constants import (
    TOOL_CATEGORIES,
    BRAND_MODIFIERS,
    SIZE_MODIFIERS,
    MATERIAL_MODIFIERS,
    APPLICATION_MODIFIERS,
    USER_ROLES,
    REALISTIC_DOMAINS,
)


class ECommerceProvider(BaseProvider):
    """Enhanced provider for e-commerce specific data generation."""

    # Tool brands based on real hardware manufacturers
    TOOL_BRANDS = [
        "DeWalt",
        "Makita",
        "Milwaukee",
        "Bosch",
        "Ryobi",
        "Black & Decker",
        "Craftsman",
        "Stanley",
        "Husky",
        "Kobalt",
        "Porter Cable",
        "Festool",
        "Hilti",
        "Metabo",
        "Hitachi",
        "Ridgid",
        "Worx",
        "Skil",
        "Dremel",
        "Klein Tools",
        "Fluke",
        "Snap-on",
        "Mac Tools",
        "Matco",
        "Proto",
        "Bahco",
        "Facom",
        "Gedore",
        "Hazet",
        "Stahlwille",
        "Wiha",
        "Channellock",
        "Irwin",
        "Lenox",
        "Starrett",
        "Mitutoyo",
        "Brown & Sharpe",
        "Tekton",
        "Performance Tool",
        "ABN",
        "ARES",
        "MAXIMUM",
        "Mastercraft",
    ]

    # Product description templates
    PRODUCT_DESCRIPTION_TEMPLATES = [
        "Professional grade {tool_type} designed for {application}. Features {material} construction with {feature} for enhanced performance and durability.",
        "High-quality {tool_type} perfect for {application}. Built with {material} and includes {feature} for maximum efficiency.",
        "Durable {tool_type} ideal for {application} tasks. Made from {material} with {feature} technology.",
        "Heavy-duty {tool_type} suitable for {application}. Constructed with {material} and featuring {feature}.",
        "Precision {tool_type} engineered for {application}. Premium {material} construction with advanced {feature}.",
        "Industrial {tool_type} designed for demanding {application}. Robust {material} build with innovative {feature}.",
        "Compact {tool_type} perfect for {application} in tight spaces. Lightweight {material} with efficient {feature}.",
        "Ergonomic {tool_type} optimized for {application}. Superior {material} design with comfortable {feature}.",
    ]

    PRODUCT_FEATURES = [
        "ergonomic grip",
        "anti-slip surface",
        "corrosion resistance",
        "precision engineering",
        "shock absorption",
        "quick-release mechanism",
        "magnetic tip",
        "LED work light",
        "variable speed control",
        "safety lock",
        "dust collection",
        "battery indicator",
        "overload protection",
        "reversible operation",
        "depth adjustment",
        "angle guide",
        "non-slip base",
        "quick-change system",
        "vibration reduction",
        "weatherproof design",
    ]

    APPLICATIONS = [
        "construction",
        "automotive repair",
        "woodworking",
        "metalworking",
        "electrical work",
        "plumbing",
        "HVAC",
        "maintenance",
        "DIY projects",
        "professional use",
        "industrial applications",
        "home improvement",
        "precision assembly",
        "field service",
    ]

    # Photo attribution sources
    PHOTO_SOURCES = [
        "Unsplash",
        "Pexels",
        "Pixabay",
        "Freepik",
        "Shutterstock",
        "Getty Images",
        "iStock",
        "Adobe Stock",
        "Depositphotos",
        "123RF",
        "Dreamstime",
        "Alamy",
    ]

    PHOTOGRAPHER_NAMES = [
        "Alex Thompson",
        "Sarah Chen",
        "Michael Rodriguez",
        "Emma Wilson",
        "David Kim",
        "Lisa Anderson",
        "James Taylor",
        "Maria Garcia",
        "Ryan Johnson",
        "Nina Patel",
        "Tom Brown",
        "Jessica Lee",
        "Mark Davis",
        "Ana Martinez",
        "Chris Wilson",
        "Sophie Turner",
        "Daniel Smith",
        "Rachel Green",
        "Kevin Wong",
        "Laura Miller",
    ]

    def tool_brand(self) -> str:
        """Generate a realistic tool brand name."""
        return self.random_element(self.TOOL_BRANDS)

    def product_name(self, category_name: str, brand: str) -> str:
        """Generate a realistic product name based on category and brand."""
        size_modifier = (
            self.random_element(SIZE_MODIFIERS)
            if self.generator.boolean(chance_of_getting_true=30)
            else ""
        )
        material_modifier = (
            self.random_element(MATERIAL_MODIFIERS)
            if self.generator.boolean(chance_of_getting_true=25)
            else ""
        )

        # Build product name
        parts = [brand]
        if size_modifier:
            parts.append(size_modifier)
        if material_modifier:
            parts.append(material_modifier)
        parts.append(category_name)

        # Add model number occasionally
        if self.generator.boolean(chance_of_getting_true=40):
            model = self.generator.bothify(text="??-####")
            parts.append(model)

        return " ".join(parts)

    def product_description(self, tool_type: str) -> str:
        """Generate a realistic product description."""
        template = self.random_element(self.PRODUCT_DESCRIPTION_TEMPLATES)

        return template.format(
            tool_type=tool_type.lower(),
            application=self.random_element(self.APPLICATIONS),
            material=self.random_element(MATERIAL_MODIFIERS).lower(),
            feature=self.random_element(self.PRODUCT_FEATURES),
        )

    def product_image_filename(self, product_name: str) -> str:
        """Generate a realistic image filename."""
        # Convert product name to filename-friendly format
        base_name = product_name.lower().replace(" ", "_").replace("-", "_")
        base_name = "".join(c for c in base_name if c.isalnum() or c == "_")

        # Add image variant
        variant = self.random_element(["main", "detail", "angle", "use", "packaging"])
        extension = self.random_element([".jpg", ".jpeg", ".png", ".webp"])

        return f"{base_name}_{variant}{extension}"

    def photographer_name(self) -> str:
        """Generate a realistic photographer name."""
        return self.random_element(self.PHOTOGRAPHER_NAMES)

    def photo_source(self) -> str:
        """Generate a realistic photo source."""
        return self.random_element(self.PHOTO_SOURCES)

    def photo_url(self, source: str, filename: str) -> str:
        """Generate a realistic photo URL."""
        domain_map = {
            "Unsplash": "unsplash.com",
            "Pexels": "pexels.com",
            "Pixabay": "pixabay.com",
            "Freepik": "freepik.com",
            "Shutterstock": "shutterstock.com",
            "Getty Images": "gettyimages.com",
            "iStock": "istockphoto.com",
            "Adobe Stock": "stock.adobe.com",
        }

        domain = domain_map.get(source, "example.com")
        photo_id = self.generator.random_int(100000, 9999999)

        return f"https://images.{domain}/photos/{photo_id}/{filename}"

    def photographer_url(self, photographer: str, source: str) -> str:
        """Generate a realistic photographer profile URL."""
        domain_map = {
            "Unsplash": "unsplash.com",
            "Pexels": "pexels.com",
            "Pixabay": "pixabay.com",
        }

        domain = domain_map.get(source, "example.com")
        username = photographer.lower().replace(" ", "")

        return f"https://{domain}/@{username}"

    def invoice_number(self, year: int, sequence: int) -> str:
        """Generate a realistic invoice number."""
        patterns = [
            f"INV-{year}-{sequence:06d}",
            f"INV{year}{sequence:06d}",
            f"{year}-INV-{sequence:05d}",
            f"I{year}{sequence:06d}",
        ]
        return self.random_element(patterns)

    def payment_reference_id(self, method: str) -> str:
        """Generate a realistic payment reference ID based on method."""
        if method == "CREDIT_CARD":
            return f"CC{self.generator.random_int(100000000000, 999999999999)}"
        elif method == "BANK_TRANSFER":
            return f"BT{self.generator.random_int(1000000000, 9999999999)}"
        elif method == "CASH_ON_DELIVERY":
            return f"COD{self.generator.random_int(100000, 999999)}"
        elif method == "BUY_NOW_PAY_LATER":
            return f"BNPL{self.generator.random_int(10000000, 99999999)}"
        else:
            return f"PAY{self.generator.random_int(1000000, 9999999)}"


class HardwareToolProvider(BaseProvider):
    """Provider specifically for hardware and tool domain data."""

    TOOL_CATEGORIES = TOOL_CATEGORIES
    USER_ROLES = USER_ROLES
    REALISTIC_DOMAINS = REALISTIC_DOMAINS
    BRAND_MODIFIERS = BRAND_MODIFIERS
    SIZE_MODIFIERS = SIZE_MODIFIERS
    MATERIAL_MODIFIERS = MATERIAL_MODIFIERS
    APPLICATION_MODIFIERS = APPLICATION_MODIFIERS

    def tool_category_name(self) -> str:
        """Generate a realistic tool category name."""
        return self.random_element(list(self.TOOL_CATEGORIES.keys()))

    def tool_subcategory_name(self, parent_category: str = None) -> str:
        """Generate a realistic tool subcategory name."""
        if parent_category and parent_category in self.TOOL_CATEGORIES:
            subcategories = self.TOOL_CATEGORIES[parent_category]["subcategories"]
            return self.random_element(list(subcategories.keys()))

        # Random subcategory from any category
        all_subcategories = []
        for cat_data in self.TOOL_CATEGORIES.values():
            all_subcategories.extend(list(cat_data["subcategories"].keys()))
        return self.random_element(all_subcategories)

    def user_role(self) -> str:
        """Generate a realistic user role with proper distribution."""
        weights = [85, 5, 3, 4, 3]  # Most users are customers
        return random.choices(self.USER_ROLES, weights=weights, k=1)[0]

    def business_email(self, first_name: str, last_name: str) -> str:
        """Generate more realistic email addresses."""
        domain = self.random_element(self.REALISTIC_DOMAINS)
        patterns = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()}@{domain}",
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}{self.random_int(1, 999)}@{domain}",
        ]
        return self.random_element(patterns)

    def generate_category_variations(self, base_name: str, count: int = 5) -> List[str]:
        """Generate realistic variations of a category name."""
        variations = [base_name]

        for _ in range(count - 1):
            modifier_type = random.choice(["brand", "size", "material", "application"])

            if modifier_type == "brand":
                modifier = self.random_element(self.BRAND_MODIFIERS)
                variations.append(f"{modifier} {base_name}")
            elif modifier_type == "size":
                modifier = self.random_element(self.SIZE_MODIFIERS)
                variations.append(f"{modifier} {base_name}")
            elif modifier_type == "material":
                modifier = self.random_element(self.MATERIAL_MODIFIERS)
                variations.append(f"{modifier} {base_name}")
            elif modifier_type == "application":
                modifier = self.random_element(self.APPLICATION_MODIFIERS)
                variations.append(f"{modifier} {base_name}")

        return list(set(variations))
