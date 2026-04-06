"""
Sprint 1 - Product Detail Tests
TC-S1-004: Product detail page displays all required information
TC-S1-005: Related products section is shown
TC-S1-006: Clicking related product navigates to its detail page
"""

import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


@pytest.fixture(autouse=True)
def go_to_product_detail(page: Page):
    page.goto(f"{BASE_URL}/#/product/1")
    page.wait_for_load_state("networkidle")


def test_tc_s1_004_product_detail_shows_all_required_info(page: Page):
    """TC-S1-004: Product detail page shows image, name, description, price,
    category badge, and brand badge."""
    # Product name (H1)
    expect(page.locator("[data-test='product-name']")).to_be_visible()
    assert page.locator("[data-test='product-name']").inner_text().strip() != ""

    # Unit price
    expect(page.locator("[data-test='unit-price']")).to_be_visible()
    assert page.locator("[data-test='unit-price']").inner_text().strip() != ""

    # Description
    expect(page.locator("[data-test='product-description']")).to_be_visible()
    assert page.locator("[data-test='product-description']").inner_text().strip() != ""

    # Product image
    expect(page.locator("figure img.figure-img")).to_be_visible()

    # Category and brand badges (there should be at least 2)
    badges = page.locator("span.badge")
    assert badges.count() >= 2, "Expected at least a category badge and a brand badge"
    expect(badges.first).to_be_visible()


def test_tc_s1_005_related_products_section_is_shown(page: Page):
    """TC-S1-005: A 'Related products' section is visible below the main product info."""
    related_heading = page.locator("h1", has_text="Related products")
    expect(related_heading).to_be_visible()

    # Verify there are related product cards
    related_cards = page.locator(
        "h1:has-text('Related products') ~ div .card, "
        "h1:has-text('Related products') + div .card"
    )
    assert related_cards.count() > 0, "Expected related product cards to be present"


def test_tc_s1_006_clicking_related_product_navigates_to_its_detail(page: Page):
    """TC-S1-006: Clicking a related product navigates to that product's detail page."""
    original_url = page.url

    # Find and click the first related product card (a.card links under Related products)
    related_product = page.locator(
        "h1:has-text('Related products') ~ div a.card"
    ).first
    expect(related_product).to_be_visible()

    # Get where it links to before clicking
    href = related_product.get_attribute("href")
    assert href and "product" in href, "Related product link should point to a product page"

    related_product.click()
    page.wait_for_load_state("networkidle")

    assert page.url != original_url, "URL should have changed after clicking related product"
    assert "product" in page.url
    expect(page.locator("[data-test='product-name']")).to_be_visible()
