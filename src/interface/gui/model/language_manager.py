import json
import os
from typing import Optional

from shared.constants import DefaultPath


class LanguageManager:
    def __init__(self, default_lang: Optional[str]) -> None:
        self._default = default_lang or "en_US"

        self._locales_dir = DefaultPath.LOCALES_DIR
        if not os.path.exists(self._locales_dir):
            raise ValueError(f"Locales dir '{self._locales_dir}' doesn't exist")

        self._avaliable_languages = self._load_locales()
        if len(self._avaliable_languages) == 0:
            raise ValueError("There are no language files available")

        translation = self._avaliable_languages.get(self._default)
        if translation is None:
            key = list(self._avaliable_languages.keys())[0]
            self._current = self._avaliable_languages[key]
            self._current_key = key
        else:
            self._current = translation
            self._current_key = self._default

    def _load_locales(self) -> dict[str, dict[str, dict]]:
        translations: dict[str, dict[str, dict]] = dict()
        for filename in os.listdir(self._locales_dir):
            if filename.endswith(".json"):
                try:
                    with open(
                        os.path.join(self._locales_dir, filename), "r", encoding="utf-8"
                    ) as fh:
                        translations[filename[:-5]] = json.load(fh)
                except Exception:
                    continue
        return translations

    def set_current_language(self, code: str) -> bool:
        if code == self._current_key:
            return False
        if code not in self._avaliable_languages:
            return False
        self._current = self._avaliable_languages[code]
        self._current_key = code
        return True

    def get_current_language(self) -> tuple[str, str]:
        langs = self._current.get("languages")
        if langs is not None:
            name = langs.get(self._current_key, self._current_key)
            return (self._current_key, str(name))

        return (self._current_key, self._current_key)

    def get_available_languages(self) -> list[tuple[str, str]]:
        lang_codes = list(self._avaliable_languages.keys())
        languages: list[tuple[str, str]] = []

        for code in lang_codes:
            name = self.t(f"languages.{code}")
            languages.append((code, name))

        return languages

    def t(self, key: str) -> str:
        keys = key.split(".")
        d = self._current
        for k in keys:
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return key
        if isinstance(d, str):
            return d

        return key
