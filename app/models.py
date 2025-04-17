from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Annotated, Optional


class Swift_Code(BaseModel):
    address: Annotated[
        Optional[str],
        Field(
            default=None,
            max_length=200,
            description="Address must be at most 200 characters long",
        ),
    ]
    bankName: Annotated[
        Optional[str],
        Field(
            default=None,
            max_length=200,
            description="Bank name must be at most 200 characters long",
        ),
    ]
    countryISO2: str = Field(
        min_length=2,
        max_length=2,
        pattern=r"^[a-zA-Z]{2}$",
        description="countryISO2 is 2 letter long string",
    )
    countryName: Annotated[
        Optional[str],
        Field(
            default=None,
            max_length=200,
            description="Country name must be at most 200 characters long",
        ),
    ]
    isHeadquarter: bool
    swiftCode: Annotated[
        str,
        Field(
            min_length=11,
            max_length=11,
            description="SWIFT code must be exactly 11 characters",
        ),
    ]

    # Valitations
    @field_validator(
        "countryISO2", "countryName", "swiftCode"
    )  # Added swiftCode to cover usecase when user tries to get/del swiftCode small latters
    @classmethod
    def to_uppercase(cls, v: str):
        if v is None:
            return
        return v.upper()

    @field_validator("countryISO2")
    @classmethod
    def validate_iso(cls, v: str):
        if not v.isalpha():
            raise ValueError(
                "countryISO2 must contain only alphabetic characters (e.g., PL, CH)"
            )
        return v.upper()

    model_config = ConfigDict(from_attributes=True)


class Switf_Branch(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str

    model_config = ConfigDict(from_attributes=True)


class Swift_with_Branches(Swift_Code):
    branches: list[Switf_Branch]

    model_config = ConfigDict(from_attributes=True)


class Swift_on_country(BaseModel):
    countryISO2: str
    countryName: str

    model_config = ConfigDict(from_attributes=True)


class Swift_with_Branches_country(Swift_on_country):
    swiftCodes: list[Switf_Branch]

    model_config = ConfigDict(from_attributes=True)
