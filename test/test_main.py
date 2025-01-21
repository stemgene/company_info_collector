import pytest
from fetch_data.main import StaticPageParser, CompanyInfoReaderFromMongoDB

# Test read from MongoDB
def test_read_data_from_db():
    reader = CompanyInfoReaderFromMongoDB()
    data = reader.read_data_from_db()
    assert isinstance(data, list), "Data should be a list"
    assert len(data) > 0, "Data list should not be empty"
