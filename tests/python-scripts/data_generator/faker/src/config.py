"""
Configuration settings for the data generator.
Centralizes all configuration to avoid magic numbers and strings.
"""

from enum import Enum
from typing import Dict
from pydantic import BaseModel, Field


class PaymentMethod(str, Enum):
    """Payment method enumeration."""

    CREDIT_CARD = "CREDIT_CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"
    BUY_NOW_PAY_LATER = "BUY_NOW_PAY_LATER"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class UserRole(str, Enum):
    """User role enumeration."""

    CUSTOMER = "customer"
    ADMIN = "admin"
    MANAGER = "manager"
    SALES_REP = "sales_rep"
    WAREHOUSE_STAFF = "warehouse_staff"


class GenerationConfig(BaseModel):
    """Configuration for data generation."""

    # Record counts
    num_users: int = Field(default=1000, description="Number of users to generate")
    num_categories: int = Field(
        default=1000, description="Number of categories to generate"
    )
    num_brands: int = Field(default=500, description="Number of brands to generate")
    num_product_images: int = Field(
        default=500, description="Number of product images to generate"
    )
    num_products: int = Field(
        default=1000, description="Number of products to generate"
    )
    num_favorites: int = Field(
        default=2000, description="Number of favorites to generate"
    )
    num_invoices: int = Field(default=800, description="Number of invoices to generate")
    num_invoice_items: int = Field(
        default=1500, description="Number of invoice items to generate"
    )
    num_payments: int = Field(default=800, description="Number of payments to generate")

    # Category generation settings
    min_categories_per_root: int = Field(
        default=15, description="Minimum subcategories per root category"
    )
    max_categories_per_root: int = Field(
        default=50, description="Maximum subcategories per root category"
    )
    enable_deep_hierarchy: bool = Field(
        default=True, description="Enable 3-level hierarchy"
    )

    # Business logic settings
    admin_totp_probability: float = Field(
        default=0.15, description="Probability of TOTP for admins"
    )
    user_totp_probability: float = Field(
        default=0.02, description="Probability of TOTP for regular users"
    )
    user_enabled_probability: float = Field(
        default=0.95, description="Probability of enabled users"
    )
    social_provider_probability: float = Field(
        default=0.25, description="Probability of social login"
    )
    password_probability: float = Field(
        default=0.95, description="Probability of having password"
    )

    # Product settings
    product_in_stock_probability: float = Field(
        default=0.85, description="Probability of product being in stock"
    )
    product_location_offer_probability: float = Field(
        default=0.1, description="Probability of location offer"
    )
    product_rental_probability: float = Field(
        default=0.05, description="Probability of rental product"
    )
    min_stock: int = Field(default=0, description="Minimum stock quantity")
    max_stock: int = Field(default=1000, description="Maximum stock quantity")
    min_price: float = Field(default=1.99, description="Minimum product price")
    max_price: float = Field(default=9999.99, description="Maximum product price")

    # Invoice settings
    min_invoice_items: int = Field(default=1, description="Minimum items per invoice")
    max_invoice_items: int = Field(default=10, description="Maximum items per invoice")
    min_quantity_per_item: int = Field(
        default=1, description="Minimum quantity per invoice item"
    )
    max_quantity_per_item: int = Field(
        default=5, description="Maximum quantity per invoice item"
    )

    # Favorites settings
    min_favorites_per_user: int = Field(
        default=0, description="Minimum favorites per user"
    )
    max_favorites_per_user: int = Field(
        default=20, description="Maximum favorites per user"
    )

    # File output settings
    output_directory: str = Field(
        default="output", description="Output directory for CSV files"
    )

    # Randomization seed
    random_seed: int = Field(
        default=42, description="Seed for reproducible randomization"
    )


# Default configuration instance
DEFAULT_CONFIG = GenerationConfig()

# User role distribution weights (must sum to 100 or be proportional)
USER_ROLE_WEIGHTS: Dict[UserRole, int] = {
    UserRole.CUSTOMER: 85,
    UserRole.ADMIN: 5,
    UserRole.MANAGER: 3,
    UserRole.SALES_REP: 4,
    UserRole.WAREHOUSE_STAFF: 3,
}

# Payment method distribution weights
PAYMENT_METHOD_WEIGHTS: Dict[PaymentMethod, int] = {
    PaymentMethod.CREDIT_CARD: 60,
    PaymentMethod.BANK_TRANSFER: 25,
    PaymentMethod.CASH_ON_DELIVERY: 10,
    PaymentMethod.BUY_NOW_PAY_LATER: 5,
}

# Payment status distribution weights
PAYMENT_STATUS_WEIGHTS: Dict[PaymentStatus, int] = {
    PaymentStatus.SUCCESS: 85,
    PaymentStatus.PENDING: 10,
    PaymentStatus.FAILED: 5,
}

# Countries with states (for realistic address generation)
COUNTRIES_WITH_STATES = {
    "US": True,
    "CA": True,
    "AU": True,
    "BR": True,
    "IN": True,
    "MX": True,
}

# Common file extensions for product images
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

# Photo stock websites for realistic image sources
PHOTO_STOCK_SITES = [
    "unsplash.com",
    "pexels.com",
    "pixabay.com",
    "freepik.com",
    "shutterstock.com",
    "getty.com",
    "istock.com",
]

# Invoice number patterns
INVOICE_NUMBER_PATTERNS = [
    "INV-{year}-{number:06d}",
    "INV{year}{month:02d}{number:04d}",
    "{year}-INV-{number:05d}",
    "I{year}{number:06d}",
]
