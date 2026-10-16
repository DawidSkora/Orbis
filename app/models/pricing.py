from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Document stored in public.pricing.data — camelCase, same shape the website renders.

Text = Field(min_length=1, max_length=300)


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @field_validator("*", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class PriceItem(_Strict):
    name: str = Text
    description: str = Field(default="", max_length=500)
    price: str = Field(min_length=1, max_length=60)
    examples: Optional[str] = Field(default=None, max_length=300)

    @field_validator("examples")
    @classmethod
    def _empty_examples_to_none(cls, v):
        return v or None


class PriceCategory(_Strict):
    id: str = Field(min_length=1, max_length=40, pattern=r"^[a-z0-9-]+$")
    title: str = Text
    subtitle: str = Field(default="", max_length=100)
    items: list[PriceItem] = Field(max_length=50)


class AddonItem(_Strict):
    name: str = Text
    price: str = Field(min_length=1, max_length=60)


class PricingData(_Strict):
    categories: list[PriceCategory] = Field(min_length=1, max_length=20)
    additional_services: list[AddonItem] = Field(alias="additionalServices", max_length=50)
    solo_services: list[AddonItem] = Field(alias="soloServices", max_length=50)
    notes: list[str] = Field(max_length=30)

    @field_validator("notes")
    @classmethod
    def _notes_not_empty(cls, notes):
        cleaned = [n.strip() for n in notes]
        if any(not n for n in cleaned):
            raise ValueError("notes must not be empty")
        return cleaned

    @field_validator("categories")
    @classmethod
    def _unique_category_ids(cls, categories):
        ids = [c.id for c in categories]
        if len(ids) != len(set(ids)):
            raise ValueError("category ids must be unique")
        return categories

    def to_document(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class PricingUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    data: PricingData
    # Optimistic concurrency: updatedAt the editor started from. Mismatch → 409.
    expected_updated_at: Optional[str] = Field(default=None, alias="expectedUpdatedAt")
