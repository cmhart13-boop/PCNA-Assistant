"""PCNA PromoStandards SOAP client.

Credentials are read by app.py from Streamlit secrets and are never stored here.
Endpoints default to the PCNA staging endpoints documented in the PCNA catalog road map,
but can be overridden in Streamlit secrets for production.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from zeep import Client, Settings
from zeep.helpers import serialize_object
from zeep.transports import Transport
import requests


DEFAULT_ENDPOINTS = {
    "product_sellable": "https://psproductdata200-stg.pcna.online",
    "product_data": "https://psproductdata100-stg.pcna.online",
    "pricing": "https://pspriceconfig100-stg.pcna.online",
    "media": "https://psmediacontent110-stg.pcna.online",
    "inventory": "https://psinventory200-stg.pcna.online",
}


class PCNAAPIError(RuntimeError):
    pass


def _plain(value: Any) -> Any:
    return serialize_object(value, target_cls=dict)


def _wsdl_url(endpoint: str) -> str:
    endpoint = endpoint.rstrip("/")
    return f"{endpoint}/?singleWsdl"


@dataclass
class PCNAClient:
    access_id: str
    password: str
    endpoints: dict[str, str] | None = None
    timeout: int = 30

    def __post_init__(self) -> None:
        if not self.access_id or not self.password:
            raise PCNAAPIError("PCNA PromoStandards production access ID/password are missing.")
        self.endpoints = {**DEFAULT_ENDPOINTS, **(self.endpoints or {})}
        session = requests.Session()
        session.headers.update({"User-Agent": "PCNA-Assistant/1.0"})
        self._transport = Transport(session=session, timeout=self.timeout, operation_timeout=self.timeout)
        self._settings = Settings(strict=False, xml_huge_tree=True)
        self._clients: dict[str, Client] = {}

    def _client(self, service: str) -> Client:
        if service not in self._clients:
            try:
                self._clients[service] = Client(
                    _wsdl_url(self.endpoints[service]),
                    transport=self._transport,
                    settings=self._settings,
                )
            except Exception as exc:
                raise PCNAAPIError(f"Could not open PCNA {service} service: {exc}") from exc
        return self._clients[service]

    def _call(self, service: str, operation: str, **kwargs: Any) -> Any:
        try:
            fn = getattr(self._client(service).service, operation)
            return _plain(fn(**kwargs))
        except Exception as exc:
            raise PCNAAPIError(f"PCNA {operation} failed: {exc}") from exc

    def get_product_sellable(self) -> Any:
        return self._call(
            "product_sellable",
            "GetProductSellable",
            wsVersion="2.0.0",
            id=self.access_id,
            password=self.password,
            localizationCountry="US",
            localizationLanguage="en",
            isSellable=True,
        )

    def get_product(self, product_id: str) -> Any:
        return self._call(
            "product_data",
            "GetProduct",
            wsVersion="2.0.0",
            id=self.access_id,
            password=self.password,
            localizationCountry="US",
            localizationLanguage="en",
            productId=product_id,
        )

    def get_inventory(self, product_id: str) -> Any:
        return self._call(
            "inventory",
            "GetInventoryLevels",
            wsVersion="2.0.0",
            id=self.access_id,
            password=self.password,
            productId=product_id,
        )

    def get_fob_points(self, product_id: str) -> Any:
        return self._call(
            "pricing",
            "GetFobPoints",
            wsVersion="1.0.0",
            id=self.access_id,
            password=self.password,
            productId=product_id,
            localizationCountry="US",
            localizationLanguage="en",
        )

    def get_configuration_and_pricing(
        self,
        product_id: str,
        fob_id: str | int,
        *,
        price_type: str = "List",
        configuration_type: str = "Decorated",
    ) -> Any:
        return self._call(
            "pricing",
            "GetConfigurationAndPricing",
            wsVersion="1.0.0",
            id=self.access_id,
            password=self.password,
            productId=product_id,
            currency="USD",
            fobId=fob_id,
            priceType=price_type,
            localizationCountry="US",
            localizationLanguage="en",
            configurationType=configuration_type,
        )

    def get_media(self, product_id: str, media_type: str = "Image") -> Any:
        return self._call(
            "media",
            "GetMediaContent",
            wsVersion="1.1.0",
            id=self.access_id,
            password=self.password,
            cultureName="en-US",
            mediaType=media_type,
            productId=product_id,
        )

    def get_product_bundle(self, product_id: str) -> dict[str, Any]:
        """Fetch the data the assistant needs to verify a PCNA item.

        Pricing/configuration requires a FOB ID, whose exact location in the SOAP response
        differs between implementations. We return FOB data separately so app code can
        display/use it and can call configuration once a FOB is selected.
        """
        result: dict[str, Any] = {"product_id": product_id}
        for key, fn in (
            ("product", self.get_product),
            ("inventory", self.get_inventory),
            ("fob_points", self.get_fob_points),
            ("media", self.get_media),
        ):
            try:
                result[key] = fn(product_id)
            except PCNAAPIError as exc:
                result[key] = {"error": str(exc)}
        return result
