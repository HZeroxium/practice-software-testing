"""
Base models for data generation using Pydantic for type safety and validation.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for environments without Pydantic
    from dataclasses import dataclass, field
    from typing import Union

    # Simple BaseModel replacement
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def model_dump(self) -> Dict[str, Any]:
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def Field(default=None, description=""):
        return default


class UserModel(BaseModel):
    """User model matching the database schema."""

    id: str
    uid: Optional[str] = None
    provider: Optional[str] = None
    first_name: str
    last_name: str
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[str] = None  # ISO date string
    email: str
    password: Optional[str] = None
    role: str
    enabled: bool = True
    failed_login_attempts: int = 0
    totp_secret: Optional[str] = None
    totp_enabled: bool = False
    totp_verified_at: Optional[str] = None  # ISO datetime string
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class CategoryModel(BaseModel):
    """Category model matching the database schema."""

    id: str
    name: str
    slug: str
    parent_id: Optional[str] = None
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class BrandModel(BaseModel):
    """Brand model matching the database schema."""

    id: str
    name: str
    slug: str
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class ProductImageModel(BaseModel):
    """Product image model matching the database schema."""

    id: str
    by_name: str
    by_url: str
    source_name: str
    source_url: str
    file_name: str
    title: str
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class ProductModel(BaseModel):
    """Product model matching the database schema."""

    id: str
    name: str
    description: str
    price: str  # Decimal as string for CSV compatibility
    is_location_offer: bool = False
    is_rental: bool = False
    category_id: str
    brand_id: str
    product_image_id: str
    in_stock: bool = True
    stock: int = 0
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class FavoriteModel(BaseModel):
    """Favorite model matching the database schema."""

    id: str
    user_id: str
    product_id: str
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class InvoiceModel(BaseModel):
    """Invoice model matching the database schema."""

    id: str
    invoice_number: str
    invoice_date: str  # ISO date string
    billing_address: str
    billing_city: str
    billing_state: Optional[str] = None
    billing_country: str
    billing_postcode: Optional[str] = None
    user_id: str
    total: str  # Decimal as string for CSV compatibility
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class InvoiceItemModel(BaseModel):
    """Invoice item model matching the database schema."""

    id: str
    invoice_id: str
    product_id: str
    quantity: int
    unit_price: str  # Decimal as string for CSV compatibility
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string


class PaymentModel(BaseModel):
    """Payment model matching the database schema."""

    id: str
    invoice_id: str
    method: str  # Enum value as string
    status: str  # Enum value as string
    payment_reference_id: Optional[str] = None
    created_at: str  # ISO datetime string
    updated_at: str  # ISO datetime string
