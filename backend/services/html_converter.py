"""
HTML to PDF Conversion Service
Converts HTML resumes to PDF format using WeasyPrint
"""

from weasyprint import HTML, CSS
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class HTMLToPDFConverter:
    """Convert HTML documents to PDF format"""

    def __init__(self):
        """Initialize PDF converter"""
        pass

    def convert(self, html_content: str) -> bytes:
        """
        Convert HTML string to PDF bytes.

        WeasyPrint handles:
        - CSS styling (including inline styles)
        - Page breaks and print media queries
        - Professional PDF output
        - Font embedding

        Args:
            html_content: Complete HTML document string

        Returns:
            PDF file as bytes

        Raises:
            Exception: If PDF conversion fails
        """
        try:
            logger.info("Converting HTML to PDF")

            # Create BytesIO buffer for PDF output
            pdf_buffer = BytesIO()

            # Convert HTML to PDF
            # WeasyPrint will respect @media print rules in the HTML
            HTML(string=html_content).write_pdf(pdf_buffer)

            # Get PDF bytes
            pdf_buffer.seek(0)
            pdf_bytes = pdf_buffer.read()

            logger.info(f"Successfully converted HTML to PDF ({len(pdf_bytes)} bytes)")
            return pdf_bytes

        except Exception as e:
            logger.error(f"Failed to convert HTML to PDF: {str(e)}", exc_info=True)
            raise Exception(f"PDF conversion failed: {str(e)}")

    def convert_with_custom_css(self, html_content: str, additional_css: str = None) -> bytes:
        """
        Convert HTML to PDF with additional CSS for print optimization.

        Args:
            html_content: Complete HTML document string
            additional_css: Optional CSS string to add for print

        Returns:
            PDF file as bytes
        """
        try:
            logger.info("Converting HTML to PDF with custom CSS")

            pdf_buffer = BytesIO()

            # Create HTML object
            html = HTML(string=html_content)

            # Add custom CSS if provided
            if additional_css:
                css = CSS(string=additional_css)
                html.write_pdf(pdf_buffer, stylesheets=[css])
            else:
                html.write_pdf(pdf_buffer)

            pdf_buffer.seek(0)
            pdf_bytes = pdf_buffer.read()

            logger.info(f"Successfully converted HTML to PDF with custom CSS ({len(pdf_bytes)} bytes)")
            return pdf_bytes

        except Exception as e:
            logger.error(f"Failed to convert HTML to PDF: {str(e)}", exc_info=True)
            raise Exception(f"PDF conversion failed: {str(e)}")


# Print-optimized CSS that can be added if needed
PRINT_OPTIMIZATION_CSS = """
@page {
    size: A4;
    margin: 1cm;
}

body {
    margin: 0;
    padding: 0;
}

/* Prevent page breaks inside important sections */
[data-section="experience"],
[data-section="education"],
[data-section="summary"] {
    page-break-inside: avoid;
}

/* Ensure header stays together */
[data-section="header"] {
    page-break-after: avoid;
}
"""
