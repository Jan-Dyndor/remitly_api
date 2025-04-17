from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.model_orm import SwiftCodeORM
from app.models import (
    Swift_Code,
    Swift_with_Branches,
    Swift_with_Branches_country,
    Switf_Branch,
)

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get(
    "/swift-codes/{swift_code}",
    response_model=Union[Swift_Code, Swift_with_Branches],
)
def get_swift_code(
    swift_code: Annotated[
        str,
        Path(
            min_length=11,
            max_length=11,
            description="SWIFT code must be exactly 11 characters",
        ),
    ],
    db: Session = Depends(get_db),
):
    swift_code = swift_code.upper()
    branches_data = []
    code = db.query(SwiftCodeORM).filter_by(swiftCode=swift_code).first()
    if not code:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    if code.isHeadquarter:
        branches = (
            db.query(SwiftCodeORM)
            .filter(
                SwiftCodeORM.swiftCode.startswith(code.swiftCode[:8]),
                SwiftCodeORM.isHeadquarter == False,
            )
            .all()
        )
        for branch in branches:
            branches_data.append(
                Switf_Branch.model_validate(branch, from_attributes=True)
            )

        base_hq = Swift_Code.model_validate(code, from_attributes=True)
        return Swift_with_Branches(**base_hq.model_dump(), branches=branches_data)

    else:
        return Swift_Code.model_validate(code)


@router.get("/swift-codes/country/{countryISO2code}")
def swift_codes_on_country(
    countryISO2code: Annotated[
        str,
        Path(
            min_length=2,
            max_length=2,
            pattern=r"^[a-zA-Z]{2}$",
            description="countryISO2 must be a 2-letter alphabetic code (e.g., PL, CH)",
        ),
    ],
    db: Session = Depends(get_db),
):
    countryISO2code = countryISO2code.upper()

    codes = db.query(SwiftCodeORM).filter_by(countryISO2=countryISO2code).all()
    if not codes:
        raise HTTPException(status_code=404, detail="Country code does not exists")

    country_name = codes[0].countryName
    branches_data = []
    for item in codes:
        branches_data.append(Switf_Branch(**item.__dict__))
    return Swift_with_Branches_country(
        countryISO2=countryISO2code, countryName=country_name, swiftCodes=branches_data
    )


@router.post("/swift-codes", status_code=201)
def add_swift(body: Swift_Code, db: Session = Depends(get_db)):
    exists = db.query(SwiftCodeORM).filter_by(swiftCode=body.swiftCode).first()
    if exists:
        raise HTTPException(status_code=409, detail="SWIFT code already exists")

    new_item = SwiftCodeORM(**body.model_dump())
    db.add(new_item)
    db.commit()
    return {"message": "SWIFT code added successfully"}


@router.delete("/swift-codes/{swift_code}", status_code=200)
def delete_swift_code(
    swift_code: Annotated[
        str,
        Path(
            min_length=11,
            max_length=11,
            description="SWIFT code must be exactly 11 characters",
        ),
    ],
    db: Session = Depends(get_db),
):
    swift_code = swift_code.upper()
    exists = db.query(SwiftCodeORM).filter_by(swiftCode=swift_code).first()
    if not exists:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    db.delete(exists)
    db.commit()
    return {"message": f"SWIFT code {swift_code} deleted successfully"}
