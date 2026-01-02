"""
LaTeX.Online API Compiler Service
Compiles LaTeX source to PDF using latexonline.cc API
"""

import httpx
import logging
import urllib.parse

logger = logging.getLogger(__name__)


class LaTeXOnlineCompiler:
    """Compile LaTeX using latexonline.cc free API"""

    # Using latexonline.cc which has a simpler API
    COMPILE_URL = "https://latexonline.cc/compile"

    def __init__(self):
        """Initialize LaTeX compiler"""
        self.timeout = 120.0
        logger.info("LaTeX online compiler initialized (latexonline.cc)")

    async def compile_to_pdf(self, latex_source: str) -> bytes:
        """
        Compile LaTeX source to PDF using latexonline.cc API.

        Args:
            latex_source: LaTeX source code as string

        Returns:
            PDF file as bytes

        Raises:
            Exception: If compilation fails
        """
        logger.info("Compiling LaTeX to PDF using latexonline.cc API")

        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                # Use multipart/form-data file upload to avoid URL length limits
                # This simulates uploading a .tex file
                files = {
                    'file': ('resume.tex', latex_source.encode('utf-8'), 'text/x-tex')
                }

                data = {
                    'command': 'pdflatex'
                }

                response = await client.post(
                    self.COMPILE_URL,
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    # Check if response is PDF
                    if response.content[:4] == b'%PDF':
                        logger.info(f"Successfully compiled LaTeX to PDF ({len(response.content)} bytes)")
                        return response.content
                    else:
                        # Response might be an error message
                        error_text = response.text[:500]
                        logger.error(f"Compilation failed. Response: {error_text}")
                        raise Exception(f"LaTeX compilation failed: {error_text}")
                else:
                    raise Exception(
                        f"LaTeX compilation failed: HTTP {response.status_code}"
                    )

        except httpx.TimeoutException:
            error_msg = "LaTeX compilation timed out"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.HTTPError as e:
            error_msg = f"LaTeX API error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"LaTeX compilation error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg)

