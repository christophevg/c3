---
name: vue
description: Use this skill when working with Vue.js components, reactivity, state management, or component patterns in Baseweb projects. Examples: "Vue component structure", "Vue reactivity issues", "shared state between components", "Vue computed properties"
---

# Vue.js Component Patterns

Guide for Vue.js patterns in Baseweb projects.

## When to Use This Skill

Use this skill when:
- Creating Vue components
- Managing shared state between components
- Fixing reactivity issues
- Implementing component lifecycle hooks

## Store Pattern for Global State

When multiple components need to share state (e.g., authentication, user session), use a centralized store instead of `$root` or prop drilling.

### Why Use a Store

| Problem | Store Solution |
|---------|----------------|
| Components race to initialize `$root` | Store initializes once on document ready |
| State changes don't propagate | Vue reactivity works correctly |
| Coupled components | Decoupled via store getters |
| Hard to debug | Clear state flow with mutations |

### Store Module Structure

```javascript
// Register a store module for authentication
store.registerModule("auth", {
  state: {
    checking: true,
    session: null
  },
  getters: {
    checking: function(state) { return state.checking; },
    session: function(state) { return state.session; }
  },
  actions: {
    setup_session: function(context) {
      context.commit("checking", true);
      $.ajax({
        type: "GET",
        url: "/auth/me",
        success: function(res) {
          context.commit("session", res);
          context.commit("checking", false);
        },
        error: function() {
          context.commit("checking", false);
        },
        dataType: "json"
      });
    },
    logout: function(context) {
      $.ajax({
        type: "POST",
        url: "/auth/logout",
        success: function() {
          context.commit("session", null);
        }
      });
    }
  },
  mutations: {
    session: function(state, new_session) {
      state.session = new_session;
    },
    checking: function(state, new_state) {
      state.checking = new_state;
    }
  }
});

// Initialize on document ready
$(document).ready(function() {
  store.dispatch("setup_session");
});
```

### Component Usage

**AuthDialog component** - Shows login dialog when not authenticated:

```javascript
app.component('AuthDialog', {
  computed: {
    showDialog() { return !store.getters.checking && !store.getters.session; },
    checkingSession() { return store.getters.checking; }
  },
  // ... rest of component
});
```

**Chat component** - Shows chat interface when authenticated:

```javascript
var Chat = {
  computed: {
    authenticated() { return store.getters.session != null; },
    currentUser() {
      return this.authenticated ? store.getters.session.user : null;
    }
  },
  methods: {
    handleLogout() {
      store.dispatch("logout");
    }
  }
  // ... rest of component
};
```

### Template Usage

```vue
<template>
  <Page>
    <!-- Show auth dialog when not authenticated -->
    <AuthDialog v-if="!authenticated" />

    <!-- Show main content when authenticated -->
    <v-layout v-if="authenticated">
      <!-- Main content -->
    </v-layout>
  </Page>
</template>

<script>
export default {
  computed: {
    authenticated() { return store.getters.session != null; }
  }
}
</script>
```

### Common Mistakes

#### ❌ Mistake: Using `$root` for Shared State

```javascript
// ✗ WRONG: Race conditions between components
this.$root.authenticated = true;

// ✗ WRONG: Vue 3 doesn't have $set
this.$set(this.$root, 'authenticated', true);
```

**Why it fails:** Multiple components may initialize `$root` at different times, causing race conditions. Vue 3 has automatic reactivity and doesn't need `$set`.

**✓ Solution:** Use store pattern:

```javascript
// ✓ CORRECT: Single source of truth
context.commit("session", { user: data.user });
```

#### ❌ Mistake: Duplicate Initialization

```javascript
// ✗ WRONG: Multiple components initializing state
// Chat component
mounted() { this.checkSession(); }

// AuthDialog component  
mounted() { this.checkSession(); }
```

**Why it fails:** Race conditions, unnecessary API calls, state conflicts.

**✓ Solution:** Single initialization:

```javascript
// ✓ CORRECT: One check on document ready
$(document).ready(function() {
  store.dispatch("setup_session");
});
```

#### ❌ Mistake: Accessing Store Directly in Templates

```vue
<!-- ✗ WRONG -->
<v-layout v-if="store.getters.session != null">
```

**Why it fails:** Vue templates can't access store directly, and it's not reactive.

**✓ Solution:** Use computed properties:

```javascript
computed: {
  authenticated() { return store.getters.session != null; }
}
```

```vue
<!-- ✓ CORRECT -->
<v-layout v-if="authenticated">
```

## Vue 3 Reactivity

### Automatic Reactivity

Vue 3 has automatic reactivity for plain objects. No need for `$set`:

```javascript
// Vue 2 (deprecated)
this.$set(this.someObject, 'key', value);

// Vue 3 (correct)
this.someObject.key = value;
```

### Computed Properties for Store Access

Always use computed properties to access store state:

```javascript
computed: {
  user() { return store.getters.session?.user; },
  authenticated() { return store.getters.session != null; }
}
```

### Watchers for Side Effects

Use watchers when you need to react to state changes:

```javascript
watch: {
  authenticated(newVal) {
    if (newVal) {
      this.connectSocket();
    } else {
      this.disconnectSocket();
    }
  }
}
```

## Component Lifecycle

### mounted() for Initialization

```javascript
mounted() {
  // Component is in DOM, safe to access refs
  this.$refs.inputField?.focus();

  // Set up event listeners
  socket.on('message', this.handleMessage);
}
```

### beforeUnmount() for Cleanup

```javascript
beforeUnmount() {
  // Clean up event listeners
  socket.off('message', this.handleMessage);
}
```

## Related Skills

- `vuetify-v4` — Vuetify 4 specific layouts and components
- `baseweb` — Baseweb project structure and patterns