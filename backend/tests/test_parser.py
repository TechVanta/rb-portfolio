import pytest

from app.domain.enums import FileType
from app.domain.exceptions import FileProcessingError
from app.services.parser_service import ParserService


@pytest.fixture
def parser():
    return ParserService()


class TestCSVParsing:
    def test_standard_csv(self, parser: ParserService):
        csv_data = (
            "Date,Description,Amount\n"
            "2025-01-15,Starbucks Coffee,4.50\n"
            "2025-01-16,Amazon Purchase,29.99\n"
            "2025-01-17,Monthly Rent,1200.00\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 3
        assert result[0].date == "2025-01-15"
        assert result[0].description == "Starbucks Coffee"
        assert result[0].amount == 4.50

    def test_csv_with_dollar_signs(self, parser: ParserService):
        csv_data = (
            "Transaction Date,Memo,Transaction Amount\n"
            "01/20/2025,Uber Ride,$15.75\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 1
        assert result[0].amount == 15.75

    def test_csv_with_commas_in_amount(self, parser: ParserService):
        csv_data = (
            "Date,Description,Amount\n"
            "2025-03-01,Wire Transfer,\"1,500.00\"\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 1
        assert result[0].amount == 1500.00

    def test_csv_negative_amounts(self, parser: ParserService):
        csv_data = (
            "Date,Description,Amount\n"
            "2025-02-01,Refund,-25.00\n"
            "2025-02-02,Payment,(50.00)\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 2
        assert result[0].amount == -25.00
        assert result[1].amount == -50.00

    def test_csv_alternate_headers(self, parser: ParserService):
        csv_data = (
            "Posting Date,Details,Debit\n"
            "03/15/2025,Grocery Store,45.67\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 1
        assert result[0].description == "Grocery Store"

    def test_csv_skips_empty_rows(self, parser: ParserService):
        csv_data = (
            "Date,Description,Amount\n"
            "2025-01-01,Valid,10.00\n"
            ",,\n"
            "2025-01-02,Also Valid,20.00\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 2

    def test_csv_empty_file_raises(self, parser: ParserService):
        csv_data = b"Date,Description,Amount\n"
        with pytest.raises(FileProcessingError, match="No valid transactions"):
            parser.parse(csv_data, FileType.CSV)

    def test_csv_no_headers_raises(self, parser: ParserService):
        with pytest.raises(FileProcessingError):
            parser.parse(b"", FileType.CSV)

    def test_csv_bom_handling(self, parser: ParserService):
        csv_data = "Date,Description,Amount\n2025-01-01,Test,10.00\n".encode("utf-8-sig")
        result = parser.parse(csv_data, FileType.CSV)
        assert len(result) == 1

    def test_date_format_mm_dd_yyyy(self, parser: ParserService):
        csv_data = (
            "Date,Description,Amount\n"
            "12/25/2025,Christmas Gift,50.00\n"
        ).encode()
        result = parser.parse(csv_data, FileType.CSV)
        assert result[0].date == "2025-12-25"


class TestDateNormalization:
    def test_iso_format(self, parser: ParserService):
        assert parser._normalize_date("2025-01-15") == "2025-01-15"

    def test_us_format(self, parser: ParserService):
        assert parser._normalize_date("01/15/2025") == "2025-01-15"

    def test_short_year(self, parser: ParserService):
        assert parser._normalize_date("01/15/25") == "2025-01-15"

    def test_invalid_date_raises(self, parser: ParserService):
        with pytest.raises(ValueError, match="Unrecognized"):
            parser._normalize_date("not-a-date")


class TestAmountParsing:
    def test_plain_number(self, parser: ParserService):
        assert parser._parse_amount("123.45") == 123.45

    def test_with_dollar_sign(self, parser: ParserService):
        assert parser._parse_amount("$123.45") == 123.45

    def test_with_commas(self, parser: ParserService):
        assert parser._parse_amount("1,234.56") == 1234.56

    def test_parentheses_negative(self, parser: ParserService):
        assert parser._parse_amount("(50.00)") == -50.00

    def test_negative_sign(self, parser: ParserService):
        assert parser._parse_amount("-75.00") == -75.00
