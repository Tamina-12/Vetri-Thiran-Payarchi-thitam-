from pathlib import Path


def format_txt(content: str, output_path: str) -> str:
    """
    Save content as a TXT file.
    """

    path = Path(output_path)

    # Create the folder if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write the content
    path.write_text(
        content,
        encoding="utf-8"
    )

    return str(path)


def format_document(
    content: str,
    output_path: str,
    file_format: str = "txt"
) -> str:
    """
    Format and save the document.
    """

    if file_format.lower() == "txt":
        return format_txt(content, output_path)

    raise ValueError(
        f"Unsupported document format: {file_format}"
    )
from pathlib import Path


def format_txt(content: str, output_path: str) -> str:
    """Save content as a TXT file."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content,
        encoding="utf-8"
    )

    return str(path)


def format_docx(content: str, output_path: str) -> str:
    """Save content as a DOCX file."""

    try:
        from docx import Document

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        document = Document()
        document.add_paragraph(content)
        document.save(str(path))

        return str(path)

    except ImportError:
        raise ImportError(
            "python-docx is not installed. "
            "Run: pip install python-docx"
        )


def format_document(
    content: str,
    output_path: str,
    file_format: str = "txt"
) -> str:
    """Save content in the requested format."""

    file_format = file_format.lower()

    if file_format == "txt":
        return format_txt(content, output_path)

    if file_format == "docx":
        return format_docx(content, output_path)

    raise ValueError(
        f"Unsupported document format: {file_format}"
    )