from typing import Annotated
from pydantic import AfterValidator, BaseModel, Field, field_validator

from libs.utils.translator import get_translator


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.discount_percentage = round(
            (self.previous_price - self.current_price) / self.previous_price * 100, 2
        )

    def __post_init__(self):
        if self.previous_price < self.current_price:
            raise ValueError("Previous price must be greater than current price")
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
    capacity: int = Field(..., description="RAM capacity in GB")
    speed: int = Field(..., description="RAM speed in MHz")
    type: str = Field(..., description="RAM type (e.g., DDR4, DDR5)")
    brand: str = Field(..., description="Brand of the RAM")


class VideoCard(Product):
    brand: str = Field(..., description="Brand of the video card")
    model: str = Field(..., description="Model of the video card")
    memory: int = Field(..., description="Memory size in GB")
    core_clock: float = Field(..., description="Core clock speed in MHz")
    memory_clock: float = Field(..., description="Memory clock speed in MHz")
