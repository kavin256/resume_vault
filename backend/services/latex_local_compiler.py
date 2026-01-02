"""
Local LaTeX Compiler Service
Compiles LaTeX source to PDF using local pdflatex installation
"""

import subprocess
import tempfile
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class LaTeXLocalCompiler:
    """Compile LaTeX using local pdflatex installation"""

    def __init__(self, pdflatex_path: str = None):
        """
        Initialize LaTeX compiler

        Args:
            pdflatex_path: Path to pdflatex executable (auto-detected if not provided)
        """
        # Auto-detect pdflatex path if not provided
        if pdflatex_path is None:
            import shutil
            pdflatex_path = shutil.which("pdflatex")
            if pdflatex_path is None:
                # Fallback to common paths
                common_paths = [
                    "/usr/bin/pdflatex",  # Linux/Docker
                    "/Library/TeX/texbin/pdflatex",  # macOS
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        pdflatex_path = path
                        break
                else:
                    raise Exception("pdflatex not found. Please install TeX Live or MacTeX.")

        self.pdflatex_path = pdflatex_path
        logger.info(f"LaTeX local compiler initialized (pdflatex: {pdflatex_path})")

    async def compile_to_pdf(self, latex_source: str) -> bytes:
        """
        Compile LaTeX source to PDF using local pdflatex.

        Args:
            latex_source: LaTeX source code as string

        Returns:
            PDF file as bytes

        Raises:
            Exception: If compilation fails
        """
        logger.info("Compiling LaTeX to PDF using local pdflatex")

        # Create a temporary directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / "resume.tex"
            pdf_file = temp_path / "resume.pdf"

            # Write LaTeX source to file
            tex_file.write_text(latex_source, encoding='utf-8')
            logger.info(f"Wrote LaTeX source to {tex_file}")

            try:
                # Run pdflatex
                # -interaction=nonstopmode: Don't stop for errors
                # -halt-on-error: But do halt if there's an error
                # -output-directory: Where to put output files
                result = subprocess.run(
                    [
                        self.pdflatex_path,
                        '-interaction=nonstopmode',
                        '-halt-on-error',
                        '-output-directory', str(temp_path),
                        str(tex_file)
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,  # 60 second timeout
                    cwd=temp_dir
                )

                # Check if PDF was generated
                if pdf_file.exists():
                    pdf_bytes = pdf_file.read_bytes()
                    logger.info(f"Successfully compiled LaTeX to PDF ({len(pdf_bytes)} bytes)")
                    return pdf_bytes
                else:
                    # Compilation failed
                    error_msg = self._extract_error(result.stdout, result.stderr)
                    logger.error(f"LaTeX compilation failed: {error_msg}")
                    raise Exception(f"LaTeX compilation failed: {error_msg}")

            except subprocess.TimeoutExpired:
                error_msg = "LaTeX compilation timed out (60s)"
                logger.error(error_msg)
                raise Exception(error_msg)
            except subprocess.CalledProcessError as e:
                error_msg = f"pdflatex error: {e.stderr}"
                logger.error(error_msg)
                raise Exception(error_msg)
            except Exception as e:
                error_msg = f"LaTeX compilation error: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise Exception(error_msg)

    def _extract_error(self, stdout: str, stderr: str) -> str:
        """Extract meaningful error message from pdflatex output"""
        # Look for common error patterns in output
        error_lines = []

        for line in stdout.split('\n'):
            # Look for error indicators
            if line.startswith('!') or 'Error:' in line or 'error' in line.lower():
                error_lines.append(line.strip())

        if error_lines:
            return '\n'.join(error_lines[:5])  # Return first 5 error lines

        # If no specific errors found, return last few lines of output
        lines = stdout.split('\n')
        return '\n'.join(lines[-10:])
