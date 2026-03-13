import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
    logger.info("Docling est correctement importé.")
except ImportError as e:
    class DocumentConverter:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Docling n'est pas installé.")
    DOCLING_AVAILABLE = False
    logger.warning("Docling désactivé : %s", str(e), exc_info=True)
except Exception as e:
    class DocumentConverter:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Docling n'est pas disponible.")
    DOCLING_AVAILABLE = False
    logger.error("Erreur inattendue lors de l'import de Docling : %s", str(e), exc_info=True)


def parse_pdf(pdf_path: str) -> str:
    """
    Convertit un fichier PDF en Markdown en utilisant Docling.
    """
    if not DOCLING_AVAILABLE or DocumentConverter is None:
        logger.error("Docling n'est pas disponible.")
        raise RuntimeError("Docling n'est pas disponible sur ce système.")

    if not os.path.exists(pdf_path):
        logger.error(f"Fichier non trouvé : {pdf_path}")
        raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas.")

    try:
        logger.info(f"Début de la conversion pour : {pdf_path}")
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        
        # Docling 2.x export_to_markdown() est disponible sur result.document
        markdown_output = result.document.export_to_markdown()
        
        logger.info(f"Conversion réussie pour : {pdf_path}")
        return markdown_output
    except Exception as e:
        logger.error(f"Erreur lors de la conversion de {pdf_path} : {str(e)}")
        raise RuntimeError(f"Échec du parsing Docling : {str(e)}")
