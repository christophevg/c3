# API Patterns

Patterns for creating and managing API endpoints in Baseweb projects.

## Resource Design

### RESTful Naming Convention

| Resource | Path | Endpoint Name | Methods |
|----------|------|---------------|---------|
| Collection | `/api/items` | `api.items` | GET, POST |
| Item | `/api/items/<id>` | `api.items.item` | GET, PUT, DELETE |

### Standard Response Format

```json
// Collection response
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20
}

// Single item response
{
  "id": 1,
  "name": "Item Name",
  "created_at": "2026-04-06T12:00:00Z"
}

// Error response
{
  "error": "Error message",
  "details": {
    "field": "validation error"
  }
}
```

## CRUD Operations

### List (GET Collection)

```python
from flask_restful import Resource
from module_name.web import server
import logging

logger = logging.getLogger(__name__)

class Items(Resource):
    """Collection endpoint for items."""
    
    @server.authenticated("app.items.list")
    def get(self):
        """List items with optional filtering and pagination."""
        try:
            # Query parameters
            page = server.request.args.get("page", 1, type=int)
            per_page = server.request.args.get("per_page", 20, type=int)
            search = server.request.args.get("search", "")
            
            # Get items
            items, total = get_items_paginated(
                page=page,
                per_page=per_page,
                search=search
            )
            
            return {
                "items": items,
                "total": total,
                "page": page,
                "per_page": per_page
            }, 200
        
        except Exception as e:
            logger.error(f"Error listing items: {e}")
            return {"error": "Internal server error"}, 500


server.api.add_resource(Items, "/api/items", endpoint="api.items")
```

### Create (POST Collection)

```python
class Items(Resource):
    
    @server.authenticated("app.items.create")
    def post(self):
        """Create a new item."""
        data = server.request.get_json()
        
        # Validate input
        errors = validate_item_data(data)
        if errors:
            return {"error": "Validation failed", "details": errors}, 400
        
        try:
            item = create_item(data)
            return item, 201
        
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            return {"error": "Internal server error"}, 500
```

### Read (GET Item)

```python
class Item(Resource):
    """Single item endpoint."""
    
    @server.authenticated("app.item.get")
    def get(self, item_id):
        """Get a single item by ID."""
        try:
            item = get_item(item_id)
            if not item:
                return {"error": "Not found"}, 404
            return item, 200
        
        except Exception as e:
            logger.error(f"Error getting item {item_id}: {e}")
            return {"error": "Internal server error"}, 500
```

### Update (PUT Item)

```python
class Item(Resource):
    
    @server.authenticated("app.item.update")
    def put(self, item_id):
        """Update an item."""
        data = server.request.get_json()
        
        # Validate input
        errors = validate_item_data(data, partial=True)
        if errors:
            return {"error": "Validation failed", "details": errors}, 400
        
        try:
            item = update_item(item_id, data)
            if not item:
                return {"error": "Not found"}, 404
            return item, 200
        
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}")
            return {"error": "Internal server error"}, 500
```

### Delete (DELETE Item)

```python
class Item(Resource):
    
    @server.authenticated("app.item.delete")
    def delete(self, item_id):
        """Delete an item."""
        try:
            success = delete_item(item_id)
            if not success:
                return {"error": "Not found"}, 404
            return {}, 204
        
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {e}")
            return {"error": "Internal server error"}, 500
```

## Authentication Scopes

### Scope Naming Convention

Use hierarchical scope names:

```
app.{resource}.{action}
ui.{page}.{action}
```

Examples:
- `app.users.list` - List all users
- `app.users.create` - Create a user
- `app.user.get` - Get single user
- `app.user.update` - Update user
- `app.user.delete` - Delete user
- `ui.dashboard.view` - View dashboard
- `ui.admin.access` - Access admin section

### Multiple Scopes

```python
from functools import wraps

def require_any(*scopes):
    """Decorator that requires any of the specified scopes."""
    def decorator(f):
        @wraps(f)
        @server.authenticated(scopes[0])
        def wrapped(*args, **kwargs):
            # Check if user has any of the scopes
            for scope in scopes:
                if check_user_scope(scope):
                    return f(*args, **kwargs)
            return {"error": "Insufficient permissions"}, 403
        return wrapped
    return decorator

class Items(Resource):
    
    @require_any("app.items.list", "app.items.view")
    def get(self):
        # User needs either scope
        pass
```

## Request Handling

### Query Parameters

```python
class Items(Resource):
    
    def get(self):
        # Required parameter
        search = server.request.args.get("search")
        if not search:
            return {"error": "search parameter required"}, 400
        
        # Optional parameter with default
        page = server.request.args.get("page", 1, type=int)
        per_page = server.request.args.get("per_page", 20, type=int)
        
        # Type conversion
        active = server.request.args.get("active", None, type=lambda v: v.lower() == "true")
        
        # List parameters
        tags = server.request.args.getlist("tag")
```

### Request Body

```python
class Items(Resource):
    
    def post(self):
        # JSON body
        data = server.request.get_json()
        
        if not data:
            return {"error": "JSON body required"}, 400
        
        name = data.get("name")
        email = data.get("email")
```

### File Uploads

```python
class Upload(Resource):
    
    @server.authenticated("app.upload.create")
    def post(self):
        if "file" not in server.request.files:
            return {"error": "No file provided"}, 400
        
        file = server.request.files["file"]
        
        if file.filename == "":
            return {"error": "No file selected"}, 400
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return {"filename": filename}, 201
        
        return {"error": "File type not allowed"}, 400
```

## Response Patterns

### Success Responses

```python
# Collection with pagination
return {
    "items": items,
    "total": total,
    "page": page,
    "per_page": per_page
}, 200

# Single item created
return item, 201

# No content (successful deletion)
return {}, 204
```

### Error Responses

```python
# Not found
return {"error": "Not found"}, 404

# Validation error
return {
    "error": "Validation failed",
    "details": {
        "name": "Name is required",
        "email": "Invalid email format"
    }
}, 400

# Unauthorized
return {"error": "Authentication required"}, 401

# Forbidden
return {"error": "Insufficient permissions"}, 403

# Server error
return {"error": "Internal server error"}, 500
```

## Filtering and Pagination

### Pagination Helper

```python
def paginate(query, page=1, per_page=20):
    """Apply pagination to a query."""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": [item.to_dict() for item in items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

class Items(Resource):
    
    def get(self):
        page = server.request.args.get("page", 1, type=int)
        per_page = server.request.args.get("per_page", 20, type=int)
        
        query = Item.query
        return paginate(query, page, per_page), 200
```

### Filtering

```python
class Items(Resource):
    
    def get(self):
        query = Item.query
        
        # Apply filters
        status = server.request.args.get("status")
        if status:
            query = query.filter(Item.status == status)
        
        category = server.request.args.get("category")
        if category:
            query = query.filter(Item.category == category)
        
        # Search
        search = server.request.args.get("search")
        if search:
            query = query.filter(Item.name.ilike(f"%{search}%"))
        
        # Ordering
        sort = server.request.args.get("sort", "created_at")
        order = server.request.args.get("order", "desc")
        
        if order == "desc":
            query = query.order_by(getattr(Item, sort).desc())
        else:
            query = query.order_by(getattr(Item, sort).asc())
        
        # Pagination
        return paginate(query), 200
```

## Nested Resources

### One-to-Many

```python
# /api/users/<int:user_id>/posts
class UserPosts(Resource):
    
    @server.authenticated("app.posts.list")
    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        posts = get_user_posts(user_id)
        return {"posts": posts}, 200

server.api.add_resource(
    UserPosts, 
    "/api/users/<int:user_id>/posts",
    endpoint="api.users.posts"
)
```

### Many-to-Many

```python
# /api/items/<int:item_id>/tags
class ItemTags(Resource):
    
    @server.authenticated("app.item.tags.list")
    def get(self, item_id):
        item = get_item(item_id)
        if not item:
            return {"error": "Item not found"}, 404
        
        return {"tags": item.tags}, 200
    
    @server.authenticated("app.item.tags.add")
    def post(self, item_id):
        data = server.request.get_json()
        tag_id = data.get("tag_id")
        
        item = get_item(item_id)
        tag = get_tag(tag_id)
        
        if not item or not tag:
            return {"error": "Not found"}, 404
        
        add_tag_to_item(item, tag)
        return {"tag": tag}, 201

server.api.add_resource(
    ItemTags,
    "/api/items/<int:item_id>/tags",
    endpoint="api.items.tags"
)
```

## Batch Operations

### Batch Create

```python
class ItemsBatch(Resource):
    
    @server.authenticated("app.items.batch.create")
    def post(self):
        data = server.request.get_json()
        items_data = data.get("items", [])
        
        if not items_data:
            return {"error": "No items provided"}, 400
        
        created = []
        errors = []
        
        for i, item_data in enumerate(items_data):
            try:
                item = create_item(item_data)
                created.append(item)
            except Exception as e:
                errors.append({"index": i, "error": str(e)})
        
        return {
            "created": created,
            "errors": errors
        }, 201 if not errors else 207  # Multi-status

server.api.add_resource(ItemsBatch, "/api/items/batch", endpoint="api.items.batch")
```

### Batch Delete

```python
class ItemsBatch(Resource):
    
    @server.authenticated("app.items.batch.delete")
    def delete(self):
        data = server.request.get_json()
        ids = data.get("ids", [])
        
        deleted = []
        not_found = []
        
        for item_id in ids:
            if delete_item(item_id):
                deleted.append(item_id)
            else:
                not_found.append(item_id)
        
        return {
            "deleted": deleted,
            "not_found": not_found
        }, 200
```