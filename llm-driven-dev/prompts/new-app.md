# Prompt: Create a New MFE App

You are generating a new micro-frontend application for the MFE Framework.

## Context

The MFE Framework is a monorepo with these key patterns:
- **Backend**: FastAPI apps using `mfe-backend-common` (Pydantic Settings, mypy strict, Poetry)
- **Frontend**: Vue 3 + Vite + TypeScript strict + Tailwind + shadcn-vue
- **Auth**: Keycloak (JWT via `get_auth_dependency()`)
- **Permissions**: OpenFGA (via `require_permission()` dependency)
- **Registration**: Apps register with the shell on startup via `register_with_shell()`
- **MFE Pattern**: Sub-apps render in iframe within shell, route-based proxy via shell backend

## Parameters

- **APP_NAME**: `{{APP_NAME}}` (e.g., "inventory")
- **APP_DISPLAY_NAME**: `{{APP_DISPLAY_NAME}}` (e.g., "Inventory Manager")
- **APP_PATH_PREFIX**: `/apps/{{APP_NAME}}`
- **DESCRIPTION**: `{{DESCRIPTION}}`

## What to Generate

### Backend (`apps/{{APP_NAME}}/backend/`)
1. `pyproject.toml` - Poetry config depending on `mfe-backend-common`
2. `src/{{APP_NAME_SNAKE}}_app/__init__.py`
3. `src/{{APP_NAME_SNAKE}}_app/settings.py` - Extends `BaseAppSettings`
4. `src/{{APP_NAME_SNAKE}}_app/main.py` - Uses `create_app()`, defines sidebar links, registers with shell
5. `src/{{APP_NAME_SNAKE}}_app/routers/` - API routes with auth
6. `tests/`
7. `tox.ini`
8. `Dockerfile`

### Frontend (`apps/{{APP_NAME}}/frontend/`)
1. `package.json`
2. `vite.config.ts` - Set `base: "/apps/{{APP_NAME}}/"`
3. `tsconfig.json`
4. `src/main.ts` - Listen for `MFE_AUTH_TOKEN` from parent shell
5. `src/App.vue` - Content only, no shell chrome
6. `src/router/index.ts` - Base path `/apps/{{APP_NAME}}/`
7. `src/views/` - App-specific views
8. `Dockerfile`

### Docker Compose
Add two services to `docker-compose.yml`:
- `{{APP_NAME}}-backend`
- `{{APP_NAME}}-frontend`

## Key Patterns to Follow

### Backend main.py pattern:
```python
from mfe_common.app_factory import create_app
from {{app}}_app.settings import {{App}}Settings
from {{app}}_app.routers import your_router

settings = {{App}}Settings()

SIDEBAR_LINKS = [
    {"label": "Section", "path": "/", "sublinks": [
        {"label": "Sub Item", "path": "/sub"},
    ]},
]

app = create_app(settings=settings, sidebar_links=SIDEBAR_LINKS, register_with_shell=True)
app.include_router(your_router.router)
```

### Frontend main.ts pattern (receive auth token from shell):
```typescript
window.addEventListener("message", (event: MessageEvent) => {
  if (event.data?.type === "MFE_AUTH_TOKEN") {
    setTokenProvider(() => event.data.token);
  }
});
window.parent.postMessage({ type: "MFE_REQUEST_TOKEN" }, "*");
```
