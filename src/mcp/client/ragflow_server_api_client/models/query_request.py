from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.query_request_mode import QueryRequestMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_request_conversation_history_type_0_item import QueryRequestConversationHistoryType0Item


T = TypeVar("T", bound="QueryRequest")


@_attrs_define
class QueryRequest:
    """
    Attributes:
        query (str): The query text
        mode (Union[Unset, QueryRequestMode]): Query mode Default: QueryRequestMode.HYBRID.
        only_need_context (Union[None, Unset, bool]): If True, only returns the retrieved context without generating a
            response.
        only_need_prompt (Union[None, Unset, bool]): If True, only returns the generated prompt without producing a
            response.
        response_type (Union[None, Unset, str]): Defines the response format. Examples: 'Multiple Paragraphs', 'Single
            Paragraph', 'Bullet Points'.
        top_k (Union[None, Unset, int]): Number of top items to retrieve. Represents entities in 'local' mode and
            relationships in 'global' mode.
        max_token_for_text_unit (Union[None, Unset, int]): Maximum number of tokens allowed for each retrieved text
            chunk.
        max_token_for_global_context (Union[None, Unset, int]): Maximum number of tokens allocated for relationship
            descriptions in global retrieval.
        max_token_for_local_context (Union[None, Unset, int]): Maximum number of tokens allocated for entity
            descriptions in local retrieval.
        hl_keywords (Union[None, Unset, list[str]]): List of high-level keywords to prioritize in retrieval.
        ll_keywords (Union[None, Unset, list[str]]): List of low-level keywords to refine retrieval focus.
        conversation_history (Union[None, Unset, list['QueryRequestConversationHistoryType0Item']]): Stores past
            conversation history to maintain context. Format: [{'role': 'user/assistant', 'content': 'message'}].
        history_turns (Union[None, Unset, int]): Number of complete conversation turns (user-assistant pairs) to
            consider in the response context.
    """

    query: str
    mode: Union[Unset, QueryRequestMode] = QueryRequestMode.HYBRID
    only_need_context: Union[None, Unset, bool] = UNSET
    only_need_prompt: Union[None, Unset, bool] = UNSET
    response_type: Union[None, Unset, str] = UNSET
    top_k: Union[None, Unset, int] = UNSET
    max_token_for_text_unit: Union[None, Unset, int] = UNSET
    max_token_for_global_context: Union[None, Unset, int] = UNSET
    max_token_for_local_context: Union[None, Unset, int] = UNSET
    hl_keywords: Union[None, Unset, list[str]] = UNSET
    ll_keywords: Union[None, Unset, list[str]] = UNSET
    conversation_history: Union[None, Unset, list["QueryRequestConversationHistoryType0Item"]] = UNSET
    history_turns: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        only_need_context: Union[None, Unset, bool]
        if isinstance(self.only_need_context, Unset):
            only_need_context = UNSET
        else:
            only_need_context = self.only_need_context

        only_need_prompt: Union[None, Unset, bool]
        if isinstance(self.only_need_prompt, Unset):
            only_need_prompt = UNSET
        else:
            only_need_prompt = self.only_need_prompt

        response_type: Union[None, Unset, str]
        if isinstance(self.response_type, Unset):
            response_type = UNSET
        else:
            response_type = self.response_type

        top_k: Union[None, Unset, int]
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        max_token_for_text_unit: Union[None, Unset, int]
        if isinstance(self.max_token_for_text_unit, Unset):
            max_token_for_text_unit = UNSET
        else:
            max_token_for_text_unit = self.max_token_for_text_unit

        max_token_for_global_context: Union[None, Unset, int]
        if isinstance(self.max_token_for_global_context, Unset):
            max_token_for_global_context = UNSET
        else:
            max_token_for_global_context = self.max_token_for_global_context

        max_token_for_local_context: Union[None, Unset, int]
        if isinstance(self.max_token_for_local_context, Unset):
            max_token_for_local_context = UNSET
        else:
            max_token_for_local_context = self.max_token_for_local_context

        hl_keywords: Union[None, Unset, list[str]]
        if isinstance(self.hl_keywords, Unset):
            hl_keywords = UNSET
        elif isinstance(self.hl_keywords, list):
            hl_keywords = self.hl_keywords

        else:
            hl_keywords = self.hl_keywords

        ll_keywords: Union[None, Unset, list[str]]
        if isinstance(self.ll_keywords, Unset):
            ll_keywords = UNSET
        elif isinstance(self.ll_keywords, list):
            ll_keywords = self.ll_keywords

        else:
            ll_keywords = self.ll_keywords

        conversation_history: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.conversation_history, Unset):
            conversation_history = UNSET
        elif isinstance(self.conversation_history, list):
            conversation_history = []
            for conversation_history_type_0_item_data in self.conversation_history:
                conversation_history_type_0_item = conversation_history_type_0_item_data.to_dict()
                conversation_history.append(conversation_history_type_0_item)

        else:
            conversation_history = self.conversation_history

        history_turns: Union[None, Unset, int]
        if isinstance(self.history_turns, Unset):
            history_turns = UNSET
        else:
            history_turns = self.history_turns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if only_need_context is not UNSET:
            field_dict["only_need_context"] = only_need_context
        if only_need_prompt is not UNSET:
            field_dict["only_need_prompt"] = only_need_prompt
        if response_type is not UNSET:
            field_dict["response_type"] = response_type
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if max_token_for_text_unit is not UNSET:
            field_dict["max_token_for_text_unit"] = max_token_for_text_unit
        if max_token_for_global_context is not UNSET:
            field_dict["max_token_for_global_context"] = max_token_for_global_context
        if max_token_for_local_context is not UNSET:
            field_dict["max_token_for_local_context"] = max_token_for_local_context
        if hl_keywords is not UNSET:
            field_dict["hl_keywords"] = hl_keywords
        if ll_keywords is not UNSET:
            field_dict["ll_keywords"] = ll_keywords
        if conversation_history is not UNSET:
            field_dict["conversation_history"] = conversation_history
        if history_turns is not UNSET:
            field_dict["history_turns"] = history_turns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_request_conversation_history_type_0_item import QueryRequestConversationHistoryType0Item

        d = dict(src_dict)
        query = d.pop("query")

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, QueryRequestMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = QueryRequestMode(_mode)

        def _parse_only_need_context(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        only_need_context = _parse_only_need_context(d.pop("only_need_context", UNSET))

        def _parse_only_need_prompt(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        only_need_prompt = _parse_only_need_prompt(d.pop("only_need_prompt", UNSET))

        def _parse_response_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response_type = _parse_response_type(d.pop("response_type", UNSET))

        def _parse_top_k(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_max_token_for_text_unit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_token_for_text_unit = _parse_max_token_for_text_unit(d.pop("max_token_for_text_unit", UNSET))

        def _parse_max_token_for_global_context(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_token_for_global_context = _parse_max_token_for_global_context(d.pop("max_token_for_global_context", UNSET))

        def _parse_max_token_for_local_context(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_token_for_local_context = _parse_max_token_for_local_context(d.pop("max_token_for_local_context", UNSET))

        def _parse_hl_keywords(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                hl_keywords_type_0 = cast(list[str], data)

                return hl_keywords_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        hl_keywords = _parse_hl_keywords(d.pop("hl_keywords", UNSET))

        def _parse_ll_keywords(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ll_keywords_type_0 = cast(list[str], data)

                return ll_keywords_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        ll_keywords = _parse_ll_keywords(d.pop("ll_keywords", UNSET))

        def _parse_conversation_history(
            data: object,
        ) -> Union[None, Unset, list["QueryRequestConversationHistoryType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                conversation_history_type_0 = []
                _conversation_history_type_0 = data
                for conversation_history_type_0_item_data in _conversation_history_type_0:
                    conversation_history_type_0_item = QueryRequestConversationHistoryType0Item.from_dict(
                        conversation_history_type_0_item_data
                    )

                    conversation_history_type_0.append(conversation_history_type_0_item)

                return conversation_history_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["QueryRequestConversationHistoryType0Item"]], data)

        conversation_history = _parse_conversation_history(d.pop("conversation_history", UNSET))

        def _parse_history_turns(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        history_turns = _parse_history_turns(d.pop("history_turns", UNSET))

        query_request = cls(
            query=query,
            mode=mode,
            only_need_context=only_need_context,
            only_need_prompt=only_need_prompt,
            response_type=response_type,
            top_k=top_k,
            max_token_for_text_unit=max_token_for_text_unit,
            max_token_for_global_context=max_token_for_global_context,
            max_token_for_local_context=max_token_for_local_context,
            hl_keywords=hl_keywords,
            ll_keywords=ll_keywords,
            conversation_history=conversation_history,
            history_turns=history_turns,
        )

        query_request.additional_properties = d
        return query_request

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
