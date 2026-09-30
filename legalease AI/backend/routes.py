from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
    ExportRequest,
)
from backend.services.document_formatter import (
    format_txt,
    format_docx,
    format_document,
)


# --------------------------------------------------
# Router
# --------------------------------------------------

router = APIRouter()


# --------------------------------------------------
# Gemini AI Generator
# --------------------------------------------------

generator = GeminiDocumentGenerator()


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@router.get("/health")
async def health_check():
    """
    Check whether the LegalEase API is running.
    """
    return {
        "status": "healthy",
        "service": "LegalEase API"
    }


# --------------------------------------------------
# Generate Legal Document
# --------------------------------------------------

@router.post("/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Generate a legal document using Gemini AI.
    """

    try:
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        # Gemini generator returns an error string if Gemini fails
        if content.startswith("Gemini AI error:"):
            print("\n"+"!"*40)
            print("grmini api error details:",content)
            print("!"*40 +"\n")
            raise HTTPException(
                status_code=500,
                detail=content
            )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=content,
            message="Document generated successfully."
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(e)}"
        )


# --------------------------------------------------
# Export TXT
# --------------------------------------------------

@router.post("/export/txt")
async def export_txt(request: ExportRequest):
    """
    Export the generated document as a TXT file.
    """

    try:
        output_path = Path("exports") / "legal_document.txt"

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        format_txt(
            request.content,
            str(output_path)
        )

        return Response(
            content=output_path.read_bytes(),
            media_type="text/plain",
            headers={
                "Content-Disposition":
                    'attachment; filename="legal_document.txt"'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TXT export failed: {str(e)}"
        )


# --------------------------------------------------
# Export DOCX
# --------------------------------------------------

@router.post("/export/docx")
async def export_docx(request: ExportRequest):
    """
    Export the generated document as a DOCX file.
    """

    try:
        output_path = Path("exports") / "legal_document.docx"

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        format_docx(
            request.content,
            str(output_path)
        )

        return Response(
            content=output_path.read_bytes(),
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            headers={
                "Content-Disposition":
                    'attachment; filename="legal_document.docx"'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"DOCX export failed: {str(e)}"
        )


# --------------------------------------------------
# Export PDF
# --------------------------------------------------

@router.post("/export/pdf")
async def export_pdf(request: ExportRequest):
    """
    Export the generated document as a PDF file.
    """

    try:
        output_path = Path("exports") / "legal_document.pdf"

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        format_document(
            content=request.content,
            output_path=str(output_path),
            file_format="pdf"
        )

        return Response(
            content=output_path.read_bytes(),
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    'attachment; filename="legal_document.pdf"'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed: {str(e)}"
        )