from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.entity_response_graph_data_type_0 import EntityResponseGraphDataType0


T = TypeVar("T", bound="EntityResponse")


@_attrs_define
class EntityResponse:
    """
    Attributes:
        entity_name (str): Name of the entity
        source_id (Union[None, str]): Source ID of the entity
        graph_data (Union['EntityResponseGraphDataType0', None]): Graph data of the entity
    """

    entity_name: str
    source_id: Union[None, str]
    graph_data: Union["EntityResponseGraphDataType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.entity_response_graph_data_type_0 import EntityResponseGraphDataType0

        entity_name = self.entity_name

        source_id: Union[None, str]
        source_id = self.source_id

        graph_data: Union[None, dict[str, Any]]
        if isinstance(self.graph_data, EntityResponseGraphDataType0):
            graph_data = self.graph_data.to_dict()
        else:
            graph_data = self.graph_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_name": entity_name,
                "source_id": source_id,
                "graph_data": graph_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.entity_response_graph_data_type_0 import EntityResponseGraphDataType0

        d = dict(src_dict)
        entity_name = d.pop("entity_name")

        def _parse_source_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_id = _parse_source_id(d.pop("source_id"))

        def _parse_graph_data(data: object) -> Union["EntityResponseGraphDataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                graph_data_type_0 = EntityResponseGraphDataType0.from_dict(data)

                return graph_data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EntityResponseGraphDataType0", None], data)

        graph_data = _parse_graph_data(d.pop("graph_data"))

        entity_response = cls(
            entity_name=entity_name,
            source_id=source_id,
            graph_data=graph_data,
        )

        entity_response.additional_properties = d
        return entity_response

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
