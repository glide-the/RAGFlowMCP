from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ollama_chat_request_options_type_0 import OllamaChatRequestOptionsType0
    from ..models.ollama_message import OllamaMessage


T = TypeVar("T", bound="OllamaChatRequest")


@_attrs_define
class OllamaChatRequest:
    """
    Attributes:
        model (str):
        messages (list['OllamaMessage']):
        stream (Union[Unset, bool]):  Default: True.
        options (Union['OllamaChatRequestOptionsType0', None, Unset]):
        system (Union[None, Unset, str]):
    """

    model: str
    messages: list["OllamaMessage"]
    stream: Union[Unset, bool] = True
    options: Union["OllamaChatRequestOptionsType0", None, Unset] = UNSET
    system: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ollama_chat_request_options_type_0 import OllamaChatRequestOptionsType0

        model = self.model

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        stream = self.stream

        options: Union[None, Unset, dict[str, Any]]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, OllamaChatRequestOptionsType0):
            options = self.options.to_dict()
        else:
            options = self.options

        system: Union[None, Unset, str]
        if isinstance(self.system, Unset):
            system = UNSET
        else:
            system = self.system

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "messages": messages,
            }
        )
        if stream is not UNSET:
            field_dict["stream"] = stream
        if options is not UNSET:
            field_dict["options"] = options
        if system is not UNSET:
            field_dict["system"] = system

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ollama_chat_request_options_type_0 import OllamaChatRequestOptionsType0
        from ..models.ollama_message import OllamaMessage

        d = dict(src_dict)
        model = d.pop("model")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = OllamaMessage.from_dict(messages_item_data)

            messages.append(messages_item)

        stream = d.pop("stream", UNSET)

        def _parse_options(data: object) -> Union["OllamaChatRequestOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = OllamaChatRequestOptionsType0.from_dict(data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OllamaChatRequestOptionsType0", None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        def _parse_system(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        system = _parse_system(d.pop("system", UNSET))

        ollama_chat_request = cls(
            model=model,
            messages=messages,
            stream=stream,
            options=options,
            system=system,
        )

        ollama_chat_request.additional_properties = d
        return ollama_chat_request

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
