"""Example MFE app entry point.

Demonstrates:
- Using create_app() factory from mfe-backend-common
- Registering with the shell on startup
- Defining sidebar links
- Auth-protected routes
"""

from mfe_common.app_factory import create_app
from example_app.routers import items
from example_app.settings import ExampleAppSettings

settings = ExampleAppSettings()

# Define sidebar links for shell registration
SIDEBAR_LINKS = [
    {
        "label": "Items",
        "path": "/",
        "icon": "package",
        "sublinks": [
            {"label": "All Items", "path": "/items"},
            {"label": "Create Item", "path": "/items/new"},
        ],
    },
]

app = create_app(
    settings=settings,
    sidebar_links=SIDEBAR_LINKS,
    register_with_shell=True,
)

app.include_router(items.router)
