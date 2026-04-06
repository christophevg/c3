---
name: baseweb
description: Use this skill any time when creating or modifying code in Baseweb projects
triggers:
  - when creating code using Baseweb
  - when creating or modifying Baseweb pages
  - when creating or modifying Baseweb API endpoints
  - when asked to review a Baseweb project
  - when asked to add features to a Baseweb project
  - when debugging issues in Baseweb projects
---

# Baseweb Skill

Comprehensive skill for creating and managing Baseweb-based projects. Provides guidance on project structure, configuration, Vuetify integration, and custom component development.

## Overview

This skill supports:

| Task | Description |
|------|-------------|
| Project Creation | Create new Baseweb projects from minimal templates |
| Feature Development | Develop features in existing Baseweb projects |
| Debugging | Diagnose and resolve Baseweb-specific issues |
| Refactoring | Improve existing code structure and patterns |

## Critical Workflow Note

**NEVER start server instances.** The user controls all server processes.

When testing:
- Ask the user to start servers
- Provide commands like `make run` or `TEST_PAGE=true make run`
- Wait for user confirmation before proceeding with tests

## When to Use This Skill

Use this skill when:
- Creating a new Baseweb project
- Adding pages or components to an existing project
- Creating or modifying API endpoints
- Debugging issues in Baseweb projects
- Refactoring Baseweb code
- Reviewing project structure

## Structure Analysis Behavior

When working with existing projects:

1. **Detect**: Identify current project structure
2. **Compare**: Compare against standard Baseweb structure
3. **Report**: Report any deviations found
4. **Offer**: Present options to user:
   - Option A: Fix deviations to match standard structure
   - Option B: Adopt the different structure as project convention

**Standard Baseweb Structure**:

```
project/
├── module_name/
│   ├── __init__.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── server.py          # Flask app configuration
│   │   └── pages/
│   │       ├── __init__.py
│   │       ├── page1.js       # Vue component (frontend)
│   │       └── page1.py       # Backend handlers
│   └── api/
│       ├── __init__.py
│       └── resources.py       # API resource definitions
├── static/                     # Static assets
├── templates/                  # HTML templates
├── config.py                   # Configuration
└── requirements.txt
```

## Vuetify Integration

This skill handles Baseweb-specific structure and delegates pure Vuetify specifics to the Vuetify skill.

| Baseweb Skill Handles | Vuetify Skill Handles |
|----------------------|----------------------|
| Page structure | Component selection |
| Navigation registration | Component props |
| API integration | Styling patterns |
| Vuex store modules | Layout options |
| Socket.IO events | Accessibility |

## Pattern Files

This skill includes detailed patterns in separate files:

- `patterns/project-setup.md` - Project initialization and configuration
- `patterns/backend.md` - Backend Python patterns
- `patterns/frontend.md` - Frontend Vue/Vuetify patterns
- `patterns/api.md` - API resource patterns
- `patterns/navigation.md` - Navigation configuration patterns

## Agent Collaboration

The Baseweb skill collaborates with specialized agents:

| Agent | Collaboration Point |
|-------|---------------------|
| API Architect | Backend API design decisions |
| Python Developer | Backend implementation details |
| UX/UI Designer | Page layouts and user flow |
| Vuetify Skill | Frontend component specifics |

## Quick Reference

### Creating a New Page

1. Create `pagename.js` in `pages/` folder with Vue component
2. Create `pagename.py` in `pages/` folder for backend registration
3. Add navigation configuration to the Vue component
4. Register component with route on backend

### Creating an API Endpoint

1. Create resource class(es) extending `Resource`
2. Implement HTTP methods (GET, POST, PUT, DELETE)
3. Register with `server.api.add_resource()` and `endpoint` argument
4. Add authentication with `@server.authenticated()` decorator

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Page not loading | Missing route in `register_component()` | Add `route="/path"` parameter |
| API 404 | Missing `endpoint` argument | Add `endpoint="api.name"` |
| Navigation duplicate | Same `index` value | Ensure unique `index` values |
| Component not found | Not registered in `Navigation` | Add `Navigation.add(Comp)` |

## Templates

This skill includes code templates for common Baseweb patterns:

| Template | Purpose |
|----------|---------|
| `templates/page.js.template` | Vue page component with navigation |
| `templates/page.py.template` | Backend page registration |
| `templates/resource.py.template` | API resource classes (collection + item) |
| `templates/vuex-module.js.template` | Vuex store module |

## Usage Examples

### Creating a New Page

```python
# backend: pages/users.py
import os
from myapp.web import server

HERE = os.path.dirname(__file__)
server.register_component("users.js", HERE, route="/users")
```

```javascript
// frontend: pages/users.js
const UsersPage = {
  navigation: {
    section: "admin",
    icon: "people",
    text: "Users",
    path: "/admin/users",
    index: 10
  },
  template: `
<Page>
  <v-container>
    <v-data-table :headers="headers" :items="users" :loading="loading">
      <template v-slot:item.actions="{ item }">
        <v-btn icon @click="editUser(item)"><v-icon>edit</v-icon></v-btn>
        <v-btn icon @click="deleteUser(item)"><v-icon>delete</v-icon></v-btn>
      </template>
    </v-data-table>
  </v-container>
</Page>
  `,
  data: function() {
    return {
      headers: [
        { text: "ID", value: "id" },
        { text: "Username", value: "username" },
        { text: "Actions", value: "actions", sortable: false }
      ],
      users: [],
      loading: false
    };
  },
  mounted: function() {
    this.loadUsers();
  },
  methods: {
    loadUsers: function() {
      this.loading = true;
      $.ajax({
        url: "/api/users",
        success: (response) => {
          this.users = response.users;
          this.loading = false;
        }
      });
    }
  }
};

Navigation.add(UsersPage);
```

### Creating an API Resource

```python
# backend: api/users.py
from flask_restful import Resource
from myapp.web import server
import logging

logger = logging.getLogger(__name__)

class Users(Resource):
    @server.authenticated("app.users.list")
    def get(self):
        return {"users": get_users()}, 200

    @server.authenticated("app.users.create")
    def post(self):
        data = server.request.get_json()
        return create_user(data), 201

class User(Resource):
    @server.authenticated("app.user.get")
    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            return {"error": "Not found"}, 404
        return user, 200

    @server.authenticated("app.user.update")
    def put(self, user_id):
        data = server.request.get_json()
        return update_user(user_id, data), 200

    @server.authenticated("app.user.delete")
    def delete(self, user_id):
        delete_user(user_id)
        return {}, 204

server.api.add_resource(Users, "/api/users", endpoint="api.users")
server.api.add_resource(User, "/api/users/<int:user_id>", endpoint="api.users.user")
```

## Validation

This skill has been validated against:
- **nationofpositivity** - E-commerce application with complex features
- **letmelearn** - Learning application with various patterns

Both projects confirm the patterns documented in this skill.

## See Also

- `/start-baseweb-project` - Create a new Baseweb project from template
- `patterns/project-setup.md` - Detailed project setup patterns
- `templates/` - Code templates for common patterns