---
name: baseweb-best-practices
description: Use this skill any time when creating code using Baseweb
---

# Baseweb Best Practices

When creating code using the Baseweb framework, use the base practices in the sections below.

## Backend

The following subsections are important when creating Python code for the backend part of Baseweb pages.

### Registering Vue Components

Register Vue components so they are loaded by the frontend:

```python
import os
from modulename.web import server

server.register_component("mycomponent.js", os.path.dirname(__file__))
```

### Creating API Resources

When creating FlaskRESTful resources, use one class to represent the collection of the resource and one class to represent the individual items. Add all required HTTP methods on those classes.

#### Example

```python
class MyItems(Resource):
  def get(self):
    # return a list of items, probably matching criteria and applying paging
  
  def post(self):
    # create a new item

classs MyItem(Resource):
  def get(self, id):
    # return item with id
  
  def put(self, id):
    # update item with id
  
  def delete(self, id):
    # delete item with is
```

### Registering API Endpoint Resources

When adding a FlaskRESTful resource to the api object, add the optional `endpoint` argument. This avoids name collisions. Create the name from the path of the endpoint, removing any leading slashes and replacing all other slashes by dots, e.g. a resource added on path "/api/my-api-endpoint" gets a name "api.my-api-endpoint".

#### Example

```python
class MyAPIEndPoint(Resource):
  def get(self):
    # logic to provide data goes here
    data = {}
    return data

server.api.add_resource(MyAPIEndPoint, "/api/my-api-endpoint", endpoint="api.my-api-endpoint")
```

### Authentication Decorator

Use `@server.authenticated("permission.name")` to protect endpoints:

```python
class MyAPIEndPoint(Resource):
  @server.authenticated("app.myendpoint.get")
  def get(self):
    return {"data": "value"}
```

### Exception Handling

Use custom exceptions for domain-specific errors and handle them gracefully in endpoints:

```python
class MyError(Exception):
  """Base exception for my module."""
  pass

class NotFoundError(MyError):
  """Raised when a resource cannot be found."""
  pass

class MyResource(Resource):
  @server.authenticated("app.myresource.get")
  def get(self, id):
    try:
      data = get_data(id)
      return data
    except NotFoundError as e:
      logger.warning(f"Resource not found: {id}")
      return {"error": str(e)}, 404
    except MyError as e:
      logger.error(f"Error: {e}\n{traceback.format_exc()}")
      return {"error": str(e)}, 500
    except Exception as e:
      logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
      return {"error": "An unexpected error occurred"}, 500
```

## Frontend

The following subsections are important when creating Vue/Vuetify code for the frontend part of Baseweb pages.

### Navigation

The Vue component has the typical Vue structure, with one additional property `navigation` with the configuration for inserting the page in the navigation bar.

It contains the following configuration properties

* `section` is the name of a previously defined menu section that can hold pages. If set to `null` the page is added to the root of the navigation menu.
* `icon` is the name of a Material Design icon
* `text` is the text label show in the menu
* `path` is the path to the page in the location bar
* `index` is the order in the navigation menu. Each page should have its own, unique index number.

### Example

```javascript
  navigation: {
    section: null,
    icon: "home",
    text: "text label",
    path: "/path",
    index: 2 
  }  
```

### The global Navigation object

A page is added to the navigation by adding the Vue component to the global `Navigation` object:

```javascript
Navigation.add(MyPage);
```

To create a section use `add_section` with an object similar to the `navigation` section in the Vue component.

```javascript
Navigation.add_section({
  name: "section name", // to be used when adding pages to a section
  icon: "section icon",
  text: "section text",
  index: 5
});
```

### Registering Routes to Pages on the Backend

Every page, added to the `Navigation` in the frontend, also needs to be registered on the backend to ensure its route also provides the application when requested directly. To ensure proper routing every registration of a page component should include its route:

### Example

Given a frontend page component called `mypage.js`, with a `path` property:

```javascript
  navigation: {
    section: null,
    icon: "article",
    text: "My Page",
    path: "/mypage",
    index: 2 
  }  
```

On the backend, when registering the page, the route should also be included:

```python
HERE = os.path.dirname(__file__)
server.register_component("mycomponent.js", HERE, route="/mypage" )
```

### Vuex Store Module Pattern

Register a Vuex store module for page-specific state:

```javascript
store.registerModule("MyModule", {
  state: {
    items: [],
    selectedItem: null,
    loading: false
  },
  mutations: {
    setItems: function(state, items) {
      state.items = items;
    },
    setSelectedItem: function(state, item) {
      state.selectedItem = item;
    },
    setLoading: function(state, loading) {
      state.loading = loading;
    }
  },
  getters: {
    items: function(state) {
      return state.items;
    },
    selectedItem: function(state) {
      return state.selectedItem;
    },
    loading: function(state) {
      return state.loading;
    }
  }
});
```

### Socket.IO Event Listeners

Listen for server-sent events:

```javascript
socket.on("log", function(msg) {
  store.commit("log", msg);
});
```

### AJAX Pattern with jQuery

Make API calls and handle responses:

```javascript
$.ajax({
  url: "/api/my-endpoint",
  type: "get",
  success: function(response) {
    store.commit("setItems", response);
  },
  error: function(response) {
    app.$notify({
      group: "notifications",
      title: "Error",
      text: "Failed to load data: " + response.responseText,
      type: "error",
      duration: 5000
    });
  }
});
```

## Cross-Backend/Frontend Topics

- **Frontend sync**: When changing API responses, always check and update corresponding frontend code in `.js` files.
