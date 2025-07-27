"""
Pixabay API Service for Realistic Product Images

This module provides integration with Pixabay API to fetch real, relevant images
for products based on their categories. It includes caching, rate limiting,
and fallback mechanisms to ensure robust image generation.

Features:
- Category-based image search
- API rate limiting and error handling
- Image caching to reduce API calls
- Fallback to synthetic URLs when API fails
- Search term optimization for hardware/tools domain

@author Software Testing Team
@version 1.0.0
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlencode
import random
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class PixabayImage:
    """Represents a Pixabay image with metadata."""

    id: int
    web_format_url: str
    large_image_url: str
    preview_url: str
    tags: str
    user: str
    user_id: int
    views: int
    downloads: int
    favorites: int
    page_url: str


class PixabayImageService:
    """Service for fetching realistic product images from Pixabay API."""

    # Category to search terms mapping for hardware/tools domain
    CATEGORY_SEARCH_TERMS = {
        "Hand Tools": [
            "hammer",
            "screwdriver",
            "wrench",
            "pliers",
            "hand tools",
            "toolkit",
        ],
        "Power Tools": [
            "drill",
            "saw",
            "grinder",
            "power tools",
            "electric tools",
            "cordless",
        ],
        "Safety Equipment": [
            "safety helmet",
            "safety glasses",
            "gloves",
            "safety gear",
            "protection",
        ],
        "Measuring Tools": [
            "ruler",
            "tape measure",
            "caliper",
            "measuring tools",
            "precision",
        ],
        "Cutting Tools": ["knife", "blade", "cutting tool", "scissors", "cutter"],
        "Fasteners": ["screws", "bolts", "nuts", "fasteners", "hardware"],
        "Storage": ["toolbox", "storage", "cabinet", "organizer", "tool chest"],
        "Automotive Tools": ["car tools", "automotive", "mechanic tools", "garage"],
        "Garden Tools": ["garden tools", "shovel", "rake", "pruning", "gardening"],
        "Workshop Equipment": [
            "workbench",
            "vise",
            "workshop",
            "machinery",
            "equipment",
        ],
        "Electrical Tools": [
            "electrical",
            "wire",
            "voltage",
            "multimeter",
            "electrical tools",
        ],
        "Plumbing Tools": ["plumbing", "pipe", "plumber tools", "wrench", "pipe tools"],
        "Construction": ["construction", "building", "contractor", "heavy duty"],
        "Precision Tools": ["precision", "measurement", "calibration", "professional"],
        "Maintenance": ["maintenance", "repair", "service", "industrial"],
    }

    # Additional generic search terms for variety
    GENERIC_TOOL_TERMS = [
        "tools",
        "hardware",
        "equipment",
        "professional tools",
        "industrial tools",
        "workshop",
        "construction tools",
        "repair tools",
        "diy tools",
        "craftsman",
    ]

    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[Path] = None):
        """
        Initialize Pixabay service.

        Args:
            api_key: Pixabay API key
            cache_dir: Directory for caching images
        """
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/"

        # Cache settings
        self.cache_dir = cache_dir or Path("cache/pixabay")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "image_cache.json"
        self.cache = self._load_cache()

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 10 requests per second max

        # Track used images to avoid duplicates
        self.used_images: Set[int] = set()

        # Performance tracking
        self.api_calls_made = 0
        self.cache_hits = 0

    def _load_cache(self) -> Dict:
        """Load cached images from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self) -> None:
        """Save cache to file."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Ignore cache save errors

    def _rate_limit(self) -> None:
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time = time.time()

    def _get_search_terms_for_category(self, category_name: str) -> List[str]:
        """Get relevant search terms for a category."""
        # Direct match
        if category_name in self.CATEGORY_SEARCH_TERMS:
            return self.CATEGORY_SEARCH_TERMS[category_name].copy()

        # Fuzzy match - check if category contains any known terms
        category_lower = category_name.lower()
        matching_terms = []

        for cat, terms in self.CATEGORY_SEARCH_TERMS.items():
            if any(word in category_lower for word in cat.lower().split()):
                matching_terms.extend(terms)

        # If no specific match, use generic terms
        if not matching_terms:
            matching_terms = self.GENERIC_TOOL_TERMS.copy()

        return list(set(matching_terms))  # Remove duplicates

    def _make_api_request(
        self, search_term: str, per_page: int = 20
    ) -> Optional[List[Dict]]:
        """Make a request to Pixabay API with enhanced error handling."""
        if not self.api_key:
            return None

        self._rate_limit()

        params = {
            "key": self.api_key,
            "q": search_term,
            "image_type": "photo",
            "orientation": "all",
            "category": "objects",
            "min_width": 640,
            "min_height": 480,
            "safesearch": "true",
            "per_page": per_page,
            "order": "popular",
        }

        try:
            url = f"{self.base_url}?{urlencode(params)}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            self.api_calls_made += 1
            data = response.json()

            hits = data.get("hits", [])
            total = data.get("total", 0)

            if hits:
                print(
                    f"📸 Pixabay API: Found {len(hits)} images for '{search_term}' (total: {total})"
                )
            else:
                print(f"🔍 Pixabay API: No images found for '{search_term}'")

            return hits

        except requests.exceptions.Timeout:
            print(
                f"⏰ Pixabay API timeout for '{search_term}' - continuing with fallback"
            )
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"🚫 Pixabay API rate limit exceeded - continuing with fallback")
            elif response.status_code == 400:
                print(
                    f"❌ Pixabay API bad request for '{search_term}' - continuing with fallback"
                )
            else:
                print(
                    f"🌐 Pixabay API HTTP error {response.status_code} for '{search_term}' - continuing with fallback"
                )
            return None
        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Pixabay API error for '{search_term}': {e}")
            return None

    def _parse_pixabay_response(self, hit: Dict) -> PixabayImage:
        """Parse a Pixabay API response hit into PixabayImage object."""
        return PixabayImage(
            id=hit["id"],
            web_format_url=hit["webformatURL"],
            large_image_url=hit["largeImageURL"],
            preview_url=hit["previewURL"],
            tags=hit["tags"],
            user=hit["user"],
            user_id=hit["user_id"],
            views=hit["views"],
            downloads=hit["downloads"],
            favorites=hit.get("likes", 0),  # Use 'likes' instead of 'favorites'
            page_url=hit["pageURL"],
        )

    def get_image_for_category(
        self, category_name: str, product_name: Optional[str] = None
    ) -> Optional[PixabayImage]:
        """
        Get a relevant image for a product category with improved cache management.

        Args:
            category_name: The product category name
            product_name: Optional product name for more specific search

        Returns:
            PixabayImage object or None if no image found
        """
        # Create multiple cache keys to increase cache hit ratio
        search_terms = self._get_search_terms_for_category(category_name)

        # Check cache for all possible search terms for this category
        for search_term in search_terms:
            cache_key = f"{search_term}:images"

            if cache_key in self.cache:
                cached_images = self.cache[cache_key]
                # Filter out already used images
                available_images = [
                    img for img in cached_images if img["id"] not in self.used_images
                ]
                if available_images:
                    self.cache_hits += 1
                    selected = random.choice(available_images)
                    self.used_images.add(selected["id"])
                    print(f"💾 Using cached image for '{category_name}' (cache hit)")
                    return PixabayImage(**selected)

        # If no cached images available, try to fetch new ones
        print(f"🔄 Cache exhausted for '{category_name}', fetching new images...")

        # If no API key, return None (will use fallback)
        if not self.api_key:
            print(f"🔑 No API key provided, using fallback for '{category_name}'")
            return None

        # If we have a specific product name, try that first
        if product_name:
            # Extract meaningful words from product name
            product_words = [
                word.lower()
                for word in product_name.split()
                if len(word) > 2 and word.lower() not in ["the", "and", "for", "with"]
            ]
            search_terms = product_words + search_terms

        # Try each search term until we find images
        for search_term in search_terms[:5]:  # Limit to avoid too many API calls
            cache_key = f"{search_term}:images"

            # Skip if we already tried this search term recently
            if cache_key in self.cache:
                continue

            images = self._make_api_request(search_term)
            if images:
                # Parse and cache the results
                parsed_images = []
                for hit in images:
                    try:
                        parsed_image = self._parse_pixabay_response(hit)
                        # Skip if this image ID is already used
                        if parsed_image.id in self.used_images:
                            continue

                        parsed_images.append(
                            {
                                "id": parsed_image.id,
                                "web_format_url": parsed_image.web_format_url,
                                "large_image_url": parsed_image.large_image_url,
                                "preview_url": parsed_image.preview_url,
                                "tags": parsed_image.tags,
                                "user": parsed_image.user,
                                "user_id": parsed_image.user_id,
                                "views": parsed_image.views,
                                "downloads": parsed_image.downloads,
                                "favorites": parsed_image.favorites,
                                "page_url": parsed_image.page_url,
                            }
                        )
                    except (KeyError, TypeError) as e:
                        print(f"⚠️ Error parsing Pixabay image: {e}")
                        continue

                if parsed_images:
                    # Cache the results with search term as key
                    self.cache[cache_key] = parsed_images
                    self._save_cache()

                    # Return a random image from results
                    selected = random.choice(parsed_images)
                    self.used_images.add(selected["id"])
                    return PixabayImage(**selected)

        return None

    def generate_fallback_image_data(
        self, category_name: str, product_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate realistic fallback image data when API is unavailable.

        Args:
            category_name: Product category name
            product_name: Optional product name

        Returns:
            Dictionary with image metadata
        """
        # Use existing providers for realistic fallback
        from .providers import ECommerceProvider
        from faker import Faker

        fake = Faker()
        fake.add_provider(ECommerceProvider)

        # Generate consistent filename based on category/product
        base_name = (
            (product_name or category_name).lower().replace(" ", "_").replace("-", "_")
        )
        base_name = "".join(c for c in base_name if c.isalnum() or c == "_")

        photographer = fake.photographer_name()

        # Generate realistic image metadata
        return {
            "id": fake.random_int(100000, 999999),
            "web_format_url": f"https://images.pixabay.com/photos/{fake.random_int(100000, 999999)}/{base_name}_640.jpg",
            "large_image_url": f"https://images.pixabay.com/photos/{fake.random_int(100000, 999999)}/{base_name}_1920.jpg",
            "preview_url": f"https://images.pixabay.com/photos/{fake.random_int(100000, 999999)}/{base_name}_150.jpg",
            "tags": f"{category_name.lower()}, tools, hardware, professional",
            "user": photographer.replace(" ", "").lower(),
            "user_id": fake.random_int(1000, 99999),
            "views": fake.random_int(100, 10000),
            "downloads": fake.random_int(10, 1000),
            "favorites": fake.random_int(5, 500),
            "page_url": f"https://pixabay.com/photos/{base_name}-{fake.random_int(100000, 999999)}/",
        }

    def get_performance_stats(self) -> Dict[str, int]:
        """Get performance statistics."""
        return {
            "api_calls_made": self.api_calls_made,
            "cache_hits": self.cache_hits,
            "total_requests": self.api_calls_made + self.cache_hits,
            "cache_hit_ratio": round(
                self.cache_hits / max(1, self.api_calls_made + self.cache_hits) * 100, 1
            ),
        }

    def clear_cache(self) -> None:
        """Clear the image cache."""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
        print("🗑️ Pixabay image cache cleared")

    def prefetch_category_images(
        self, categories: List[str], images_per_category: int = 40
    ) -> None:
        """
        Prefetch images for all categories to improve cache hit ratio.

        Args:
            categories: List of category names to prefetch
            images_per_category: Number of images to fetch per category
        """
        if not self.api_key:
            print("🔑 No API key provided, skipping prefetch")
            return

        print(f"🚀 Prefetching images for {len(categories)} categories...")

        for category in categories:
            search_terms = self._get_search_terms_for_category(category)

            for search_term in search_terms[
                :2
            ]:  # Fetch for top 2 search terms per category
                cache_key = f"{search_term}:images"

                # Skip if already cached
                if cache_key in self.cache and len(self.cache[cache_key]) >= 10:
                    continue

                print(f"  📥 Prefetching '{search_term}'...")
                images = self._make_api_request(
                    search_term, per_page=images_per_category
                )

                if images:
                    parsed_images = []
                    for hit in images:
                        try:
                            parsed_image = self._parse_pixabay_response(hit)
                            parsed_images.append(
                                {
                                    "id": parsed_image.id,
                                    "web_format_url": parsed_image.web_format_url,
                                    "large_image_url": parsed_image.large_image_url,
                                    "preview_url": parsed_image.preview_url,
                                    "tags": parsed_image.tags,
                                    "user": parsed_image.user,
                                    "user_id": parsed_image.user_id,
                                    "views": parsed_image.views,
                                    "downloads": parsed_image.downloads,
                                    "favorites": parsed_image.favorites,
                                    "page_url": parsed_image.page_url,
                                }
                            )
                        except (KeyError, TypeError) as e:
                            print(f"⚠️ Error parsing prefetch image: {e}")
                            continue

                    if parsed_images:
                        self.cache[cache_key] = parsed_images
                        print(
                            f"  ✅ Cached {len(parsed_images)} images for '{search_term}'"
                        )

                # Rate limiting between requests
                time.sleep(0.2)

        # Save cache after prefetching
        self._save_cache()
        print(
            f"💾 Prefetch complete. Cache now contains {len(self.cache)} search term groups"
        )


def create_pixabay_service(
    api_key: Optional[str] = None, cache_dir: Optional[Path] = None
) -> PixabayImageService:
    """
    Factory function to create PixabayImageService.

    Args:
        api_key: Pixabay API key
        cache_dir: Cache directory path

    Returns:
        Configured PixabayImageService instance
    """
    return PixabayImageService(api_key=api_key, cache_dir=cache_dir)


if __name__ == "__main__":
    # Test the service
    import os

    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        print("Please set PIXABAY_API_KEY environment variable for testing")
        exit(1)

    service = create_pixabay_service(api_key)

    # Test with different categories
    test_categories = ["Hand Tools", "Power Tools", "Safety Equipment"]

    for category in test_categories:
        print(f"\n🔍 Testing category: {category}")
        image = service.get_image_for_category(category)

        if image:
            print(f"✅ Found image: {image.tags}")
            print(f"   User: {image.user}")
            print(f"   Views: {image.views}")
        else:
            print("❌ No image found")

    # Show performance stats
    stats = service.get_performance_stats()
    print(f"\n📊 Performance Stats:")
    print(f"   API calls: {stats['api_calls_made']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Cache hit ratio: {stats['cache_hit_ratio']}%")
