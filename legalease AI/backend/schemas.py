from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    """
    Request sent to the document generation API.
    """

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class DocumentResponse(BaseModel):
    """
    Response returned after AI generation.
    """

    success: bool

    document_type: str

    content: str

    message: str


class ExportRequest(BaseModel):
    """
    Request used to create downloadable documents.
    """

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )