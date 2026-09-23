"""
PDF text extraction.

FIX vs original app.py:
- Original had zero error handling. A corrupted PDF or a scanned/image-only PDF
  (extract_text() returns "") would silently produce an empty string, which then
  crashes TfidfVectorizer downstream with a confusing "empty vocabulary" error
  instead of a clear message to the user.
"""

from dataclasses import dataclass
import PyPDF2


@dataclass
class ExtractionResult:
    filename: str
    text: str
    success: bool
    error: str | None = None
    is_likely_scanned: bool = False


def extract_resume_text_from_file(uploaded_file) -> ExtractionResult:
    """Read a PDF from a Streamlit UploadedFile and return its text safely."""
    filename = uploaded_file.name
    try:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(uploaded_file)

        if reader.is_encrypted:
            try:
                reader.decrypt("")  # try empty password, common for "protected" exports
            except Exception:
                return ExtractionResult(
                    filename=filename,
                    text="",
                    success=False,
                    error="PDF is password-protected and could not be opened.",
                )

        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        full_text = "\n".join(text_parts).strip()

        if not full_text:
            return ExtractionResult(
                filename=filename,
                text="",
                success=False,
                error="No extractable text found (this PDF is likely a scanned image, not real text).",
                is_likely_scanned=True,
            )

        return ExtractionResult(filename=filename, text=full_text, success=True)

    except Exception as exc:  # PyPDF2 can raise several different exception types
        return ExtractionResult(
            filename=filename,
            text="",
            success=False,
            error=f"Could not read this PDF: {exc}",
        )
