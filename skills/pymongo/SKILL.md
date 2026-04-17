---
name: pymongo
description: Use this skill when creating or modifying MongoDB database access code with PyMongo
---

# PyMongo Best Practices

When creating database access code, follow the best practices below:

## Module Structure

Create a database module with:

1. **Custom Exceptions** - Define domain-specific exceptions
2. **Connection Handling** - Environment-based configuration
3. **CRUD Operations** - Functions for Create, Read, Update, Delete
4. **Error Handling** - Graceful error handling with logging

## Connection Pattern

Use environment variables for connection configuration:

```python
import os
import logging
import threading
import traceback
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
  """Base exception for database errors."""
  pass

class ConnectionError(DatabaseError):
  """Raised when connection fails."""
  pass

# Singleton for connection pooling (thread-safe)
_client = None
_client_lock = threading.Lock()

def get_mongodb_uri():
  """Get MongoDB URI from environment or default."""
  return os.environ.get("MONGODB_URI", "mongodb://localhost:27017/kookiecooky")

def get_database_name(uri=None):
  """Extract database name from MongoDB URI."""
  from urllib.parse import urlparse
  if uri is None:
    uri = get_mongodb_uri()
  parsed = urlparse(uri)
  db_name = parsed.path.lstrip('/')
  return db_name if db_name else "kookiecooky"

def get_mongodb_client():
  """Create and return a MongoDB client (thread-safe singleton).

  Uses double-checked locking for thread safety.
  Pool size is configurable via MONGODB_POOL_SIZE env var.
  """
  global _client

  if _client is not None:
    return _client

  with _client_lock:
    # Double-check after acquiring lock
    if _client is not None:
      return _client

    uri = get_mongodb_uri()
    pool_size = int(os.environ.get("MONGODB_POOL_SIZE", "50"))

    try:
      _client = MongoClient(uri, maxPoolSize=pool_size)
      _client.admin.command('ping')  # Test connection
      # SECURITY: Log database name only, not full URI (may contain credentials)
      db_name = get_database_name(uri)
      logger.info(f"Connected to MongoDB database: {db_name}")
      return _client
    except ConnectionFailure as e:
      raise ConnectionError(f"Failed to connect to MongoDB: {e}")

def close_mongodb_client():
  """Close the MongoDB connection (for testing/graceful shutdown)."""
  global _client
  with _client_lock:
    if _client is not None:
      _client.close()
      _client = None
      logger.info("MongoDB connection closed")
```

**Important Security Note**: Never log the full MongoDB URI as it may contain credentials. Always extract and log only the database name.

**Thread Safety**: Always use a lock when implementing singleton patterns. Double-checked locking prevents race conditions when multiple threads try to create connections simultaneously.

## ObjectId Helper Function

Use a helper function to convert string IDs to ObjectId:

```python
from bson.objectid import ObjectId
from bson.errors import InvalidId

class NotFoundError(DatabaseError):
  """Raised when a resource is not found."""
  pass

def _to_object_id(item_id):
  """Convert item_id to ObjectId if needed.

  Args:
    item_id: String or ObjectId

  Returns:
    ObjectId

  Raises:
    NotFoundError: If the ID format is invalid
  """
  if isinstance(item_id, str):
    try:
      return ObjectId(item_id)
    except InvalidId:
      raise NotFoundError(f"Invalid ID: {item_id}")
  return item_id
```

**Important**: Use `bson.errors.InvalidId` instead of broad `Exception` when catching invalid ObjectId conversions.

## CRUD Operations Pattern

Follow this pattern for CRUD operations:

```python
def list_items(client=None):
  """List all items in a collection."""
  try:
    collection = get_collection(client)
    items = []
    for doc in collection.find():
      items.append({
        'id': str(doc['_id']),
        # ... other fields
      })
    return items
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Failed to list items: {e}")

def get_item(item_id, client=None):
  """Get a single item by ID."""
  try:
    collection = get_collection(client)
    item_id = _to_object_id(item_id)

    doc = collection.find_one({'_id': item_id})
    if doc is None:
      raise NotFoundError(f"Item not found: {item_id}")

    return {
      'id': str(doc['_id']),
      # ... other fields
    }
  except NotFoundError:
    raise
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Failed to get item: {e}")

def create_item(item_data, client=None):
  """Create a new item."""
  try:
    collection = get_collection(client)
    doc = {
      # Map item_data to document fields
      'field1': item_data.get('field1'),
      'field2': item_data.get('field2', 'default'),
    }
    result = collection.insert_one(doc)
    return {
      'id': str(result.inserted_id),
      # ... other fields
    }
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Failed to create item: {e}")

def update_item(item_id, item_data, client=None):
  """Update an existing item."""
  try:
    collection = get_collection(client)
    item_id = _to_object_id(item_id)

    update_fields = {k: v for k, v in item_data.items() if v is not None}
    result = collection.update_one(
      {'_id': item_id},
      {'$set': update_fields}
    )

    if result.matched_count == 0:
      raise NotFoundError(f"Item not found: {item_id}")

    return get_item(item_id, client)
  except NotFoundError:
    raise
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Failed to update item: {e}")

def delete_item(item_id, client=None):
  """Delete an item."""
  try:
    collection = get_collection(client)
    item_id = _to_object_id(item_id)

    result = collection.delete_one({'_id': item_id})

    if result.deleted_count == 0:
      raise NotFoundError(f"Item not found: {item_id}")

    return True
  except NotFoundError:
    raise
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Failed to delete item: {e}")
```

## Error Handling

Always follow this exception handling pattern:

1. Import `traceback` for logging
2. Catch specific exceptions first (e.g., `NotFoundError`)
3. Catch `PyMongoError` for database-specific errors
4. Catch generic `Exception` as last resort
5. Log with traceback for debugging
6. Re-raise as domain exceptions

```python
import logging
import traceback
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)

def some_database_operation(id):
  try:
    # ... database operation
    pass
  except NotFoundError:
    # Re-raise domain exceptions
    raise
  except PyMongoError as e:
    logger.error(f"Database error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Operation failed: {e}")
  except Exception as e:
    logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
    raise DatabaseError(f"Unexpected error: {e}")
```

## Testing Database Code

Use `unittest.mock.patch` to mock `get_collection` or `get_mongodb_client`:

```python
from unittest.mock import patch, MagicMock

class TestDatabaseOperations:
  """Tests for database operations."""

  @pytest.fixture(autouse=True)
  def setup_mock_collection(self):
    """Set up mock collection for tests."""
    self.mock_collection = MagicMock()
    self.collection_patcher = patch(
      'myapp.database.get_collection',
      return_value=self.mock_collection
    )
    self.collection_patcher.start()
    yield
    self.collection_patcher.stop()

  def test_list_items_empty(self):
    """Test listing items when collection is empty."""
    self.mock_collection.find.return_value = []

    result = list_items()

    assert result == []
    self.mock_collection.find.assert_called_once()
```

## CLI Integration

When exposing database operations via CLI, use the Fire module:

```python
# In __main__.py
import sys
import logging
import fire

from .database import (
  DatabaseError,
  ConnectionError,
  list_items,
  create_item
)

logger = logging.getLogger(__name__)

def list_items_cli():
  """List all items from database."""
  # Setup logging
  logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

  try:
    items = list_items()
    for item in items:
      print(f"  - {item['title']} (id: {item['id']})")
    return items
  except DatabaseError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

def main():
  """Entry point for CLI."""
  fire.Fire({
    'list': list_items_cli,
    # Add more commands
  })

if __name__ == '__main__':
  main()
```

**Important**: Put database connection calls inside try blocks, not before them. This ensures errors are properly caught by exception handlers.

## Security Considerations

### Regex Injection Prevention

When implementing search functionality with MongoDB `$regex`, **always escape special regex characters** to prevent ReDoS (Regular Expression Denial of Service) attacks:

```python
import re

def list_items(search=None):
  """List items with optional search."""
  query = {}
  if search:
    # SECURITY: Escape regex characters to prevent injection
    escaped_search = re.escape(search)
    query['$or'] = [
      {'title': {'$regex': escaped_search, '$options': 'i'}},
      {'description': {'$regex': escaped_search, '$options': 'i'}}
    ]
  # ... execute query
```

**Why**: Without escaping, users could craft malicious patterns like `.*` to match everything, or complex patterns like `(a+)+$` that cause CPU exhaustion (ReDoS).

### Input Validation

Always validate and sanitize user input before using it in database queries:

- Escape regex characters for text search
- Use marshmallow or similar for request validation
- Validate ObjectId format before queries

## Testing Paginated Endpoints

When testing paginated endpoints, mock the MongoDB cursor chain properly:

```python
def test_paginated_list(self):
  """Test paginated list endpoint."""
  self.mock_cursor = MagicMock()
  self.mock_cursor.skip.return_value = self.mock_cursor
  self.mock_cursor.limit.return_value = self.mock_cursor
  self.mock_cursor.sort.return_value = self.mock_cursor
  self.mock_cursor.__iter__ = lambda self: iter([
    {'_id': ObjectId(), 'title': 'Test'}
  ])

  self.mock_collection.find.return_value = self.mock_cursor
  self.mock_collection.count_documents.return_value = 1

  result = list_items(page=1, per_page=20)

  assert 'data' in result
  assert 'pagination' in result
  assert result['pagination']['total_items'] == 1
```
