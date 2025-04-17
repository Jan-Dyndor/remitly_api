from app.database import Base
from sqlalchemy import Boolean, Column, String


class SwiftCodeORM(Base):
    __tablename__ = "swift_codes"

    swiftCode = Column(String(11), primary_key=True, index=True)
    bankName = Column(String(100), nullable=True)
    address = Column(String(200), nullable=True)
    countryISO2 = Column(String(2), nullable=False)
    countryName = Column(String(100), nullable=True)
    isHeadquarter = Column(Boolean, default=False)
