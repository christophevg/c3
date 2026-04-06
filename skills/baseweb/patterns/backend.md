# Backend Patterns

Patterns for Python backend development in Baseweb projects.

## API Resources

### Collection + Item Pattern

Use two resource classes: one for the collection, one for individual items.

```python
from flask_restful import Resource
from module_name.web import server
import logging

logger = logging.getLogger(__name__)

class MyItems(Resource):
    """Collection endpoint for items."""
    
    @server.authenticated("app.myitems.list")
    def get(self):
        """List all items."""
        try:
            items = get_items_from_db()
            return {"items": items}, 200
        except Exception as e:
            logger.error(f"Error fetching items: {e}")
            return {"error": str(e)}, 500
    
    @server.authenticated("app.myitems.create")
    def post(self):
        """Create a new item."""
        data = server.request.get_json()
        try:
            item = create_item(data)
            return item, 201
        except ValidationError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            return {"error": "Internal server error"}, 500


class MyItem(Resource):
    """Single item endpoint."""
    
    @server.authenticated("app.myitem.get")
    def get(self, item_id):
        """Get a single item by ID."""
        try:
            item = get_item(item_id)
            if not item:
                return {"error": "Not found"}, 404
            return item, 200
        except Exception as e:
            logger.error(f"Error fetching item {item_id}: {e}")
            return {"error": "Internal server error"}, 500
    
    @server.authenticated("app.myitem.update")
    def put(self, item_id):
        """Update an item."""
        data = server.request.get_json()
        try:
            item = update_item(item_id, data)
            return item, 200
        except NotFoundError:
            return {"error": "Not found"}, 404
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}")
            return {"error": "Internal server error"}, 500
    
    @server.authenticated("app.myitem.delete")
    def delete(self, item_id):
        """Delete an item."""
        try:
            delete_item(item_id)
            return {}, 204
        except NotFoundError:
            return {"error": "Not found"}, 404


# Register endpoints with unique names
server.api.add_resource(MyItems, "/api/my-items", endpoint="api.my-items")
server.api.add_resource(MyItem, "/api/my-items/<int:item_id>", endpoint="api.my-items.item")
```

### Endpoint Naming Convention

Create endpoint names from the path:
- Remove leading slashes
- Replace slashes with dots
- `/api/my-items` → `api.my-items`
- `/api/my-items/<id>` → `api.my-items.item`

```python
# Good: Clear endpoint names
server.api.add_resource(Users, "/api/users", endpoint="api.users")
server.api.add_resource(User, "/api/users/<int:user_id>", endpoint="api.users.user")

# Bad: Missing endpoint names causes collisions
server.api.add_resource(Users, "/api/users")  # Ambiguous!
```

## Authentication

### Using the Decorator

```python
from module_name.web import server

class MyResource(Resource):
    
    @server.authenticated("app.myresource.get")
    def get(self):
        """Protected GET endpoint."""
        return {"data": "value"}
    
    @server.authenticated("app.myresource.create")
    def post(self):
        """Protected POST endpoint."""
        data = server.request.get_json()
        return create_resource(data), 201
```

### Scope Naming Convention

Use a consistent scope naming pattern:
- `app.resource.action` for application-level permissions
- `ui.page.action` for UI page permissions

Examples:
- `app.users.list` - List users
- `app.users.create` - Create user
- `app.user.get` - Get single user
- `app.user.update` - Update user
- `app.user.delete` - Delete user

## Exception Handling

### Custom Exceptions

```python
class MyError(Exception):
    """Base exception for my module."""
    pass

class NotFoundError(MyError):
    """Raised when a resource cannot be found."""
    pass

class ValidationError(MyError):
    """Raised when validation fails."""
    pass

class AuthenticationError(MyError):
    """Raised when authentication fails."""
    pass
```

### Graceful Error Handling

```python
from flask_restful import Resource
from module_name.web import server
import logging
import traceback

logger = logging.getLogger(__name__)

class MyResource(Resource):
    
    @server.authenticated("app.myresource.get")
    def get(self, resource_id):
        try:
            resource = get_resource(resource_id)
            if not resource:
                raise NotFoundError(f"Resource {resource_id} not found")
            return resource, 200
        
        except NotFoundError as e:
            logger.warning(f"Not found: {e}")
            return {"error": str(e)}, 404
        
        except ValidationError as e:
            logger.warning(f"Validation failed: {e}")
            return {"error": str(e)}, 400
        
        except AuthenticationError as e:
            logger.warning(f"Authentication failed: {e}")
            return {"error": "Unauthorized"}, 401
        
        except MyError as e:
            logger.error(f"Application error: {e}\n{traceback.format_exc()}")
            return {"error": str(e)}, 500
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            return {"error": "An unexpected error occurred"}, 500
```

## Socket.IO Handlers

### Event Handlers

```python
from baseweb import server
import logging

logger = logging.getLogger(__name__)

@server.socketio.on("connect")
def on_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {server.request.sid}")

@server.socketio.on("disconnect")
def on_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {server.request.sid}")

@server.socketio.on("my_event")
def on_my_event(data):
    """Handle custom event."""
    logger.debug(f"Received my_event: {data}")
    
    # Process the data
    result = process_event(data)
    
    # Option 1: Emit to all clients
    server.socketio.emit("event_result", result)
    
    # Option 2: Emit to specific room
    # server.socketio.emit("event_result", result, room=server.request.sid)
    
    # Option 3: Return to sender only
    return {"status": "success", "data": result}
```

### Room-Based Events

```python
from baseweb import server

@server.socketio.on("join_room")
def on_join_room(data):
    """Join a specific room for targeted updates."""
    room = data.get("room")
    from flask_socketio import join_room
    join_room(room)
    logger.info(f"Client {server.request.sid} joined room {room}")

@server.socketio.on("leave_room")
def on_leave_room(data):
    """Leave a room."""
    room = data.get("room")
    from flask_socketio import leave_room
    leave_room(room)
    logger.info(f"Client {server.request.sid} left room {room}")

# Emit to a specific room
server.socketio.emit("room_update", data, room="my_room")
```

## Request Handling

### Getting Request Data

```python
from module_name.web import server

class MyResource(Resource):
    
    def post(self):
        # JSON body
        data = server.request.get_json()
        
        # Query parameters
        page = server.request.args.get("page", 1, type=int)
        per_page = server.request.args.get("per_page", 20, type=int)
        
        # Headers
        content_type = server.request.headers.get("Content-Type")
        
        # Files
        if "file" in server.request.files:
            file = server.request.files["file"]
```

### Response Patterns

```python
# Success with data
return {"items": items, "total": len(items)}, 200

# Created
return new_item, 201

# No content (after delete)
return {}, 204

# Not found
return {"error": "Not found"}, 404

# Validation error
return {"error": "Invalid input", "details": errors}, 400

# Server error
return {"error": "Internal server error"}, 500
```

## Database Integration

### Using with SQLAlchemy

```python
from flask_sqlalchemy import SQLAlchemy
from module_name.web import server

db = SQLAlchemy()

def init_db():
    """Initialize database with app."""
    db.init_app(server)
    with server.app_context():
        db.create_all()

# In models.py
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
```

### Using with MongoDB

```python
from flask_pymongo import PyMongo
from module_name.web import server

mongo = PyMongo(server)

def get_users():
    users = mongo.db.users.find()
    return [{"id": str(u["_id"]), "username": u["username"]} for u in users]
```