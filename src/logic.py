from typing import Final
import logging

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.exceptions import DataOverflowError
from PIL import Image

logger = logging.getLogger(__name__)


class QRCodeGenerationError(Exception):
    """Base exception for QR generation failures."""


class QRCodeDataTooLargeError(QRCodeGenerationError):
    """Raised when input data exceeds QR code capacity."""


class QRCodeGenerator:
    """
    Pure business logic for QR code generation.
    """

    ERROR_CORRECTION: Final = ERROR_CORRECT_H
    BORDER: Final = 4
    BOX_SIZE: Final = 10

    @staticmethod
    def generate_qr(data: str) -> Image.Image:
        """
        Generate a QR code image from input data.

        Args:
            data (str): Text or URL to encode.

        Returns:
            Image.Image: Generated QR code image.

        Raises:
            QRCodeDataTooLargeError: If data cannot fit in a QR matrix.
            QRCodeGenerationError: For other QR-related failures.
        """
        try:
            qr = qrcode.QRCode(
                version=None, 
                error_correction=QRCodeGenerator.ERROR_CORRECTION,
                box_size=QRCodeGenerator.BOX_SIZE,
                border=QRCodeGenerator.BORDER,
            )

            qr.add_data(data)
            qr.make(fit=True)

            return qr.make_image(fill_color="black", back_color="white")

        except DataOverflowError as exc:
            logger.warning("QR data too large: %s", data, exc_info=True)
            raise QRCodeDataTooLargeError(
                "The provided data is too long to encode as a QR code."
            ) from exc

        except Exception as exc:
            logger.exception("Unexpected QR generation failure")
            raise QRCodeGenerationError("QR code generation failed.") from exc
