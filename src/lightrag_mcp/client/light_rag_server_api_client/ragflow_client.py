"""Convenience helpers for Ragflow API calls."""

import os
from typing import List, Optional

from .api.retrieval import retrieval_retrieval_post
from .client import AuthenticatedClient
from .models.ragflow_retrieval_request import (
    RagflowMetadataCondition,
    RagflowRetrievalRequest,
)
from .models.ragflow_retrieval_response import RagflowRetrievalResponse


def build_ragflow_client(
    base_url: Optional[str] = None, api_key: Optional[str] = None
) -> AuthenticatedClient:
    """Create an authenticated Ragflow API client using environment fallbacks."""

    resolved_base_url = base_url or os.getenv("RAGFLOW_API_BASE")
    resolved_api_key = api_key or os.getenv("RAGFLOW_API_KEY")

    if not resolved_base_url or not resolved_api_key:
        raise RuntimeError("RAGFLOW_API_BASE and RAGFLOW_API_KEY must be set")

    return AuthenticatedClient(
        base_url=resolved_base_url,
        token=resolved_api_key,
        verify_ssl=False,
    )


async def ragflow_retrieve_chunks(
    *,
    client: AuthenticatedClient,
    question: str,
    dataset_ids: Optional[List[str]] = None,
    document_ids: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 30,
    similarity_threshold: float = 0.2,
    vector_similarity_weight: float = 0.3,
    top_k: int = 1024,
    keyword: bool = False,
    highlight: bool = False,
    use_kg: bool = False,
    metadata_condition: Optional[RagflowMetadataCondition] = None,
    cross_languages: Optional[List[str]] = None,
    rerank_id: Optional[str] = None,
) -> RagflowRetrievalResponse:
    """Execute Ragflow retrieval."""

    request = RagflowRetrievalRequest(
        question=question,
        dataset_ids=dataset_ids,
        document_ids=document_ids,
        page=page,
        page_size=page_size,
        similarity_threshold=similarity_threshold,
        vector_similarity_weight=vector_similarity_weight,
        top_k=top_k,
        keyword=keyword,
        highlight=highlight,
        use_kg=use_kg,
        metadata_condition=metadata_condition,
        cross_languages=cross_languages,
        rerank_id=rerank_id,
    )

    return await retrieval_retrieval_post.asyncio(client=client, json_body=request)
