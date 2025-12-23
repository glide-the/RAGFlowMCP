from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ollama_generate_request_options_type_0 import OllamaGenerateRequestOptionsType0


T = TypeVar("T", bound="OllamaGenerateRequest")


@_attrs_define
class OllamaGenerateRequest:
    """
    Attributes:
        model (str):
        prompt (str):
        system (Union[None, Unset, str]):
        stream (Union[Unset, bool]):  Default: False.
        options (Union['OllamaGenerateRequestOptionsType0', None, Unset]):
    """

    model: str
    prompt: str
    system: Union[None, Unset, str] = UNSET
    stream: Union[Unset, bool] = False
    options: Union["OllamaGenerateRequestOptionsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ollama_generate_request_options_type_0 import OllamaGenerateRequestOptionsType0

        model = self.model

        prompt = self.prompt

        system: Union[None, Unset, str]
        if isinstance(self.system, Unset):
            system = UNSET
        else:
            system = self.system

        stream = self.stream

        options: Union[None, Unset, dict[str, Any]]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, OllamaGenerateRequestOptionsType0):
            options = self.options.to_dict()
        else:
            options = self.options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "prompt": prompt,
            }
        )
        if system is not UNSET:
            field_dict["system"] = system
        if stream is not UNSET:
            field_dict["stream"] = stream
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ollama_generate_request_options_type_0 import OllamaGenerateRequestOptionsType0

        d = dict(src_dict)
        model = d.pop("model")

        prompt = d.pop("prompt")

        def _parse_system(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        system = _parse_system(d.pop("system", UNSET))

        stream = d.pop("stream", UNSET)

        def _parse_options(data: object) -> Union["OllamaGenerateRequestOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = OllamaGenerateRequestOptionsType0.from_dict(data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OllamaGenerateRequestOptionsType0", None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        ollama_generate_request = cls(
            model=model,
            prompt=prompt,
            system=system,
            stream=stream,
            options=options,
        )

        ollama_generate_request.additional_properties = d
        return ollama_generate_request

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
