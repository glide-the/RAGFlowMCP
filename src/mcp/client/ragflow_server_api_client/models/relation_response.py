from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relation_response_graph_data_type_0 import RelationResponseGraphDataType0


T = TypeVar("T", bound="RelationResponse")


@_attrs_define
class RelationResponse:
    """
    Attributes:
        src_entity (str): Source entity of the relation
        tgt_entity (str): Target entity of the relation
        source_id (Union[None, str]): Source ID of the relation
        graph_data (Union['RelationResponseGraphDataType0', None]): Graph data of the relation
    """

    src_entity: str
    tgt_entity: str
    source_id: Union[None, str]
    graph_data: Union["RelationResponseGraphDataType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.relation_response_graph_data_type_0 import RelationResponseGraphDataType0

        src_entity = self.src_entity

        tgt_entity = self.tgt_entity

        source_id: Union[None, str]
        source_id = self.source_id

        graph_data: Union[None, dict[str, Any]]
        if isinstance(self.graph_data, RelationResponseGraphDataType0):
            graph_data = self.graph_data.to_dict()
        else:
            graph_data = self.graph_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "src_entity": src_entity,
                "tgt_entity": tgt_entity,
                "source_id": source_id,
                "graph_data": graph_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relation_response_graph_data_type_0 import RelationResponseGraphDataType0

        d = dict(src_dict)
        src_entity = d.pop("src_entity")

        tgt_entity = d.pop("tgt_entity")

        def _parse_source_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_id = _parse_source_id(d.pop("source_id"))

        def _parse_graph_data(data: object) -> Union["RelationResponseGraphDataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                graph_data_type_0 = RelationResponseGraphDataType0.from_dict(data)

                return graph_data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RelationResponseGraphDataType0", None], data)

        graph_data = _parse_graph_data(d.pop("graph_data"))

        relation_response = cls(
            src_entity=src_entity,
            tgt_entity=tgt_entity,
            source_id=source_id,
            graph_data=graph_data,
        )

        relation_response.additional_properties = d
        return relation_response

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
