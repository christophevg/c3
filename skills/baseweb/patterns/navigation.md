# Navigation Patterns

Patterns for configuring navigation in Baseweb applications.

## Navigation Object

The global `Navigation` object manages all pages and sections in the application menu.

### Adding Pages

```javascript
// Add a page to the navigation
Navigation.add(MyPage);
```

### Adding Sections

Create menu sections to organize pages:

```javascript
// Create a section first
Navigation.add_section({
  name: "admin",      // Reference name for pages
  icon: "settings",    // Material Design icon
  text: "Administration",
  index: 100           // Sort order for sections
});
```

## Navigation Configuration

### Page Properties

Each page component should have a `navigation` property:

```javascript
const MyPage = {
  navigation: {
    section: null,      // null for root, or section name
    icon: "home",       // Material Design icon name
    text: "My Page",    // Display text in menu
    path: "/mypage",    // URL path (must start with /)
    index: 10           // Sort order (lower = first)
  },
  // ... rest of component
};
```

### Section Reference

Pages with a `section` property appear under that section:

```javascript
// First create the section
Navigation.add_section({
  name: "management",
  icon: "business",
  text: "Management",
  index: 50
});

// Then add pages to it
const UsersPage = {
  navigation: {
    section: "management",  // References the section above
    icon: "people",
    text: "Users",
    path: "/management/users",
    index: 10
  },
  // ...
};

const RolesPage = {
  navigation: {
    section: "management",
    icon: "security",
    text: "Roles",
    path: "/management/roles",
    index: 20
  },
  // ...
};

Navigation.add(UsersPage);
Navigation.add(RolesPage);
```

## Index Ordering

### Ordering Convention

- Root pages: 1-99
- Section pages: 1-99 within section
- Sections: 100+ (to separate from root pages)

```javascript
// Root pages
Navigation.add(HomePage);       // index: 1
Navigation.add(DashboardPage);  // index: 2
Navigation.add(ProfilePage);    // index: 3

// Sections
Navigation.add_section({
  name: "admin",
  icon: "settings",
  text: "Administration",
  index: 100
});

// Pages in sections
Navigation.add(UsersPage);      // section: "admin", index: 10
Navigation.add(RolesPage);      // section: "admin", index: 20
Navigation.add(SettingsPage);   // section: "admin", index: 30
```

### Typical Index Values

| Level | Index Range | Purpose |
|-------|-------------|---------|
| Root Home | 1-5 | Home, Dashboard |
| Root Primary | 10-50 | Main features |
| Root Secondary | 60-90 | Secondary features |
| Sections | 100+ | Grouped features |

## Icon Reference

Use Material Design icon names:

| Category | Icons |
|----------|-------|
| Home | `home`, `dashboard`, `apps` |
| Content | `article`, `description`, `folder` |
| Users | `people`, `person`, `group` |
| Settings | `settings`, `build`, `tune` |
| Data | `storage`, `table_chart`, `analytics` |
| Actions | `add`, `edit`, `delete`, `save` |
| Status | `check_circle`, `warning`, `error` |
| Communication | `email`, `chat`, `notifications` |

## Backend Registration

Every page must be registered on the backend with its route:

```python
# pages/mypage.py
import os
from module_name.web import server

HERE = os.path.dirname(__file__)
server.register_component("mypage.js", HERE, route="/mypage")
```

### Batch Registration

```python
# pages/__init__.py
from pathlib import Path
from module_name.web import server

PAGES = Path(__file__).parent

for page in ["home", "dashboard", "users", "settings"]:
    server.register_component(f"{page}.js", PAGES, route=f"/{page}")
```

### Route Parameters

For pages with dynamic routes:

```python
# For /users/:id
server.register_component("user-detail.js", PAGES, route="/users/:id")

# For nested routes /users/:id/posts
server.register_component("user-posts.js", PAGES, route="/users/:id/posts")
```

## Protected Pages

### Authentication Check

Pages can be protected by checking authentication:

```javascript
const ProtectedPage = {
  navigation: {
    section: "admin",
    icon: "lock",
    text: "Protected",
    path: "/protected",
    index: 10
  },
  
  template: `
<v-dialog v-model="authenticating" persistent max-width="500">
  <v-card>
    <v-card-title>Authentication Required</v-card-title>
    <v-card-text>
      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />
    </v-card-text>
    <v-card-actions>
      <v-btn @click="login">Login</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
  `,
  
  data: function() {
    return {
      authenticating: true,
      username: "",
      password: ""
    };
  },
  
  methods: {
    login: function() {
      $.ajax({
        url: "/api/auth/login",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify({
          username: this.username,
          password: this.password
        }),
        success: (response) => {
          store.commit("setUser", response.user);
          this.authenticating = false;
        },
        error: () => {
          this.$notify({
            group: "notifications",
            title: "Error",
            text: "Invalid credentials",
            type: "error"
          });
        }
      });
    }
  }
};

Navigation.add(ProtectedPage);
```

## Dynamic Navigation

### Conditional Visibility

```javascript
const AdminPage = {
  navigation: {
    section: "admin",
    icon: "admin_panel_settings",
    text: "Admin Panel",
    path: "/admin",
    index: 100
  },
  
  computed: {
    isVisible: function() {
      // Check if user has admin role
      return store.getters.hasRole("admin");
    }
  },
  
  // ... rest
};

// Add only if user has permission
if (store.getters.hasRole("admin")) {
  Navigation.add(AdminPage);
}
```

### Runtime Navigation Updates

```javascript
// Add navigation dynamically
function addDynamicPage(pageConfig) {
  const DynamicPage = {
    navigation: {
      section: pageConfig.section,
      icon: pageConfig.icon,
      text: pageConfig.text,
      path: pageConfig.path,
      index: pageConfig.index
    },
    template: pageConfig.template,
    // ... other config
  };
  
  Navigation.add(DynamicPage);
}
```

## Navigation Menu Structure

The navigation structure created by the above code:

```
┌─────────────────────────────┐
│  🏠 Home                    │  index: 1
│  📊 Dashboard               │  index: 2
│  👤 Profile                 │  index: 3
├─────────────────────────────┤
│  ⚙️ Administration          │  section: admin (index: 100)
│    👥 Users                 │    index: 10
│    🔐 Roles                │    index: 20
│    ⚙️ Settings             │    index: 30
├─────────────────────────────┤
│  🏢 Management              │  section: management (index: 50)
│    📂 Projects             │    index: 10
│    📋 Tasks                │    index: 20
└─────────────────────────────┘
```

## Common Patterns

### Multi-Level Navigation

For deep navigation hierarchies, use nested sections:

```javascript
// First level section
Navigation.add_section({
  name: "settings",
  icon: "settings",
  text: "Settings",
  index: 100
});

// Second level (pages under settings)
Navigation.add({
  navigation: {
    section: "settings",
    icon: "palette",
    text: "Appearance",
    path: "/settings/appearance",
    index: 10
  },
  // ...
});

Navigation.add({
  navigation: {
    section: "settings",
    icon: "notifications",
    text: "Notifications",
    path: "/settings/notifications",
    index: 20
  },
  // ...
});
```

### External Links

For links to external pages:

```javascript
const ExternalLink = {
  navigation: {
    section: null,
    icon: "open_in_new",
    text: "Documentation",
    path: "https://docs.example.com",  // External URL
    index: 999
  },
  // External links typically don't need a template
  // They open in a new tab
};
```

### Search/Filter Pages

Pages with query parameters:

```javascript
const SearchPage = {
  navigation: {
    section: null,
    icon: "search",
    text: "Search",
    path: "/search",
    index: 50
  },
  
  template: `
<Page>
  <v-container>
    <v-text-field v-model="query" @input="search" label="Search" />
    <v-list>
      <v-list-item v-for="result in results" :key="result.id">
        {{ result.name }}
      </v-list-item>
    </v-list>
  </v-container>
</Page>
  `,
  
  data: function() {
    return {
      query: "",
      results: []
    };
  },
  
  mounted: function() {
    // Read initial query from URL
    this.query = this.$route.query.q || "";
    if (this.query) {
      this.search();
    }
  },
  
  methods: {
    search: function() {
      // Update URL
      this.$router.push({ query: { q: this.query } });
      
      // Perform search
      $.ajax({
        url: "/api/search",
        data: { q: this.query },
        success: (response) => {
          this.results = response.results;
        }
      });
    }
  }
};

Navigation.add(SearchPage);
```