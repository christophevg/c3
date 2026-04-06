# Frontend Patterns

Patterns for Vue/Vuetify frontend development in Baseweb projects.

## Page Component Structure

### Basic Page Component

```javascript
// pages/mypage.js

const MyPage = {
  // Navigation configuration (for visible pages)
  navigation: {
    section: null,      // null for root, or section name
    icon: "home",       // Material Design icon name
    text: "My Page",    // Display text in menu
    path: "/mypage",    // URL path
    index: 10           // Sort order in menu
  },
  
  // Template (required)
  template: `
<Page>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>My Page</h1>
        <p>{{ message }}</p>
      </v-col>
    </v-row>
  </v-container>
</Page>
  `,
  
  // Data function (returns initial state)
  data: function() {
    return {
      message: "Hello from My Page!",
      items: [],
      loading: false
    };
  },
  
  // Lifecycle hooks
  mounted: function() {
    // Scroll to top when page loads
    this.$vuetify.goTo(0);
    // Load initial data
    this.loadItems();
  },
  
  // Computed properties
  computed: {
    itemCount: function() {
      return this.items.length;
    }
  },
  
  // Methods
  methods: {
    loadItems: function() {
      this.loading = true;
      $.ajax({
        url: "/api/my-items",
        type: "get",
        success: (response) => {
          this.items = response.items || response;
          this.loading = false;
        },
        error: (response) => {
          this.$notify({
            group: "notifications",
            title: "Error",
            text: "Failed to load items: " + response.responseText,
            type: "error"
          });
          this.loading = false;
        }
      });
    }
  }
};

// Register with navigation
Navigation.add(MyPage);
```

### Page with Vuex Store

```javascript
// pages/users.js

const UsersPage = {
  navigation: {
    section: "admin",
    icon: "people",
    text: "Users",
    path: "/users",
    index: 20
  },
  
  template: `
<Page>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="users"
      :loading="loading"
    >
      <template v-slot:item.actions="{ item }">
        <v-btn icon @click="editUser(item)">
          <v-icon>edit</v-icon>
        </v-btn>
        <v-btn icon @click="deleteUser(item)">
          <v-icon>delete</v-icon>
        </v-btn>
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
        { text: "Email", value: "email" },
        { text: "Actions", value: "actions", sortable: false }
      ]
    };
  },
  
  computed: {
    users: function() {
      return store.getters["users/items"];
    },
    loading: function() {
      return store.getters["users/loading"];
    }
  },
  
  mounted: function() {
    this.$vuetify.goTo(0);
    store.dispatch("users/fetchItems");
  },
  
  methods: {
    editUser: function(user) {
      store.commit("users/setSelected", user);
      this.$router.push("/users/" + user.id + "/edit");
    },
    deleteUser: function(user) {
      if (confirm("Delete this user?")) {
        store.dispatch("users/deleteUser", user.id);
      }
    }
  }
};

Navigation.add(UsersPage);
```

## Vuex Store Modules

### Module Registration

```javascript
// Register page-specific state
store.registerModule("users", {
  namespaced: true,  // Recommended for clarity
  
  state: {
    items: [],
    selectedItem: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_ITEMS: function(state, items) {
      state.items = items;
    },
    SET_SELECTED: function(state, item) {
      state.selectedItem = item;
    },
    SET_LOADING: function(state, loading) {
      state.loading = loading;
    },
    SET_ERROR: function(state, error) {
      state.error = error;
    }
  },
  
  actions: {
    fetchItems: function({ commit }) {
      commit("SET_LOADING", true);
      $.ajax({
        url: "/api/users",
        type: "get",
        success: function(response) {
          commit("SET_ITEMS", response.users || response);
          commit("SET_LOADING", false);
        },
        error: function(xhr) {
          commit("SET_ERROR", xhr.responseText);
          commit("SET_LOADING", false);
        }
      });
    },
    
    deleteUser: function({ dispatch }, userId) {
      $.ajax({
        url: "/api/users/" + userId,
        type: "delete",
        success: function() {
          dispatch("fetchItems");
        },
        error: function(xhr) {
          store.commit("SET_ERROR", xhr.responseText);
        }
      });
    }
  },
  
  getters: {
    items: function(state) { return state.items; },
    selectedItem: function(state) { return state.selectedItem; },
    loading: function(state) { return state.loading; },
    error: function(state) { return state.error; }
  }
});
```

## Navigation Configuration

### Navigation Sections

Create menu sections to organize pages:

```javascript
// In a separate file (e.g., sections.js)

// Add a section first
Navigation.add_section({
  name: "admin",      // Used to reference this section
  icon: "settings",    // Material Design icon
  text: "Administration",
  index: 100          // Sort order for sections
});

// Pages with this section will appear under it
const UsersPage = {
  navigation: {
    section: "admin",  // References the section above
    icon: "people",
    text: "Users",
    path: "/admin/users",
    index: 10
  },
  // ... rest of component
};
```

### Navigation Index

- Root pages: Use index 1-99
- Sectioned pages: Use index within section (1-99)
- Lower index = appears first in menu

```javascript
// Root pages
Navigation.add(HomePage);      // index: 1
Navigation.add(DashboardPage); // index: 2

// Section: Admin (index: 100)
Navigation.add_section({
  name: "admin",
  icon: "settings",
  text: "Administration",
  index: 100
});
Navigation.add(UsersPage);     // section: "admin", index: 10
Navigation.add(SettingsPage);  // section: "admin", index: 20
```

## AJAX Patterns

### GET Request

```javascript
// Simple GET
$.ajax({
  url: "/api/my-endpoint",
  type: "get",
  success: function(response) {
    console.log("Success:", response);
  },
  error: function(xhr) {
    console.error("Error:", xhr.responseText);
  }
});

// GET with query parameters
$.ajax({
  url: "/api/items",
  type: "get",
  data: { page: 1, per_page: 20 },
  success: function(response) {
    // Handle response
  }
});
```

### POST Request

```javascript
// Create new item
$.ajax({
  url: "/api/items",
  type: "post",
  contentType: "application/json",
  data: JSON.stringify({ name: "New Item", value: 42 }),
  success: function(response) {
    this.$notify({
      group: "notifications",
      title: "Success",
      text: "Item created successfully",
      type: "success"
    });
  }.bind(this),
  error: function(xhr) {
    this.$notify({
      group: "notifications",
      title: "Error",
      text: "Failed to create: " + xhr.responseText,
      type: "error"
    });
  }.bind(this)
});
```

### PUT Request

```javascript
// Update item
$.ajax({
  url: "/api/items/" + itemId,
  type: "put",
  contentType: "application/json",
  data: JSON.stringify({ name: "Updated Name" }),
  success: function(response) {
    // Handle success
  }
});
```

### DELETE Request

```javascript
// Delete item
$.ajax({
  url: "/api/items/" + itemId,
  type: "delete",
  success: function() {
    // Item deleted (204 No Content)
  }
});
```

## Socket.IO Events

### Client-Side Event Handling

```javascript
// Connect and listen for events
const MyPage = {
  template: `
<Page>
  <v-container>
    <v-list>
      <v-list-item v-for="log in logs" :key="log.id">
        {{ log.message }}
      </v-list-item>
    </v-list>
  </v-container>
</Page>
  `,
  
  data: function() {
    return {
      logs: []
    };
  },
  
  mounted: function() {
    // Listen for server events
    socket.on("log", (msg) => {
      this.logs.push({
        id: Date.now(),
        message: msg
      });
    });
  },
  
  beforeDestroy: function() {
    // Clean up listener
    socket.off("log");
  }
};
```

### Emitting Events

```javascript
// From frontend to server
socket.emit("my_event", { data: "value" }, (response) => {
  // Handle server response (if any)
  console.log("Server response:", response);
});
```

## Reusable Components

### Creating a Reusable Component

```javascript
// components/my-widget.js

const MyWidget = {
  // No navigation property (not a page)
  
  // Props for customization
  props: {
    title: {
      type: String,
      default: "Widget Title"
    },
    items: {
      type: Array,
      default: () => []
    }
  },
  
  template: `
<v-card>
  <v-card-title>{{ title }}</v-card-title>
  <v-card-text>
    <v-list>
      <v-list-item v-for="item in items" :key="item.id">
        {{ item.name }}
      </v-list-item>
    </v-list>
  </v-card-text>
  <v-card-actions>
    <v-btn text @click="$emit('refresh')">Refresh</v-btn>
  </v-card-actions>
</v-card>
  `,
  
  methods: {
    handleClick: function(item) {
      this.$emit("select", item);
    }
  }
};

// Usage in another component:
// <MyWidget :title="Widget Title" :items="items" @refresh="loadItems" @select="onSelect" />
```

### Using Components

```javascript
// In a page component
const MyPage = {
  components: {
    MyWidget: MyWidget  // Register for local use
  },
  
  template: `
<Page>
  <v-container>
    <MyWidget
      title="My Items"
      :items="items"
      @refresh="loadItems"
      @select="onItemSelect"
    />
  </v-container>
</Page>
  `,
  
  // ... rest of component
};
```

## Common Patterns

### Loading State

```javascript
const MyPage = {
  data: function() {
    return {
      loading: false,
      items: []
    };
  },
  
  methods: {
    loadData: function() {
      this.loading = true;
      $.ajax({
        url: "/api/data",
        success: (response) => {
          this.items = response;
        },
        error: (xhr) => {
          this.$notify({
            group: "notifications",
            title: "Error",
            text: xhr.responseText,
            type: "error"
          });
        },
        complete: () => {
          this.loading = false;  // Always hide loading
        }
      });
    }
  }
};
```

### Error Handling

```javascript
const MyPage = {
  methods: {
    handleError: function(xhr, action) {
      let message = "An error occurred";
      
      try {
        const response = JSON.parse(xhr.responseText);
        message = response.error || message;
      } catch (e) {
        message = xhr.responseText || message;
      }
      
      this.$notify({
        group: "notifications",
        title: action + " Failed",
        text: message,
        type: "error",
        duration: 5000
      });
    }
  }
};
```

### Form Submission

```javascript
const MyPage = {
  data: function() {
    return {
      form: {
        name: "",
        email: "",
        active: true
      },
      errors: {}
    };
  },
  
  methods: {
    submitForm: function() {
      this.errors = {};
      
      $.ajax({
        url: "/api/items",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(this.form),
        success: (response) => {
          this.$notify({
            group: "notifications",
            title: "Success",
            text: "Item created",
            type: "success"
          });
          this.$router.push("/items");
        },
        error: (xhr) => {
          if (xhr.status === 400) {
            this.errors = JSON.parse(xhr.responseText).errors;
          } else {
            this.handleError(xhr, "Create");
          }
        }
      });
    }
  }
};
```