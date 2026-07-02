from flask import Blueprint, render_template_string

placeholder_bp = Blueprint("placeholder", __name__)

PAGES = [
"crm","hr","finance","inventory","orders","customers",
"products","analytics","attendance","tasks","mail",
"reports","settings","ai","sales"
]

for page in PAGES:
    def make_view(name):
        def view():
            return render_template_string(f"""
            <h1>{name.title()}</h1>
            <p>This module is under development.</p>
            <a href="/dashboard">← Dashboard</a>
            """)
        view.__name__ = f"{name}_view"
        return view

    placeholder_bp.add_url_rule(
        f"/{page}",
        endpoint=page,
        view_func=make_view(page)
    )
