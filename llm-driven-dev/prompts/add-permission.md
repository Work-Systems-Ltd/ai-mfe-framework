# Prompt: Add Permission Check to an MFE App Route

You are adding a fine-grained permission check to an existing route using OpenFGA.

## Context

- **App**: `{{APP_NAME}}`
- **Route**: `{{ROUTE_PATH}}`
- **Relation**: `{{RELATION}}` (e.g., "can_view", "can_edit")
- **Object type**: `{{OBJECT_TYPE}}` (e.g., "resource", "document")

## Steps

### 1. Update OpenFGA Model (if new type/relation)

Edit `apps/permissions/openfga/model.fga` to add your new type or relation:
```
type {{OBJECT_TYPE}}
  relations
    define viewer: [user, organization#member]
    define editor: [user, organization#admin]
    define can_view: viewer or editor
    define can_edit: editor
```

### 2. Add Permission Check to Route

Use the `require_permission` dependency from `mfe_common.permissions.dependencies`:

```python
from mfe_common.permissions.dependencies import require_permission

@router.get(
    "/{{ROUTE_PATH}}/{id}",
    dependencies=[Depends(require_permission("{{RELATION}}", "{{OBJECT_TYPE}}", settings, get_current_user))],
)
async def get_item(id: str, user: UserInfo = Depends(get_current_user)):
    ...
```

### 3. Seed Development Tuples

Add tuples to `apps/permissions/openfga/tuples.json`:
```json
{
  "user": "user:testuser",
  "relation": "viewer",
  "object": "{{OBJECT_TYPE}}:sample-1"
}
```

### 4. Frontend Permission Check (optional)

Use `usePermissions` composable for UI-level checks:
```typescript
import { usePermissions } from "@common/composables/usePermissions";
const { check } = usePermissions("/apps/permissions");
const canEdit = await check("can_edit", "{{OBJECT_TYPE}}:item-1");
```
