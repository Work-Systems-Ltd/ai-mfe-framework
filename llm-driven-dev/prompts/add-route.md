# Prompt: Add a Route to an Existing MFE App

You are adding a new API route and corresponding frontend view to an existing MFE app.

## Context

- **App name**: `{{APP_NAME}}`
- **Route**: `{{ROUTE_PATH}}` (e.g., `/api/reports`)
- **Description**: `{{DESCRIPTION}}`

## Backend Steps

1. Create a new router file at `apps/{{APP_NAME}}/backend/src/{{APP_NAME_SNAKE}}_app/routers/{{ROUTER_NAME}}.py`
2. Follow this pattern:
```python
from fastapi import APIRouter, Depends
from mfe_common.auth.dependencies import get_auth_dependency
from mfe_common.auth.models import UserInfo
from {{APP_NAME_SNAKE}}_app.settings import {{App}}Settings

router = APIRouter(prefix="/api/{{ROUTER_NAME}}", tags=["{{ROUTER_NAME}}"])
settings = {{App}}Settings()
get_current_user = get_auth_dependency(settings)

@router.get("")
async def list_{{ROUTER_NAME}}(user: UserInfo = Depends(get_current_user)):
    ...
```
3. Include the router in `main.py`: `app.include_router({{ROUTER_NAME}}.router)`

## Frontend Steps

1. Create view at `apps/{{APP_NAME}}/frontend/src/views/{{ViewName}}View.vue`
2. Add route to `router/index.ts`
3. Use `apiFetch` from common for API calls with auth headers
4. Update sidebar links in backend `main.py` if needed

## Testing

- Add pytest tests in `apps/{{APP_NAME}}/backend/tests/test_{{ROUTER_NAME}}.py`
- Test both authenticated and unauthenticated access
