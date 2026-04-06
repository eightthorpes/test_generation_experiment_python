"""
Sprint 1 - Category Page Tests
TC-S1-007: Category page displays products for the selected category
TC-S1-008: Category name is shown as the page title
TC-S1-009: Only category-specific products are shown
"""

from playwright.sync_api import Page, expect
from conftest import BASE_URL


def test_tc_s1_007_category_page_displays_products(page: Page):
    """TC-S1-007: Clicking a category nav link displays products for that category."""
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='nav-hand-tools']").click()
    page.wait_for_load_state("networkidle")

    product_links = page.locator("[data-test^='product-']")
    expect(product_links.first).to_be_visible()
    assert (
        product_links.count() > 0
    ), "Expected products to be displayed on the category page"


def test_tc_s1_008_category_name_shown_as_page_title(page: Page):
    """TC-S1-008: The category name is shown as the page title on the category page."""
    page.goto(f"{BASE_URL}/#/category/hand-tools")
    page.wait_for_load_state("networkidle")

    title = page.locator("[data-test='page-title']")
    expect(title).to_be_visible()
    expect(title).to_contain_text("Hand Tools")


def test_tc_s1_009_only_category_specific_products_are_shown(page: Page):
    """TC-S1-009: The category page only shows products belonging to that category.

    Verified by collecting product names from each category and confirming the
    Hand Tools and Power Tools sets are disjoint — each category has its own products.

    Angular re-renders the product list asynchronously after a hash-route change.
    The page-title updates before the product list does, so after navigating we
    wait for a known product from the *previous* category to disappear before
    reading the new list — confirming the DOM has fully switched.
    """
    page.goto(f"{BASE_URL}/#/category/hand-tools")
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='page-title']")).to_contain_text("Hand Tools")
    hand_tools_names = set(page.locator("[data-test='product-name']").all_inner_texts())
    assert len(hand_tools_names) > 0, "Hand Tools category should have products"

    # Pick one known hand-tools product to use as a staleness marker
    stale_product = next(iter(hand_tools_names))

    page.goto(f"{BASE_URL}/#/category/power-tools")
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='page-title']")).to_contain_text("Power Tools")
    # Wait until the stale hand-tools product is no longer in the product list
    expect(
        page.locator("[data-test='product-name']").filter(has_text=stale_product)
    ).to_have_count(0)
    power_tools_names = set(
        page.locator("[data-test='product-name']").all_inner_texts()
    )
    assert len(power_tools_names) > 0, "Power Tools category should have products"

    # The two categories should not share any products
    overlap = hand_tools_names & power_tools_names
    assert overlap == set(), (
        f"Category pages should show only their own products, "
        f"but found overlap: {overlap}"
    )

    # Each category should be a strict subset of all products on the home page
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    all_names = set(page.locator("[data-test='product-name']").all_inner_texts())

    assert hand_tools_names.issubset(
        all_names
    ), "Hand Tools products should exist in the full catalog"
    assert power_tools_names.issubset(
        all_names
    ), "Power Tools products should exist in the full catalog"
    assert (
        hand_tools_names != all_names
    ), "Category page should show fewer products than the full catalog"
