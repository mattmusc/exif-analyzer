from .renderers.console import render_console
from .renderers.json import render_json


def emit_summary(summary, args):
    if args.format == "console":
        render_console(summary, args)
        return

    if args.format == "json":
        text = render_json(summary)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            print(text)
        return

    raise ValueError(f"Unknown format: {args.format}")
