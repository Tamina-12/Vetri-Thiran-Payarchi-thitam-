import io
import requests
import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# Create Word Document
# --------------------------------------------------

def create_docx(content):
    document = Document()

    document.add_heading(
        "LegalEase AI - Legal Document",
        level=1
    )

    for paragraph in content.split("\n"):
        document.add_paragraph(paragraph)

    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    return output.getvalue()


# --------------------------------------------------
# Create PDF Document
# --------------------------------------------------

def create_pdf(content):
    output = io.BytesIO()

    pdf = canvas.Canvas(
        output,
        pagesize=A4
    )

    width, height = A4

    x = 50
    y = height - 50

    # Title
    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        x,
        y,
        "LegalEase AI - Legal Document"
    )

    y -= 40

    # Content
    pdf.setFont(
        "Helvetica",
        10
    )

    for paragraph in content.split("\n"):

        words = paragraph.split()
        current_line = ""

        for word in words:

            test_line = (
                current_line + " " + word
            ).strip()

            if pdf.stringWidth(
                test_line,
                "Helvetica",
                10
            ) < width - 100:

                current_line = test_line

            else:

                pdf.drawString(
                    x,
                    y,
                    current_line
                )

                y -= 15

                current_line = word

                if y < 50:

                    pdf.showPage()

                    pdf.setFont(
                        "Helvetica",
                        10
                    )

                    y = height - 50

        if current_line:

            pdf.drawString(
                x,
                y,
                current_line
            )

        y -= 15

        if y < 50:

            pdf.showPage()

            pdf.setFont(
                "Helvetica",
                10
            )

            y = height - 50

    pdf.save()

    output.seek(0)

    return output.getvalue()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("⚖️ LegalEase AI")

st.subheader(
    "AI-Powered Legal Document Generator"
)

st.write(
    "Generate professional legal documents using Generative AI."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("About LegalEase AI")

    st.write(
        "LegalEase AI helps generate legal documents "
        "using Google Gemini."
    )

    st.info(
        "This application is for document generation "
        "and educational purposes."
    )


# --------------------------------------------------
# Document Form
# --------------------------------------------------

st.header("📄 Create Your Legal Document")


document_type = st.selectbox(
    "Document Type",
    [
        "Student Project Agreement",
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "Sale Agreement",
        "Other"
    ]
)



parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Landlord and Tenant"
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder="Enter the important terms and conditions..."
)


effective_date = st.date_input(
    "Effective Date"
)


# --------------------------------------------------
# Generate Button
# --------------------------------------------------

if st.button(
    "✨ Generate Legal Document",
    use_container_width=True
):

    if not parties.strip():

        st.warning(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.warning(
            "Please enter the terms and conditions."
        )

    else:

        request_data = {

            "document_type": document_type,

            "parties": parties,

            "terms": terms,

            "effective_date": str(
                effective_date
            )
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=request_data,

                    timeout=120
                )


            if response.status_code == 200:

                result = response.json()

                if result.get("success"):

                    st.session_state["document"] = (
                        result.get("content", "")
                    )

                    st.success(
                        "✅ Document generated successfully!"
                    )

                else:

                    st.error(
                        "Document generation failed."
                    )

            else:

                try:

                    error_detail = response.json().get(
                        "detail",
                        response.text
                    )

                except Exception:

                    error_detail = response.text

                st.error(
                    f"Backend error: "
                    f"{response.status_code}\n\n"
                    f"{error_detail}"
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to the backend.\n\n"
                "Make sure FastAPI is running on "
                "http://127.0.0.1:8000"
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ Request timed out. "
                "Please try again."
            )


        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )


# --------------------------------------------------
# Generated Document + Downloads
# --------------------------------------------------
if "document" in st.session_state:
    document = st.session_state["document"]
    
    st.divider()
    st.header("📑 Generated Legal Document")

    st.text_area(
        "Document Content",
        value=document,
        height=500
    )

    # your download buttons here


    

    
    

    st.subheader("📥 Download Document")

    # Create Word and PDF files BEFORE the buttons
    docx_bytes = create_docx(document)
    pdf_bytes = create_pdf(document)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("📄 Text File")

        st.download_button(
            label="📥 Download TXT",
            data=document,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.write("📄 Document")

        st.download_button(
            label="📥 Download Document",
            data=docx_bytes,
            file_name="legalease_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )

    with col3:
        st.write("📕 PDF")

        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True
        )


