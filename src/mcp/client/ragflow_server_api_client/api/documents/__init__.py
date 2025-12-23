"""Contains endpoint functions for accessing the API"""

# Импортируем модули для удобства использования
from .clear_documents_documents_delete import asyncio as async_clear_documents
from .clear_documents_documents_delete import sync as clear_documents
from .documents_documents_get import asyncio as async_get_documents
from .documents_documents_get import sync as get_documents
from .get_pipeline_status_documents_pipeline_status_get import asyncio as async_get_pipeline_status
from .get_pipeline_status_documents_pipeline_status_get import sync as get_pipeline_status
from .insert_batch_documents_file_batch_post import asyncio as async_insert_batch
from .insert_batch_documents_file_batch_post import sync as insert_batch
from .insert_file_documents_file_post import asyncio as async_insert_file
from .insert_file_documents_file_post import sync as insert_file
from .insert_text_documents_text_post import asyncio as async_insert_document
from .insert_text_documents_text_post import sync as insert_document
from .insert_texts_documents_texts_post import asyncio as async_insert_texts
from .insert_texts_documents_texts_post import sync as insert_texts
from .scan_for_new_documents_documents_scan_post import asyncio as async_scan_for_new_documents
from .scan_for_new_documents_documents_scan_post import sync as scan_for_new_documents
from .upload_to_input_dir_documents_upload_post import asyncio as async_upload_document
from .upload_to_input_dir_documents_upload_post import sync as upload_document

__all__ = [
    "clear_documents",
    "async_clear_documents",
    "get_documents",
    "async_get_documents",
    "get_pipeline_status",
    "async_get_pipeline_status",
    "insert_batch",
    "async_insert_batch",
    "insert_file",
    "async_insert_file",
    "insert_document",
    "async_insert_document",
    "insert_texts",
    "async_insert_texts",
    "scan_for_new_documents",
    "async_scan_for_new_documents",
    "upload_document",
    "async_upload_document",
]
