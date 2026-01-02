"""
LaTeX to PDF Compiler Service
Compiles LaTeX source to PDF using pdflatex
"""

import subprocess
import tempfile
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class LaTeXCompiler:
    """Compile LaTeX source to PDF"""

    def __init__(self):
        """Initialize LaTeX compiler"""
        self._check_latex_installation()

    def _check_latex_installation(self):
        """Check if pdflatex is installed"""
        try:
            result = subprocess.run(
                ['pdflatex', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("pdflatex found and ready")
                self.is_available = True
            else:
                logger.warning("pdflatex check returned non-zero exit code")
                self.is_available = False
        except FileNotFoundError:
            logger.warning("pdflatex not found - LaTeX compilation will not be available")
            self.is_available = False
        except Exception as e:
            logger.warning(f"Error checking pdflatex: {str(e)}")
            self.is_available = False

    def compile_to_pdf(self, latex_source: str) -> bytes:
        """
        Compile LaTeX source to PDF.

        Args:
            latex_source: LaTeX source code as string

        Returns:
            PDF file as bytes

        Raises:
            Exception: If compilation fails or pdflatex not available
        """
        if not self.is_available:
            raise Exception("pdflatex is not installed. Please install MacTeX or TeX Live.")

        logger.info("Compiling LaTeX to PDF")

        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write LaTeX source to file
            tex_file = temp_path / 'resume.tex'
            tex_file.write_text(latex_source, encoding='utf-8')

            try:
                # Run pdflatex (run twice for references/cross-references)
                for i in range(2):
                    result = subprocess.run(
                        [
                            'pdflatex',
                            '-interaction=nonstopmode',
                            '-output-directory', str(temp_path),
                            str(tex_file)
                        ],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=temp_dir
                    )

                    if result.returncode != 0:
                        logger.error(f"pdflatex compilation failed (run {i+1})")
                        logger.error(f"stdout: {result.stdout}")
                        logger.error(f"stderr: {result.stderr}")
                        if i == 0:
                            # First run might fail on references, continue
                            continue
                        else:
                            raise Exception(f"LaTeX compilation failed: {result.stderr}")

                # Read the generated PDF
                pdf_file = temp_path / 'resume.pdf'
                if not pdf_file.exists():
                    raise Exception("PDF file not generated")

                pdf_bytes = pdf_file.read_bytes()
                logger.info(f"Successfully compiled LaTeX to PDF ({len(pdf_bytes)} bytes)")
                return pdf_bytes

            except subprocess.TimeoutExpired:
                logger.error("pdflatex compilation timeout")
                raise Exception("LaTeX compilation timed out")
            except Exception as e:
                logger.error(f"LaTeX compilation error: {str(e)}", exc_info=True)
                raise Exception(f"Failed to compile LaTeX: {str(e)}")
