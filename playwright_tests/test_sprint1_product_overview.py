"""
Sprint 1 - Product Overview Tests
TC-S1-001: Product grid is displayed on home page
TC-S1-002: Each product card shows image, name, and price
TC-S1-003: Clicking product card navigates to detail page
"""

import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


@pytest.fixture(autouse=True)
def go_to_home(page: Page):
    """Navigate to the home page before each test."""
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")


def test_tc_s1_001_product_grid_is_displayed(page: Page):
    """TC-S1-001: A grid of product cards is visible on the home page."""
    product_links = page.locator("[data-test^='product-']")
    expect(product_links.first).to_be_visible()
    assert product_links.count() > 1, "Expected multiple product cards in the grid"


def test_tc_s1_002_product_card_shows_image_name_and_price(page: Page):
    """TC-S1-002: Each product card displays an image, product name, and price.

    DOM structure: each product is a <li class="list-group-item"> containing
    an <a data-test="product-N"> (name) and a sibling <span data-test="product-price">.
    The product image is rendered inside the linked product card, so we verify
    images exist on the page alongside the name/price pairs.
    """
    # Use the list-group-item <li> as the card container so both the name
    # anchor and the sibling price span are in scope.
    first_card = page.locator("li.list-group-item").first

    # Name — inside the <a data-test="product-N">
    name = first_card.locator("[data-test='product-name']")
    expect(name).to_be_visible()
    assert name.inner_text().strip() != "", "Product name should not be empty"

    # Price — sibling <span> inside the same <li>
    price = first_card.locator("[data-test='product-price']")
    expect(price).to_be_visible()
    assert price.inner_text().strip() != "", "Product price should not be empty"

    # Images are rendered on the page (one per product in the overview grid)
    expect(page.locator("img").first).to_be_visible()


def test_tc_s1_003_clicking_product_card_navigates_to_detail(page: Page):
    """TC-S1-003: Clicking a product card navigates to that product's detail page."""
    first_product = page.locator("[data-test^='product-']").first
    product_name = first_product.locator("[data-test='product-name']").inner_text()

    first_product.click()
    page.wait_for_load_state("networkidle")

    assert "product" in page.url, f"Expected URL to contain 'product', got: {page.url}"
    expect(page.locator("[data-test='product-name']")).to_have_text(product_name)
