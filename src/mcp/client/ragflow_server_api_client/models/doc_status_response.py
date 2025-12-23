from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.doc_status import DocStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doc_status_response_metadata_type_0 import DocStatusResponseMetadataType0


T = TypeVar("T", bound="DocStatusResponse")


@_attrs_define
class DocStatusResponse:
    """
    Attributes:
        id (str):
        content_summary (str):
        content_length (int):
        status (DocStatus): Document processing status
        created_at (str):
        updated_at (str):
        file_path (str):
        chunks_count (Union[None, Unset, int]):
        error (Union[None, Unset, str]):
        metadata (Union['DocStatusResponseMetadataType0', None, Unset]):
    """

    id: str
    content_summary: str
    content_length: int
    status: DocStatus
    created_at: str
    updated_at: str
    file_path: str
    chunks_count: Union[None, Unset, int] = UNSET
    error: Union[None, Unset, str] = UNSET
    metadata: Union["DocStatusResponseMetadataType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.doc_status_response_metadata_type_0 import DocStatusResponseMetadataType0

        id = self.id

        content_summary = self.content_summary

        content_length = self.content_length

        status = self.status.value

        created_at = self.created_at

        updated_at = self.updated_at

        file_path = self.file_path

        chunks_count: Union[None, Unset, int]
        if isinstance(self.chunks_count, Unset):
            chunks_count = UNSET
        else:
            chunks_count = self.chunks_count

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, DocStatusResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "content_summary": content_summary,
                "content_length": content_length,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "file_path": file_path,
            }
        )
        if chunks_count is not UNSET:
            field_dict["chunks_count"] = chunks_count
        if error is not UNSET:
            field_dict["error"] = error
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doc_status_response_metadata_type_0 import DocStatusResponseMetadataType0

        d = dict(src_dict)
        id = d.pop("id")

        content_summary = d.pop("content_summary")

        content_length = d.pop("content_length")

        status = DocStatus(d.pop("status"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        file_path = d.pop("file_path")

        def _parse_chunks_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        chunks_count = _parse_chunks_count(d.pop("chunks_count", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_metadata(data: object) -> Union["DocStatusResponseMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = DocStatusResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DocStatusResponseMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        doc_status_response = cls(
            id=id,
            content_summary=content_summary,
            content_length=content_length,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            file_path=file_path,
            chunks_count=chunks_count,
            error=error,
            metadata=metadata,
        )

        doc_status_response.additional_properties = d
        return doc_status_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
