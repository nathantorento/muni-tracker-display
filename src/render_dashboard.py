# src/render_dashboard.py

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path


def render_dashboard(entries):
    """Render HTML dashboard from a list of entry dicts."""
    
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("muni_dashboard.html")

    now_str = datetime.now().strftime("%I:%M %p")

    html = template.render(
        current_time=now_str,
        entries=entries
    )

    output_path = Path(__file__).resolve().parent.parent / "dashboard.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"Dashboard updated → {output_path}")
