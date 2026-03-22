from __future__ import annotations

import csv
import io
import logging
import re
from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import FileType
from app.domain.exceptions import FileProcessingError

logger = logging.getLogger(__name__)


@dataclass
class RawTransaction:
    date: str
    description: str
    amount: float


class ParserService:
    """Parses CSV and structured PDF files to extract transactions."""

    def parse(self, file_data: bytes, file_type: FileType) -> list[RawTransaction]:
        if file_type == FileType.CSV:
            return self._parse_csv(file_data)
        elif file_type == FileType.PDF:
            return self._parse_pdf(file_data)
        raise FileProcessingError(f"Unsupported file type: {file_type}")

    # ── CSV ───────────────────────────────────────────────────────────────

    def _parse_csv(self, data: bytes) -> list[RawTransaction]:
        try:
            text = data.decode("utf-8-sig")  # handle BOM
        except UnicodeDecodeError:
            text = data.decode("latin-1")

        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise FileProcessingError("CSV file has no headers")

        # Normalize headers: lowercase, strip whitespace, remove residual BOM
        field_map = {f.strip().lower().lstrip('\ufeff'): f for f in reader.fieldnames}

        date_col = self._find_column(field_map, ["date", "transaction date", "trans date", "posting date"])
        desc_col = self._find_column(field_map, ["description", "memo", "details", "transaction description", "narration"])
        amount_col = self._find_column(field_map, ["amount", "transaction amount", "debit", "value"])

        if not all([date_col, desc_col, amount_col]):
            raise FileProcessingError(
                "Could not identify required columns (date, description, amount) in CSV. "
                f"Found headers: {list(field_map.keys())}"
            )

        transactions: list[RawTransaction] = []
        for row_num, row in enumerate(reader, start=2):
            try:
                raw_date = row[date_col].strip()
                description = row[desc_col].strip()
                raw_amount = row[amount_col].strip()

                if not raw_date or not description or not raw_amount:
                    continue

                parsed_date = self._normalize_date(raw_date)
                amount = self._parse_amount(raw_amount)

                if amount == 0.0:
                    continue

                transactions.append(RawTransaction(
                    date=parsed_date,
                    description=description,
                    amount=amount,
                ))
            except (ValueError, KeyError) as exc:
                logger.warning("Skipping CSV row %d: %s", row_num, exc)
                continue

        if not transactions:
            raise FileProcessingError("No valid transactions found in CSV")

        logger.info("Parsed %d transactions from CSV", len(transactions))
        return transactions

    # ── PDF ───────────────────────────────────────────────────────────────

    def _parse_pdf(self, data: bytes) -> list[RawTransaction]:
        try:
            import pdfplumber
        except ImportError:
            raise FileProcessingError("pdfplumber is required for PDF parsing")

        transactions: list[RawTransaction] = []
        try:
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                for page in pdf.pages:
                    # Try table extraction first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            transactions.extend(self._parse_pdf_table(table))
                    else:
                        # Fallback: line-by-line text extraction
                        text = page.extract_text()
                        if text:
                            transactions.extend(self._parse_pdf_text(text))
        except Exception as exc:
            raise FileProcessingError(f"Failed to parse PDF: {exc}")

        if not transactions:
            raise FileProcessingError("No valid transactions found in PDF")

        logger.info("Parsed %d transactions from PDF", len(transactions))
        return transactions

    def _parse_pdf_table(self, table: list[list[str | None]]) -> list[RawTransaction]:
        """Parse a table extracted from PDF."""
        if len(table) < 2:
            return []

        # First row is headers
        headers = [str(h).strip().lower() if h else "" for h in table[0]]
        date_idx = self._find_index(headers, ["date", "trans date", "posting date"])
        desc_idx = self._find_index(headers, ["description", "details", "memo", "narration"])
        amt_idx = self._find_index(headers, ["amount", "debit", "value"])

        if date_idx is None or desc_idx is None or amt_idx is None:
            return []

        results: list[RawTransaction] = []
        for row in table[1:]:
            try:
                if len(row) <= max(date_idx, desc_idx, amt_idx):
                    continue
                raw_date = str(row[date_idx] or "").strip()
                desc = str(row[desc_idx] or "").strip()
                raw_amt = str(row[amt_idx] or "").strip()

                if not raw_date or not desc or not raw_amt:
                    continue

                results.append(RawTransaction(
                    date=self._normalize_date(raw_date),
                    description=desc,
                    amount=self._parse_amount(raw_amt),
                ))
            except (ValueError, IndexError):
                continue

        return results

    def _parse_pdf_text(self, text: str) -> list[RawTransaction]:
        """Regex fallback for line-based parsing of statement text."""
        # Pattern: date description amount
        pattern = re.compile(
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+"  # date
            r"(.+?)\s+"                               # description
            r"(-?\$?[\d,]+\.?\d{0,2})\s*$",           # amount
            re.MULTILINE,
        )
        results: list[RawTransaction] = []
        for match in pattern.finditer(text):
            try:
                results.append(RawTransaction(
                    date=self._normalize_date(match.group(1)),
                    description=match.group(2).strip(),
                    amount=self._parse_amount(match.group(3)),
                ))
            except ValueError:
                continue
        return results

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _find_column(field_map: dict[str, str], candidates: list[str]) -> str | None:
        for c in candidates:
            if c in field_map:
                return field_map[c]
        return None

    @staticmethod
    def _find_index(headers: list[str], candidates: list[str]) -> int | None:
        for c in candidates:
            if c in headers:
                return headers.index(c)
        return None

    @staticmethod
    def _normalize_date(raw: str) -> str:
        """Try common date formats and return YYYY-MM-DD."""
        formats = [
            "%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y",
            "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%y", "%d/%m/%y",
            "%b %d, %Y", "%d %b %Y",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(raw.strip(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {raw}")

    @staticmethod
    def _parse_amount(raw: str) -> float:
        """Parse amount string, handling $, commas, parentheses for negatives."""
        cleaned = raw.strip()
        # Handle parentheses notation for negatives: (123.45)
        if cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = "-" + cleaned[1:-1]
        cleaned = cleaned.replace("$", "").replace(",", "").strip()
        return float(cleaned)
