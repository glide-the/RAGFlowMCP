from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merge_entities_request_merge_strategy_type_0 import (
        MergeEntitiesRequestMergeStrategyType0,
    )


T = TypeVar("T", bound="MergeEntitiesRequest")


@_attrs_define
class MergeEntitiesRequest:
    """
    Attributes:
        source_entities (list[str]): List of source entities to merge
        target_entity (str): Name of the target entity after merging
        merge_strategy (Union['MergeEntitiesRequestMergeStrategyType0', None, Unset]): Merge strategy for properties
            ('max', 'min', 'concat', 'first', 'last'). Example: {"description": "concat", "weight": "max"}
    """

    source_entities: list[str]
    target_entity: str
    merge_strategy: Union["MergeEntitiesRequestMergeStrategyType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.merge_entities_request_merge_strategy_type_0 import (
            MergeEntitiesRequestMergeStrategyType0,
        )

        source_entities = self.source_entities

        target_entity = self.target_entity

        merge_strategy: Union[None, Unset, dict[str, Any]]
        if isinstance(self.merge_strategy, Unset):
            merge_strategy = UNSET
        elif isinstance(self.merge_strategy, MergeEntitiesRequestMergeStrategyType0):
            merge_strategy = self.merge_strategy.to_dict()
        else:
            merge_strategy = self.merge_strategy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_entities": source_entities,
                "target_entity": target_entity,
            }
        )
        if merge_strategy is not UNSET:
            field_dict["merge_strategy"] = merge_strategy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merge_entities_request_merge_strategy_type_0 import (
            MergeEntitiesRequestMergeStrategyType0,
        )

        d = dict(src_dict)
        source_entities = cast(list[str], d.pop("source_entities"))

        target_entity = d.pop("target_entity")

        def _parse_merge_strategy(
            data: object,
        ) -> Union["MergeEntitiesRequestMergeStrategyType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                merge_strategy_type_0 = MergeEntitiesRequestMergeStrategyType0.from_dict(data)

                return merge_strategy_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MergeEntitiesRequestMergeStrategyType0", None, Unset], data)

        merge_strategy = _parse_merge_strategy(d.pop("merge_strategy", UNSET))

        merge_entities_request = cls(
            source_entities=source_entities,
            target_entity=target_entity,
            merge_strategy=merge_strategy,
        )

        merge_entities_request.additional_properties = d
        return merge_entities_request

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
