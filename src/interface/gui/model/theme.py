from dataclasses import dataclass, fields


@dataclass
class ThemeColors:
    AlternateBase: str
    Base: str
    BrightText: str
    Button: str
    ButtonText: str
    Dark: str
    Highlight: str
    HighlightedText: str
    Light: str
    Link: str
    LinkVisited: str
    Mid: str
    Midlight: str
    PlaceholderText: str
    Shadow: str
    Text: str
    ToolTipBase: str
    ToolTipText: str
    Window: str
    WindowText: str


@dataclass
class ThemePalette:
    disabled: ThemeColors
    normal: ThemeColors


@dataclass
class Theme:
    name: dict[str, str]
    palette: ThemePalette

    def localized_name(self, locale: str = "en_US") -> str:
        if isinstance(self.name, dict):
            return self.name.get(locale) or next(iter(self.name.values()), "")
        return str(self.name)


def theme_object_hook(d: dict):
    color_field_names = {f.name for f in fields(ThemeColors)}
    if color_field_names.issubset(d.keys()):
        return ThemeColors(**{k: d[k] for k in color_field_names})

    if "disabled" in d and "normal" in d:
        return ThemePalette(disabled=d["disabled"], normal=d["normal"])
    if "name" in d and "palette" in d:
        return Theme(name=d["name"], palette=d["palette"])

    return d
