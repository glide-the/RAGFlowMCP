"""Contains endpoint functions for accessing the API"""

# Импортируем модули для удобства использования
from .create_entity_entities_entity_name_post import asyncio as async_create_entity
from .create_entity_entities_entity_name_post import sync as create_entity
from .create_relation_relations_source_target_post import (
    asyncio as async_create_relation,
)
from .create_relation_relations_source_target_post import sync as create_relation
from .delete_by_doc_id_documents_doc_id_delete import asyncio as async_delete_by_doc_id
from .delete_by_doc_id_documents_doc_id_delete import sync as delete_by_doc_id
from .delete_entity_entities_entity_name_delete import asyncio as async_delete_entity
from .delete_entity_entities_entity_name_delete import sync as delete_entity
from .edit_entity_entities_entity_name_put import asyncio as async_edit_entity
from .edit_entity_entities_entity_name_put import sync as edit_entity
from .edit_relation_relations_source_target_put import asyncio as async_edit_relation
from .edit_relation_relations_source_target_put import sync as edit_relation
from .get_graph_labels_graph_label_list_get import asyncio as async_get_graph_labels
from .get_graph_labels_graph_label_list_get import sync as get_graph_labels
from .get_knowledge_graph_graphs_get import asyncio as async_get_knowledge_graph
from .get_knowledge_graph_graphs_get import sync as get_knowledge_graph
from .merge_entities_entities_merge_post import asyncio as async_merge_entities
from .merge_entities_entities_merge_post import sync as merge_entities

__all__ = [
    "get_graph_labels",
    "async_get_graph_labels",
    "get_knowledge_graph",
    "async_get_knowledge_graph",
    "create_entity",
    "async_create_entity",
    "create_relation",
    "async_create_relation",
    "delete_entity",
    "async_delete_entity",
    "edit_entity",
    "async_edit_entity",
    "edit_relation",
    "async_edit_relation",
    "merge_entities",
    "async_merge_entities",
    "delete_by_doc_id",
    "async_delete_by_doc_id",
]
