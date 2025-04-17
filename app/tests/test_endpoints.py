from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.routers.swift import get_db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from app.model_orm import Base


# Tests are done on in memory database


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Full OK data
def test_get_swift_code_success(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/TESTCHPW001")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "TESTCHPW001"
    assert data["isHeadquarter"] is False


# Full OK data, small  letters on countryISO2 and countryName
def test_get_small_letters(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/TESTCHPW001")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "TESTCHPW001"
    assert data["isHeadquarter"] is False
    assert data["countryISO2"] == "CH"
    assert data["countryName"] == "SWITZERLAND"


# Empty string in optional data
def test_empty_string_optional_data(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "",
            "address": "",
            "countryISO2": "CH",
            "countryName": "",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/TESTCHPW001")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "TESTCHPW001"
    assert data["isHeadquarter"] is False
    assert data["bankName"] == ""
    assert data["address"] == ""


# Null in optional data
def test_null_optional_data(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "countryISO2": "CH",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/TESTCHPW001")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "TESTCHPW001"
    assert data["isHeadquarter"] is False
    assert data["bankName"] == None
    assert data["address"] == None


# Wrong types in optional
def test_empty_string_optional_data(client: TestClient):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": 123,
            "address": 123,
            "countryISO2": "CH",
            "countryName": 123,
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# SwiftCode Tests ===============================================================


# Empty string SwiftCode
def test_empty_string_swift(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# Null  SwiftCode
def test_null_swiftCode(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": None,
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# To short swift code
def test_short_swiftCode(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "1111",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# To long swift code
def test_long_swiftCode(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "1111111111111111111111111",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# Adding the same swiftCode
def test_post_the_same_swiftCode(client: TestClient):
    response1 = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
            "bankName": "Bank A",
            "address": "Address A",
        },
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
            "bankName": "Bank B",
            "address": "Address B",
        },
    )
    assert response2.status_code == 409
    data = response2.json()
    assert data["detail"] == "SWIFT code already exists"


# GET no existing swiftCode
def test_get_no_existing_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/NOSWIFTCODE")
    assert response.status_code == 404


# GET wrongly formatted swiftCode
def test_get_wrong_format_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/1")
    assert response.status_code == 422


# GET small letters swiftCode
def test_get_small_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "testchpw001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/testchpw001")
    assert response.status_code == 200


# GET small letters swiftCode but capital in database
def test_get_small_capital_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/testchpw001")
    assert response.status_code == 200


# DEL swiftCode
def test_delete_existing_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Bank Szwajcarski",
            "address": "Zurich",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.delete("/v1/swift-codes/TESTCHPW001")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "SWIFT code TESTCHPW001 deleted successfully"

    get_response = client.get("/v1/swift-codes/TESTCHPW001")
    assert get_response.status_code == 404


# DEL non existing ssiwftCode
def test_delete_non_existing_swiftCode(client: TestClient):
    response = client.delete("/v1/swift-codes/NONEXIST000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "SWIFT code not found"


# DEL wrong format SwiftCode
def test_delete_wrong_foramt_swiftCode(client: TestClient):
    response = client.delete("/v1/swift-codes/XYZ")
    assert response.status_code == 422


# DEL small letters swiftCode
def test_delete_small_letters_swiftCode(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Bank Szwajcarski",
            "address": "Zurich",
            "countryISO2": "CH",
            "countryName": "SWITZERLAND",
            "isHeadquarter": False,
        },
    )

    response = client.delete("/v1/swift-codes/testchpw001")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "SWIFT code TESTCHPW001 deleted successfully"

    get_response = client.get("/v1/swift-codes/testchpw001")
    assert get_response.status_code == 404


# DEL twice the same
def test_delete_twice(client: TestClient):
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TODEL123XXX",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
        },
    )
    assert client.delete("/v1/swift-codes/todel123xxx").status_code == 200
    assert client.delete("/v1/swift-codes/todel123xxx").status_code == 404


# POST after DEL
def test_post_after_delete(client: TestClient):
    swift = {
        "swiftCode": "REPOST123XX",
        "countryISO2": "PL",
        "countryName": "POLAND",
        "isHeadquarter": False,
    }
    client.post("/v1/swift-codes", json=swift)
    client.delete("/v1/swift-codes/repost123xx")
    r = client.post("/v1/swift-codes", json=swift)
    assert r.status_code == 201


# isHeadquarter Tests =================================================================


# Emtpy string isHeadquarter (+ type error)
def test_empty_string_isHeadquarter(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": "",
        },
    )
    assert response.status_code == 422


# Null string isHeadquarter (+ type error)
def test_null_isHeadquarter(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": None,
        },
    )
    assert response.status_code == 422


# Wrong type isHeadquarter
def test_wrong_type_isHeadquarter(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "cH",
            "countryName": "switzerlaND",
            "isHeadquarter": 2,
        },
    )
    assert response.status_code == 422


# countryISO2 ======================================


# Wrond type countryISO2
def test_wrong_type_countryISO2(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": 222,
            "countryName": "switzerlaND",
            "isHeadquarter": False,
        },
    )
    assert response.status_code == 422


# Null countryISO2
def test_null_countryISO2(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryName": "switzerlaND",
            "isHeadquarter": True,
        },
    )
    assert response.status_code == 422


# Empty string countryISO2
def test_null_countryISO2(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "",
            "countryName": "switzerlaND",
            "isHeadquarter": True,
        },
    )
    assert response.status_code == 422


# GET small letters on countryISO2
def test_get_small_countryISO2(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "switzerlaND",
            "isHeadquarter": True,
        },
    )
    assert response.status_code == 201
    response2 = client.get("/v1/swift-codes/country/ch")
    assert response2.status_code == 200
    data = response2.json()
    assert data["countryISO2"] == "CH"
    assert data["countryName"] == "SWITZERLAND"


# GET null on countryISO2 -- redirect to swiftCode Endpoint
def test_missing_countryISO2(
    client: TestClient,
):
    response = client.get("/v1/swift-codes/country/")
    assert response.status_code == 422


# GET no existance countryISO2
def test_get_no_countryISO2(
    client: TestClient,
):
    response = client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "TESTCHPW001",
            "bankName": "Swiss Bank",
            "address": "Zurich Center",
            "countryISO2": "CH",
            "countryName": "switzerlaND",
            "isHeadquarter": True,
        },
    )
    assert response.status_code == 201
    response2 = client.get("/v1/swift-codes/country/PL")
    assert response2.status_code == 404
    data = response2.json()
    assert data["detail"] == "Country code does not exists"


# Additionally manual testing in /docs has beed done to ensure the right format of returned data
def test_get_hq_with_branches(client: TestClient):
    # Add HQ
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "BANKTESTXXX",
            "bankName": "Bank HQ",
            "address": "HQ St",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": True,
        },
    )
    # Add branch
    client.post(
        "/v1/swift-codes",
        json={
            "swiftCode": "BANKTEST001",
            "bankName": "Branch",
            "address": "Branch St",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
        },
    )

    response = client.get("/v1/swift-codes/BANKTESTXXX")
    data = response.json()
    assert response.status_code == 200
    assert data["swiftCode"] == "BANKTESTXXX"
    assert data["isHeadquarter"] is True
    assert isinstance(data["branches"], list)
    assert len(data["branches"]) == 1
