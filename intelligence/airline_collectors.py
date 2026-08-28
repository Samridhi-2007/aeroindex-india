import re
from datetime import date, datetime, timezone
from itertools import count
from typing import Any

from .models import RawFareObservation


class BrowserFareCollector:
    """Base Playwright collector. Airline subclasses provide page-specific form hooks."""

    source_id = ""
    carrier = ""
    booking_url = ""

    def __init__(self, origin: str, destination: str, travel_date: str, period: str, booking_window_days: int, fare_selector: str, headless: bool = True) -> None:
        validate_collection_date(travel_date)
        self.origin = origin.upper()
        self.destination = destination.upper()
        self.travel_date = travel_date
        self.period = period
        self.booking_window_days = booking_window_days
        self.fare_selector = fare_selector
        self.headless = headless

    def collect(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as error:
            raise RuntimeError("Install Playwright with 'pip install playwright' and 'playwright install chromium'") from error

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            try:
                response = page.goto(self.booking_url, wait_until="domcontentloaded", timeout=60000)
                if response and response.status in (403, 429):
                    raise RuntimeError(f"{self.source_id} returned HTTP {response.status}; collection stopped")
                self.search(page)
                try:
                    page.wait_for_selector(self.fare_selector, timeout=60000)
                except Exception as error:
                    if error.__class__.__name__ == "TargetClosedError":
                        raise RuntimeError(f"{self.source_id} browser page was closed before fare extraction; keep the browser open after verification") from error
                    body_text = page.locator("body").inner_text().lower()
                    if any(term in body_text for term in ("captcha", "verify you are human", "are you a person or a robot", "access denied")):
                        if self.headless:
                            raise RuntimeError(f"{self.source_id} blocked automated collection; no CAPTCHA was bypassed") from error
                        input(f"Complete the {self.source_id} verification in the browser, then press Enter here to continue...")
                        try:
                            page.wait_for_selector(self.fare_selector, timeout=120000)
                        except Exception as retry_error:
                            if retry_error.__class__.__name__ == "TargetClosedError":
                                raise RuntimeError(f"{self.source_id} browser page was closed before fare extraction; keep the browser open after verification") from retry_error
                            raise RuntimeError(f"{self.source_id} verification did not lead to visible fare results") from retry_error
                    else:
                        raise RuntimeError(f"No fare elements found for {self.source_id}; verify the selector or page response") from error
                body_text = page.locator("body").inner_text().lower()
                if any(term in body_text for term in ("captcha", "verify you are human", "access denied")):
                    raise RuntimeError(f"{self.carrier} blocked automated collection; no CAPTCHA was bypassed")
                fares = self.read_fares(page)
                observation_ids = count(1)
                collection_timestamp = datetime.now(timezone.utc).isoformat()
                for raw_fare, fare in fares:
                    yield RawFareObservation(
                        observation_id=f"{self.source_id}-{self.period}-{self.travel_date}-{self.origin}-{self.destination}-{next(observation_ids)}",
                        period=self.period,
                        route=f"{self.origin}-{self.destination}",
                        origin=self.origin,
                        destination=self.destination,
                        booking_window_days=self.booking_window_days,
                        raw_fare=raw_fare,
                        source_id=self.source_id,
                        carrier=self.carrier,
                        fare_class="ECONOMY",
                        observation_date=self.travel_date,
                        collection_timestamp=collection_timestamp,
                        extraction_status="extracted" if fare is not None else "invalid_fare",
                        source_url=self.booking_url,
                    )
            finally:
                browser.close()

    def search(self, page: Any) -> None:
        raise NotImplementedError

    def read_fares(self, page: Any) -> list[tuple[str, float | None]]:
        values: list[tuple[str, float | None]] = []
        for text in page.locator(self.fare_selector).all_inner_texts():
            match = re.search(r"(?:INR|Rs\.?|₹|\u20b9)?\s*([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
            if match:
                val_str = match.group(1).replace(",", "")
                try:
                    val = float(val_str)
                    if val > 0:
                        values.append((text.strip(), val))
                except ValueError:
                    pass
        return values

    def select_airport(self, page: Any, field_name: str, airport: str) -> None:
        page.get_by_role("button", name=re.compile(field_name, re.IGNORECASE)).click()
        search = page.get_by_placeholder(re.compile("search city or airport", re.IGNORECASE))
        search.fill(airport)
        page.get_by_text(re.compile(rf"\b{airport}\b", re.IGNORECASE)).last.click()


class AirIndiaCollector(BrowserFareCollector):
    source_id = "airindia"
    carrier = "Air India"
    booking_url = "https://www.airindia.com/in/en/book/search-flights.html"

    def search(self, page: Any) -> None:
        self.select_airport(page, "FROM", self.origin)
        self.select_airport(page, "TO", self.destination)
        page.get_by_role("button", name=re.compile("Depart", re.IGNORECASE)).click()
        page.get_by_text(self.travel_date, exact=True).click()
        page.get_by_role("button", name=re.compile("Search", re.IGNORECASE)).last.click()
        page.wait_for_load_state("networkidle", timeout=60000)


class IndigoCollector(BrowserFareCollector):
    source_id = "indigo"
    carrier = "IndiGo"
    booking_url = "https://www.goindigo.in/"

    def search(self, page: Any) -> None:
        fields = page.get_by_placeholder("Start typing..")
        fields.nth(0).fill(self.origin)
        page.get_by_text(re.compile(rf"\b{self.origin}\b", re.IGNORECASE)).last.click()
        fields.nth(1).fill(self.destination)
        page.get_by_text(re.compile(rf"\b{self.destination}\b", re.IGNORECASE)).last.click()
        page.get_by_role("button", name=re.compile("Search", re.IGNORECASE)).first.click()
        page.wait_for_load_state("networkidle", timeout=60000)


class SkyscannerCollector(BrowserFareCollector):
    """Collect visible fares from a permitted public Skyscanner results page."""

    source_id = "skyscanner"
    carrier = None

    def __init__(self, origin: str, destination: str, travel_date: str, period: str, booking_window_days: int, fare_selector: str = '[data-backpack-ds-component="Text"]', headless: bool = True, market: str = "IN", currency: str = "INR") -> None:
        super().__init__(origin, destination, travel_date, period, booking_window_days, fare_selector, headless)
        self.market = market
        self.currency = currency
        self.booking_url = f"https://www.skyscanner.co.in/transport/flights/{self.origin.lower()}/{self.destination.lower()}/{self.travel_date.replace('-', '')}/?adultsv2=1&cabinclass=economy&currency={currency}&market={market}&rtn=0"

    def search(self, page: Any) -> None:
        return None


class EaseMyTripCollector(BrowserFareCollector):
    """Collect visible fares from a permitted EaseMyTrip listing page."""

    source_id = "easemytrip"
    carrier = None
    fare_selector = ".value"
    airport_slugs = {"DEL": "Delhi-India", "BOM": "Mumbai-India", "BLR": "Bangalore-India", "HYD": "Hyderabad-India", "MAA": "Chennai-India", "CCU": "Kolkata-India"}

    def __init__(self, origin: str, destination: str, travel_date: str, period: str, booking_window_days: int, fare_selector: str = ".value", headless: bool = True, currency: str = "INR") -> None:
        super().__init__(origin, destination, travel_date, period, booking_window_days, fare_selector, headless)
        self.currency = currency
        day = date.fromisoformat(travel_date).strftime("%d/%m/%Y")
        origin_slug = self.airport_slugs.get(self.origin, self.origin)
        destination_slug = self.airport_slugs.get(self.destination, self.destination)
        self.booking_url = f"https://www.easemytrip.com/flight-search/listing?srch={self.origin}-{origin_slug}|{self.destination}-{destination_slug}|{day}&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=en-us&IsDoubleSeat=false&CCODE=IN&curr={currency}&apptype=B2C"

    def search(self, page: Any) -> None:
        page.wait_for_selector(self.fare_selector, timeout=60000)
        try:
            page.wait_for_function("() => Array.from(document.querySelectorAll('.value')).some(el => el.innerText.trim().length > 0)", timeout=30000)
        except Exception:
            pass


def validate_collection_date(value: str) -> str:
    """Validate the ISO date passed to a collector before opening a browser."""
    date.fromisoformat(value)
    return value