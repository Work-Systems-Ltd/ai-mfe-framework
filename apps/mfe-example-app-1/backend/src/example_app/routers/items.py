"""Example CRUD routes for items - demonstrates auth and permission patterns."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from mfe_common.auth.dependencies import get_auth_dependency
from mfe_common.auth.models import UserInfo
from example_app.settings import ExampleAppSettings

router = APIRouter(prefix="/api/items", tags=["items"])

settings = ExampleAppSettings()
get_current_user = get_auth_dependency(settings)


# In-memory store for demo purposes
class Item(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str


_items: dict[str, Item] = {
    "1": Item(id="1", name="Sample Item", description="A sample item for demonstration", owner_id="testuser"),
    "2": Item(id="2", name="Another Item", description="Another demo item", owner_id="admin"),
}


@router.get("")
async def list_items(user: UserInfo = Depends(get_current_user)) -> list[Item]:
    """List all items (authenticated)."""
    return list(_items.values())


@router.get("/{item_id}")
async def get_item(item_id: str, user: UserInfo = Depends(get_current_user)) -> Item:
    """Get a specific item by ID (authenticated)."""
    item = _items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("")
async def create_item(
    name: str,
    description: str,
    user: UserInfo = Depends(get_current_user),
) -> Item:
    """Create a new item (authenticated)."""
    item_id = str(len(_items) + 1)
    item = Item(id=item_id, name=name, description=description, owner_id=user.sub)
    _items[item_id] = item
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: str, user: UserInfo = Depends(get_current_user)) -> dict[str, str]:
    """Delete an item (authenticated, admin only)."""
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
    return {"status": "deleted"}
