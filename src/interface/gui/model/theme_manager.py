import json
from os import listdir, path
from typing import Optional

from PySide6.QtGui import QPalette

from interface.gui.model.theme import Theme, theme_object_hook
from shared.constants import DefaultPath


class ThemeManager:
    def __init__(self, default_theme: Optional[str] = None) -> None:
        self._default = default_theme or "default"
        self._palettes_dir = DefaultPath.PALETTES_DIR
        self._availables = self._get_available_themes()
        current = self._availables.get(self._default, None)
        if current is None:
            raise ValueError(
                f"Default theme '{self._default}' not found in available themes."
            )
        self._current: tuple[str, Theme] = (self._default, current)

    def _get_available_themes(self) -> dict[str, Theme]:
        files: set[str] = set()
        for file in listdir(self._palettes_dir):
            if file.endswith(".json"):
                files.add(file)

        themes: dict[str, Theme] = dict()
        for file in files:
            theme = self._load_theme(file)
            if theme is None:
                continue
            themes[file[:-5]] = theme
        return themes

    def _load_theme(self, theme_file: str) -> Theme | None:
        theme_path = path.join(self._palettes_dir, theme_file)
        if not path.exists(theme_path):
            return None
        try:
            with open(theme_path, "r") as t:
                loaded = json.load(t, object_hook=theme_object_hook)
            return loaded if isinstance(loaded, Theme) else None

        except Exception:
            return None

    def get_current_theme(self) -> tuple[str, Theme]:
        return self._current

    def get_stylesheet(self) -> str:

        role_to_selector: dict[str, tuple[str, str]] = {
            "Window": ("QWidget", "background-color"),
            "Base": (
                "QLineEdit, QTextEdit, QPlainTextEdit, QAbstractItemView",
                "background-color",
            ),
            "ToolTipBase": ("QToolTip", "background-color"),
            "Button": ("QPushButton", "background-color"),
            "HighlightedText": ("QWidget *", "selection-color"),
            "WindowText": ("QWidget", "color"),
            "Text": ("QLabel, QLineEdit, QTextEdit, QPlainTextEdit", "color"),
            "ButtonText": ("QPushButton", "color"),
            "ToolTipText": ("QToolTip", "color"),
            "PlaceholderText": ("QLineEdit, QTextEdit, QPlainTextEdit", "color"),
            "BrightText": ("QWidget *", "color"),
            "AlternateBase": (
                "QTableView, QHeaderView::section, QListView, QTreeView",
                "background-color",
            ),
            "Highlight": ("QWidget *", "selection-background-color"),
        }

        stylesheet_lines: list[str] = []
        normal: dict[str, str] = self._current[1].palette.normal.__dict__
        disabled: dict[str, str] = self._current[1].palette.disabled.__dict__

        for role, color in normal.items():
            if role == "PlaceholderText":
                stylesheet_lines.append(
                    f"QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder {{ color: {color}; }}"
                )
                continue

            if role == "Link":
                stylesheet_lines.append(
                    f"QLabel, QTextBrowser, QAbstractTextDocumentLayout::a {{ color: {color}; }}"
                )
                continue

            if role == "LinkVisited":
                stylesheet_lines.append(
                    f"QLabel:visited, QTextBrowser:visited, QAbstractTextDocumentLayout::a:visited {{ color: {color}; }}"
                )
                continue

            selector, prop = role_to_selector.get(role, (None, None))
            if selector and prop:
                stylesheet_lines.append(f"{selector} {{{prop}: {color};}}")

        for role, color in disabled.items():
            if role in ("Window", "Link", "LinkVisited"):
                continue
            if role == "PlaceholderText":
                stylesheet_lines.append(
                    f"QLineEdit::placeholder:disabled, QTextEdit::placeholder:disabled, QPlainTextEdit::placeholder:disabled {{ color: {color}; }}"
                )
                continue
            if role == "Text":
                stylesheet_lines.append(
                    f"QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{ color: {color}; }}"
                )
                continue
            selector, prop = role_to_selector.get(role, (None, None))
            if selector and prop:
                stylesheet_lines.append(f"{selector}:disabled {{{prop}: {color};}}")

        return "\n".join(stylesheet_lines)

    def get_palette(self) -> QPalette:

        palette = QPalette()

        for role_name, color_hex in self._current[1].palette.normal.__dict__.items():
            role = getattr(QPalette, role_name, None)
            if role is not None:
                palette.setColor(role, color_hex)

        for role_name, color_hex in self._current[1].palette.disabled.__dict__.items():
            role = getattr(QPalette, role_name, None)
            if role is not None:
                palette.setColor(QPalette.ColorGroup.Disabled, role, color_hex)

        return palette

    def get_themes_options(self) -> list[str]:
        return list(self._availables.keys())

    def set_current_theme(self, theme_name: str) -> bool:
        if theme_name == self._current[0]:
            return False
        theme = self._availables.get(theme_name)
        if theme is None:
            return False
        self._current = (theme_name, theme)
        return True
