from enum import Enum


class TransactionCategory(str, Enum):
    FOOD = "Food"
    TRAVEL = "Travel"
    GROCERIES = "Groceries"
    BILLS = "Bills"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    TRANSPORTATION = "Transportation"
    OTHER = "Other"


class FileType(str, Enum):
    PDF = "pdf"
    CSV = "csv"


class FileProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
