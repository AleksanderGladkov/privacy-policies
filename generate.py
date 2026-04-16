#!/usr/bin/env python3
"""Generate per-app privacy policy HTML pages from apps.yaml + template.html."""

import yaml
from jinja2 import Template
from pathlib import Path


DEFAULTS = {
    "uses_common_sdks": True,
    "has_billing": True,
    "permissions": [],
    "extra_sdks": [],
    "on_device_processing": [],
    "external_apis": [],
}

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policies — Aleksandr Gladkov</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 720px; margin: 0 auto; padding: 2rem 1rem; line-height: 1.6; color: #222; }
        h1 { font-size: 1.8rem; }
        a { color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { padding-left: 1.5rem; }
        li { margin: 0.5rem 0; }
    </style>
</head>
<body>
    <h1>Privacy Policies</h1>
    <p>Privacy policies for apps by {{ developer_name }}.</p>
    <ul>
{% for app in apps %}
        <li><a href="{{ app.slug }}.html">{{ app.display_name }}</a></li>
{% endfor %}
    </ul>
</body>
</html>
"""


def main():
    root = Path(__file__).parent

    with open(root / "apps.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    with open(root / "template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    developer = config["developer"]
    common_sdks = config.get("common_sdks", [])
    apps = config.get("apps", {})

    index_apps = []

    for slug, app_config in apps.items():
        # Apply defaults for optional fields
        app = dict(DEFAULTS, **app_config)

        html = template.render(
            app=app,
            developer=developer,
            common_sdks=common_sdks,
        )

        out_path = root / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  Generated {out_path.name}")

        index_apps.append({"slug": slug, "display_name": app["display_name"]})

    # Generate index page
    index_template = Template(INDEX_TEMPLATE)
    index_html = index_template.render(
        developer_name=developer["name"],
        apps=index_apps,
    )
    index_path = root / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"  Generated {index_path.name}")

    print(f"\nDone — {len(index_apps)} app(s) + index.html")


if __name__ == "__main__":
    main()
