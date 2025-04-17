from app.database import engine
from app.model_orm import SwiftCodeORM

if __name__ == "__main__":
    SwiftCodeORM.metadata.create_all(bind=engine)
    print("Data Base Created!")
