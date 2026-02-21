"""Report Parser Service
Receives an uploaded file path (PDF or plain text).
Extracts raw text, cleans it, and returns a single clean string.
Raises ValueError for corrupt / unreadable / unsupported files.
"""
import os
import re
from utils.logger import get_logger

logger = get_logger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".text"}


class ReportParserService:
    def parse(self, file_path: str) -> str:
        """Parse a report file and return clean text.

        Args:
            file_path: absolute or relative path to the report file.

        Returns:
            Cleaned text string.

        Raises:
            FileNotFoundError: if the file does not exist.
            ValueError: if the file type is unsupported, empty, or unreadable.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Report file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{ext}'. "
                f"Supported types: {', '.join(SUPPORTED_EXTENSIONS)}. "
                "Please re-upload a PDF or plain-text file."
            )

        logger.info(f"ReportParserService: parsing {ext} file — {file_path}")

        if ext == ".pdf":
            raw_text = self._extract_pdf(file_path)
        else:
            raw_text = self._extract_text(file_path)

        if not raw_text or not raw_text.strip():
            raise ValueError(
                f"Could not extract text from '{file_path}'. "
                "The file may be corrupt or empty. Please re-upload."
            )

        cleaned = self._clean(raw_text)
        logger.info(f"ReportParserService: extracted {len(cleaned)} chars from {os.path.basename(file_path)}")
        return cleaned

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    def _extract_pdf(self, file_path: str) -> str:
        try:
            import PyPDF2
            text_parts = []
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if reader.is_encrypted:
                    raise ValueError(
                        f"PDF '{file_path}' is password-protected. "
                        "Please provide an unencrypted file."
                    )
                for page_num, page in enumerate(reader.pages, start=1):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_parts.append(page_text)
                    else:
                        logger.warning(f"ReportParserService: page {page_num} yielded no text")
            return "\n".join(text_parts)
        except (PyPDF2.errors.PdfReadError, Exception) as e:
            raise ValueError(
                f"Failed to read PDF '{file_path}': {e}. "
                "The file may be corrupt. Please re-upload."
            ) from e

    def _extract_text(self, file_path: str) -> str:
        encodings = ["utf-8", "latin-1", "cp1252"]
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise ValueError(
                    f"Failed to read text file '{file_path}': {e}. "
                    "The file may be corrupt. Please re-upload."
                ) from e
        raise ValueError(
            f"Unable to decode '{file_path}' with any supported encoding. "
            "Please re-upload in UTF-8 format."
        )

    # ------------------------------------------------------------------
    # Cleaning
    # ------------------------------------------------------------------

    def _clean(self, text: str) -> str:
        """Remove headers, footers, page numbers, and excess whitespace."""
        # Remove page numbers (standalone digits on their own line)
        text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

        # Remove common header/footer noise (e.g. "Page 1 of 5", "Confidential")
        text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"(Confidential|Draft|DRAFT|CONFIDENTIAL)\b.*", "", text)

        # Collapse multiple blank lines into a single blank line
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip leading/trailing whitespace from each line
        lines = [line.rstrip() for line in text.splitlines()]
        text = "\n".join(lines)

        # Final strip
        return text.strip()
