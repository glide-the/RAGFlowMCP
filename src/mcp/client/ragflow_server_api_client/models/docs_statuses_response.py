from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docs_statuses_response_statuses import DocsStatusesResponseStatuses


T = TypeVar("T", bound="DocsStatusesResponse")


@_attrs_define
class DocsStatusesResponse:
    """
    Attributes:
        statuses (Union[Unset, DocsStatusesResponseStatuses]):
    """

    statuses: Union[Unset, "DocsStatusesResponseStatuses"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        statuses: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = self.statuses.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docs_statuses_response_statuses import DocsStatusesResponseStatuses

        d = dict(src_dict)
        _statuses = d.pop("statuses", UNSET)
        statuses: Union[Unset, DocsStatusesResponseStatuses]
        if isinstance(_statuses, Unset):
            statuses = UNSET
        else:
            statuses = DocsStatusesResponseStatuses.from_dict(_statuses)

        docs_statuses_response = cls(
            statuses=statuses,
        )

        docs_statuses_response.additional_properties = d
        return docs_statuses_response

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
