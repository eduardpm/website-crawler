from typing import Annotated, ClassVar
from pydantic import AfterValidator, BaseModel, Field, field_validator

from common.products.product_brands import (
    KNOWN_GPU_BRANDS,
    KNOWN_GPU_MODELS,
    KNOWN_RAM_BRANDS,
)
from common.products.product_types import ProductTypes
from common.utils.data_extractors import extract_info, extract_info_known_sources
from common.utils.translator import get_translator


def translate_text(text: str) -> str:
    translation = get_translator().translate(text)
    if "MYMEMORY WARNING" in translation:
        # translation failed, return the original text
        return text
    return translation


class Product(BaseModel):
    """
    Base class for all products.
    """

    discount_percentage: float = Field(
        default=0.0, description="Discount percentage on the product"
    )
    link: str = Field(description="Link to the product page")
    title: Annotated[str, AfterValidator(translate_text)] = Field(
        description="Title of the product"
    )
    specs: Annotated[str, AfterValidator(translate_text)] = Field(
        default="", description="Specifications of the product"
    )
    previous_price: float = Field(description="Previous price of the product in euros")
    current_price: float = Field(description="Current price of the product in euros")
    rgb: bool | None = Field(
        default=None, description="Whether the product has RGB lighting"
    )

    def model_post_init(self, _):
        if self.previous_price < self.current_price:
            raise ValueError("Previous price must be greater than current price")
        self.discount_percentage = round(
            (self.previous_price - self.current_price) / self.previous_price * 100, 2
        )
        if self.discount_percentage <= 0:
            raise ValueError("Discount percentage must be a positive number")

    @field_validator("previous_price", "current_price")
    def check_price(cls, value):
        if value < 0:
            raise ValueError("Price must be a positive number")
        return value

    def __str__(self):
        product_descr = ""
        product_descr += f"Title: {self.title}\n"
        product_descr += f"Link: {self.link}\n"
        product_descr += f"Previous Price: {self.previous_price}\n"
        product_descr += f"Current Price: {self.current_price}\n"
        product_descr += f"Discount: {self.discount_percentage}%\n"
        product_descr += "-" * 40
        return product_descr


class RAM(Product):
    product_type: ClassVar[ProductTypes] = ProductTypes.RAM
    capacity: int | None = Field(default=None, description="RAM capacity in GB")
    speed: int | None = Field(default=None, description="RAM speed in MHz")
    type: str | None = Field(default=None, description="RAM type (e.g., DDR4, DDR5)")
    brand: str | None = Field(default=None, description="Brand of the RAM")

    def model_post_init(self, _):
        super().model_post_init(_)
        capacity_match = extract_info(self.specs, r"(\d+)\s*GB") or extract_info(
            self.title, r"(\d+)\s*GB"
        )
        if capacity_match:
            self.capacity = int(capacity_match.group(1))
        speed_match = extract_info(
            self.specs, r"DDR\d?[^0-9]*(\d+)(?:\s*MHz?)?"
        ) or extract_info(self.title, r"DDR\d?[^0-9]*(\d+)(?:\s*MHz?)?")
        if speed_match:
            self.speed = int(speed_match.group(1))
        type_match = extract_info(self.specs, r"DDR\d?") or extract_info(
            self.title, r"DDR\d?"
        )
        if type_match:
            self.type = type_match.group(0)
        brand_match = extract_info_known_sources(
            self.specs, KNOWN_RAM_BRANDS
        ) or extract_info_known_sources(self.title, KNOWN_RAM_BRANDS)
        if brand_match:
            self.brand = brand_match

    def __str__(self):
        product_descr = super().__str__()[:-40]  # get parent class string
        product_descr += "Specifications:\n"
        product_descr += f"\tCapacity: {self.capacity} GB\n"
        product_descr += f"\tSpeed: {self.speed} MHz\n"
        product_descr += f"\tType: {self.type}\n"
        product_descr += f"\tBrand: {self.brand}\n"
        product_descr += "-" * 40
        return product_descr


class VideoCard(Product):
    product_type: ClassVar[ProductTypes] = ProductTypes.VIDEO_CARD
    brand: str | None = Field(default=None, description="Brand of the video card")
    model: str | None = Field(default=None, description="Model of the video card")
    memory: int | None = Field(default=None, description="Memory size in GB")
    type: str | None = Field(
        default=None, description="Type of the video card (e.g., GDDR6, GDDR5)"
    )
    core_clock: float | None = Field(
        default=None, description="Core clock speed in MHz"
    )

    def model_post_init(self, _):
        super().model_post_init(_)
        brand_match = extract_info_known_sources(
            self.specs, KNOWN_GPU_BRANDS
        ) or extract_info_known_sources(self.title, KNOWN_GPU_BRANDS)
        if brand_match:
            self.brand = brand_match
        model_match = extract_info_known_sources(
            self.specs, KNOWN_GPU_MODELS
        ) or extract_info_known_sources(self.title, KNOWN_GPU_MODELS)
        if model_match:
            self.model = model_match
        memory_match = extract_info(self.specs, r"(\d+)\s*GB") or extract_info(
            self.title, r"(\d+)\s*GB"
        )
        if memory_match:
            self.memory = int(memory_match.group(1))
        type_match = extract_info(self.specs, r"GDDR\d?") or extract_info(
            self.title, r"GDDR\d?"
        )
        if type_match:
            self.type = type_match.group(0)
        core_clock_match = extract_info(self.specs, r"(\d+)\s*MHz") or extract_info(
            self.title, r"(\d+)\s*MHz"
        )
        if core_clock_match:
            self.core_clock = float(core_clock_match.group(1))

    def __str__(self):
        product_descr = super().__str__()[:-40]
        # get parent class string
        product_descr += "Specifications:\n"
        product_descr += f"\tBrand: {self.brand}\n"
        product_descr += f"\tModel: {self.model}\n"
        product_descr += f"\tMemory: {self.memory} GB\n"
        product_descr += f"\tType: {self.type}\n"
        product_descr += f"\tCore Clock: {self.core_clock} MHz\n"
        product_descr += "-" * 40
        return product_descr


PRODUCT_TYPE_TO_CLASS_MAP = None


def get_product_type_to_class_map() -> dict[str, type[Product]]:
    """
    Returns a mapping of product types to their corresponding classes.
    """
    global PRODUCT_TYPE_TO_CLASS_MAP
    if PRODUCT_TYPE_TO_CLASS_MAP is None:
        PRODUCT_TYPE_TO_CLASS_MAP = {
            product_cls.product_type: product_cls
            for product_cls in Product.__subclasses__()
        }
    return PRODUCT_TYPE_TO_CLASS_MAP
