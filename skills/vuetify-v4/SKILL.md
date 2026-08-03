---
name: vuetify-v4
description: |
  Use this skill when creating or modifying Vuetify 4 UI components in Baseweb projects. Examples: "create Vuetify 4 component", "Vuetify layout structure", "Vuetify v-layout v-main v-footer", "fix scrolling layout"
---

# Vuetify 4 Layout and Components

Guide for using Vuetify 4 components and layouts in Baseweb projects.

## When to Use This Skill

Use this skill when:
- Creating Vuetify 4 UI components
- Setting up application layouts
- Implementing responsive design
- Adding navigation, forms, or data display
- Fixing layout issues (scrolling, positioning)

## Vuetify 4 Application Layout

### Standard Layout Structure

Vuetify 4 uses a specific layout hierarchy:

```vue
<v-app>
  <v-layout>
    <v-main>
      <!-- Content fills available space -->
    </v-main>
    <v-footer app>
      <!-- Fixed at bottom -->
    </v-footer>
  </v-layout>
</v-app>
```

**Key Concepts:**

| Component | Purpose |
|-----------|---------|
| `v-app` | Root wrapper (required) |
| `v-layout` | Flexible layout container |
| `v-main` | Content area (fills space between app-bar and footer) |
| `v-footer app` | Fixed footer with `app` prop |
| `v-app-bar app` | Fixed header with `app` prop |

### The `app` Prop

**CRITICAL:** Use `app` prop on `v-footer` and `v-app-bar` to make them fixed.

```vue
<!-- ✓ CORRECT -->
<v-footer app>
  <v-form>...</v-form>
</v-footer>

<!-- ✗ WRONG -->
<v-footer>
  <v-form>...</v-form>
</v-footer>
```

**Why:** The `app` prop tells Vuetify to position the element fixed and adjust `v-main` padding automatically.

## Common Layouts

### Chat Application Layout

For chat apps with fixed input at bottom:

```vue
<v-app>
  <v-layout>
    <v-main style="height: calc(100vh - 64px);">
      <v-container style="height: 100%; display: flex; flex-direction: column; padding: 8px;">
        <v-card style="flex: 1; display: flex; flex-direction: column;">
          <v-card-title>Title</v-card-title>
          <v-card-text style="flex: 1; overflow-y: auto;">
            <!-- Scrollable content -->
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
    
    <v-footer app style="padding: 8px;">
      <v-form style="width: 100%;">
        <v-text-field placeholder="Type a message..." />
      </v-form>
    </v-footer>
  </v-layout>
</v-app>
```

### Scrolling Content Layout

For pages with scrollable content area:

```vue
<v-layout>
  <v-main>
    <v-container style="height: 100%;">
      <v-card style="height: 100%; display: flex; flex-direction: column;">
        <v-card-title>Fixed Header</v-card-title>
        <v-card-text style="flex: 1; overflow-y: auto;">
          <!-- This scrolls independently -->
          <div v-for="item in items">...</div>
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
  
  <v-footer app>
    Fixed Footer Content
  </v-footer>
</v-layout>
```

## Common Mistakes to Avoid

### ❌ Mistake 1: Using Fixed Height with v-container

```vue
<!-- ✗ WRONG: Content won't scroll properly -->
<v-container style="height: calc(100vh - 64px)">
  <div v-for="item in items">...</div>
</v-container>
```

**Why it fails:** v-container doesn't handle overflow correctly, content overflows viewport.

**✓ Solution:** Use v-main + flexbox:

```vue
<!-- ✓ CORRECT: Proper scrolling -->
<v-layout>
  <v-main>
    <v-container style="height: 100%; display: flex; flex-direction: column;">
      <v-card style="flex: 1; overflow-y: auto;">
        <div v-for="item in items">...</div>
      </v-card>
    </v-container>
  </v-main>
</v-layout>
```

### ❌ Mistake 2: Not Using v-layout

```vue
<!-- ✗ WRONG: No layout structure -->
<template>
  <v-main>
    <v-container>...</v-container>
  </v-main>
  <v-footer>...</v-footer>
</template>
```

**Why it fails:** v-main and v-footer need v-layout wrapper to work together.

**✓ Solution:** Add v-layout:

```vue
<!-- ✓ CORRECT -->
<template>
  <v-layout>
    <v-main>
      <v-container>...</v-container>
    </v-main>
    <v-footer app>...</v-footer>
  </v-layout>
</template>
```

### ❌ Mistake 3: Input Not at Bottom

```vue
<!-- ✗ WRONG: Input in middle of screen -->
<v-container style="height: 100vh;">
  <v-row style="flex: 1;">
    <v-col>Messages</v-col>
  </v-row>
  <v-row style="flex-shrink: 0;">
    <v-col>Input</v-col>  <!-- Will float in middle -->
  </v-row>
</v-container>
```

**Why it fails:** Flexbox inside container doesn't work with Vuetify layout.

**✓ Solution:** Use v-footer app:

```vue
<!-- ✓ CORRECT: Input fixed at bottom -->
<v-layout>
  <v-main>
    <v-container>Messages</v-container>
  </v-main>
  <v-footer app>
    <v-text-field />
  </v-footer>
</v-layout>
```

## Notifications

### v-snackbar for Transient Messages

Use `v-snackbar` for connection status, errors, and transient notifications:

```vue
<template>
  <v-snackbar
    v-model="showDisconnected"
    color="warning"
    :timeout="-1"
    location="top"
  >
    <v-icon start>mdi-wifi-off</v-icon>
    Connecting to server...
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      showDisconnected: false
    }
  },
  mounted() {
    socket.on('connect', () => {
      this.showDisconnected = false
    })
    socket.on('disconnect', () => {
      this.showDisconnected = true
    })
  }
}
</script>
```

**Key props:**

| Prop | Purpose |
|------|---------|
| `v-model` | Control visibility |
| `color` | Severity (error, warning, success, info) |
| `:timeout="-1"` | Keep visible until dismissed |
| `location` | Position (top, bottom, left, right) |

### Auto-dismiss Notifications

For temporary messages:

```vue
<v-snackbar
  v-model="showSuccess"
  color="success"
  :timeout="3000"  <!-- Auto-dismiss after 3 seconds -->
>
  Message sent successfully
</v-snackbar>
```

## Scrolling Patterns

### Auto-scroll to Bottom

For chat/message lists:

```vue
<v-card-text
  ref="messagesContainer"
  style="flex: 1; overflow-y: auto;"
>
  <div v-for="message in messages" :key="message.id">
    {{ message.content }}
  </div>
</v-card-text>

<script>
export default {
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container && container.$el) {
          // Vuetify components return component, need $el
          const el = container.$el || container
          el.scrollTop = el.scrollHeight
        }
      })
    }
  },
  mounted() {
    socket.on('message', (message) => {
      this.messages.push(message)
      this.scrollToBottom()
    })
  }
}
</script>
```

## Baseweb Integration

### Baseweb Template Structure

Baseweb's `minimal.html` template provides:

```html
<v-app id="app">
  <keep-alive>
    <router-view></router-view>
  </keep-alive>
  <notification-snackbar></notification-snackbar>
</v-app>
```

**Your Page component should use:**

```vue
<Page>
  <v-layout style="height: 100vh;">
    <v-main>
      <!-- Content -->
    </v-main>
    <v-footer app>
      <!-- Footer -->
    </v-footer>
  </v-layout>
</Page>
```

## Responsive Design

### Mobile-first with v-container

```vue
<v-container fluid style="padding: 0;">
  <v-layout>
    <v-main>
      <v-container>
        <!-- Mobile-first, full-width on small screens -->
        <v-row>
          <v-col cols="12" md="8">
            <!-- Full width on mobile, 8 columns on medium+ -->
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</v-container>
```

### Breakpoints

| Breakpoint | Width | Class Suffix |
|------------|-------|---------------|
| xs | < 600px | `cols="12"` |
| sm | ≥ 600px | `sm="6"` |
| md | ≥ 960px | `md="4"` |
| lg | ≥ 1280px | `lg="3"` |
| xl | ≥ 1920px | `xl="2"` |

## Related Skills

- `baseweb` — Baseweb project structure and patterns
- `python-project` — Python project setup
- `readme` — README documentation
