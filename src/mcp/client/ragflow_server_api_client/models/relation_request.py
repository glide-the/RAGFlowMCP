from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RelationRequest")


@_attrs_define
class RelationRequest:
    """
    Attributes:
        description (str): Description of the relation
        keywords (str): Keywords of the relation
        source_id (Union[None, str]): Source ID of the relation
        weight (Union[None, float]): Weight of the relation
    """

    description: str
    keywords: str
    source_id: Union[None, str]
    weight: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        keywords = self.keywords

        source_id: Union[None, str]
        source_id = self.source_id

        weight: Union[None, float]
        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "keywords": keywords,
                "source_id": source_id,
                "weight": weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        keywords = d.pop("keywords")

        def _parse_source_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_id = _parse_source_id(d.pop("source_id"))

        def _parse_weight(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        weight = _parse_weight(d.pop("weight"))

        relation_request = cls(
            description=description,
            keywords=keywords,
            source_id=source_id,
            weight=weight,
        )

        relation_request.additional_properties = d
        return relation_request

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
