import sys

from cli.app import run_cli_mode

CLI_MODE_TOKENS = {"cli", "--cli"}
CLI_HINT_TOKENS = {
    "--image",
    "--directory",
    "--output",
    "--format_out",
    "--rgbm_coe",
    "--eef",
    "--exposure",
    "--eblf",
    "--black_level",
    "--esf",
    "--saturation",
}


def run_gui_mode(argv):
    from gui.app import HDRApp
    from gui.fonts.load_font import load_font
    from gui.palette.custom_palette import get_custom_palette

    app = HDRApp(argv)
    font = load_font()
    app.setFont(font)
    app.setPalette(get_custom_palette())
    app.home_screen.show()
    return app.exec()


def should_run_cli(argv):
    if not argv:
        return False

    if argv[0] in CLI_MODE_TOKENS:
        return True

    return any(token in CLI_HINT_TOKENS for token in argv)


def main():
    argv = sys.argv[1:]

    if should_run_cli(argv):
        cli_args = argv[1:] if argv and argv[0] in CLI_MODE_TOKENS else argv
        sys.exit(run_cli_mode(cli_args))

    sys.exit(run_gui_mode(sys.argv))


if __name__ == "__main__":
    main()
