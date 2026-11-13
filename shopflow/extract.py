"""Extract cart records from the DummyJSON REST API."""
import logging
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOG = logging.getLogger(__name__)


def build_session(retries=3):
    session = Session()
    retry = Retry(total=retries, connect=retries, read=retries, status=retries,
                  backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=frozenset(["GET"]), respect_retry_after_header=True)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


def extract_carts(base_url, page_size=20, timeout=20, retries=3, session=None):
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    client = session or build_session(retries)
    carts = []
    skip = 0
    while True:
        response = client.get(base_url, params={"limit": page_size, "skip": skip}, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("carts"), list):
            raise ValueError("Unexpected API response: expected a carts list")
        batch = payload["carts"]
        carts.extend(batch)
        LOG.info("Fetched %s carts (offset %s)", len(batch), skip)
        skip += len(batch)
        total = payload.get("total")
        if not batch or (isinstance(total, int) and skip >= total) or len(batch) < page_size:
            break
    return carts
