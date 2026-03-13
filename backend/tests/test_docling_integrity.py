import pytest
import logging
from backend.app.parser import DOCLING_AVAILABLE

logger = logging.getLogger(__name__)

def test_docling_dependency_integrity():
    """
    Vérifie que docling est non seulement installé mais aussi instanciable.
    Cela permet de détecter les dépendances système manquantes (ex: libgl1).
    """
    if not DOCLING_AVAILABLE:
        pytest.skip("Docling n'est pas installé dans cet environnement.")
    
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        assert converter is not None
        logger.info("Docling DocumentConverter a été instancié avec succès.")
    except Exception as e:
        pytest.fail(f"Docling est installé mais ne peut pas être instancié. Erreur possible de dépendance système : {str(e)}")

def test_docling_import_status():
    """
    Vérifie que DOCLING_AVAILABLE reflète la réalité de l'environnement.
    """
    try:
        from docling.document_converter import DocumentConverter
        expected_available = True
    except ImportError:
        expected_available = False
    
    assert DOCLING_AVAILABLE == expected_available
