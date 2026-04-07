# Navigation Patterns

Comprehensive patterns for Vuetify V2 navigation components.

## Toolbars and System Bars

### v-toolbar
Primary source of site navigation and a versatile container for GUI layouts.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `app` | boolean | Integrates into application layout sizing |
| `color` | string | CSS or material color |
| `dark` / `light` | boolean | Theme variants |
| `dense` | boolean | Reduces height |
| `flat` | boolean | Removes box-shadow |
| `prominent` | boolean | Increases height |

**Example:**
```vue
<v-toolbar app color="primary" dark>
  <v-toolbar-title>My Application</v-toolbar-title>
  <v-toolbar-items>
    <v-btn flat>Home</v-btn>
    <v-btn flat>About</v-btn>
  </v-toolbar-items>
</v-toolbar>
```

### v-system-bar
Mimics a system status bar (mobile status bar or desktop window bar).

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `color` | string | Background color |
| `dark` | boolean | White text/icons |
| `height` | number | Defaults to 24 (32 if `window` is true) |
| `window` | boolean | Increases default height to 32px |
| `app` | boolean | Integrates into layout system |

**Example:**
```vue
<v-system-bar dark color="primary">
  <v-icon>mdi-wifi</v-icon>
  <v-spacer></v-spacer>
  <span>12:30 PM</span>
</v-system-bar>
```

## App Bar


### v-app-bar

Top-level navigation bar.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `app` | boolean | Register with layout system |
| `color` | string | Background color |
| `dark` | boolean | Dark theme |
| `elevation` | number | Shadow depth 0-24 |
| `flat` | boolean | Remove shadow |
| `clipped-left` | boolean | Clip left drawer |
| `clipped-right` | boolean | Clip right drawer |
| `dense` | boolean | Dense style |
| `prominent` | boolean | Increase height |
| `shrink-on-scroll` | boolean | Shrink on scroll |

```vue
<v-app-bar app color="primary" dark>
  <v-app-bar-nav-icon @click="drawer = !drawer" />
  <v-toolbar-title>App Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon><v-icon>mdi-magnify</v-icon></v-btn>
  <v-btn icon><v-icon>mdi-cog</v-icon></v-btn>
  <v-btn icon><v-icon>mdi-account</v-icon></v-btn>
</v-app-bar>
```

### App Bar with Tabs

```vue
<v-app-bar app color="primary" dark>
  <v-toolbar-title>Page Title</v-toolbar-title>

  <template v-slot:extension>
    <v-tabs v-model="tab" background-color="primary" dark>
      <v-tab href="#tab-1">Tab 1</v-tab>
      <v-tab href="#tab-2">Tab 2</v-tab>
      <v-tab href="#tab-3">Tab 3</v-tab>
    </v-tabs>
  </template>
</v-app-bar>

<v-tabs-items v-model="tab">
  <v-tab-item id="tab-1">Content 1</v-tab-item>
  <v-tab-item id="tab-2">Content 2</v-tab-item>
  <v-tab-item id="tab-3">Content 3</v-tab-item>
</v-tabs-items>
```

### Collapsible App Bar

```vue
<v-app-bar
  app
  color="primary"
  dark
  prominent
  shrink-on-scroll
  fade-img-on-scroll
>
  <v-app-bar-nav-icon @click="drawer = !drawer" />
  <v-toolbar-title>Scroll to Collapse</v-toolbar-title>
</v-app-bar>
```

## Navigation Drawer

### v-navigation-drawer

Side navigation panel.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `app` | boolean | Register with layout system |
| `v-model` | boolean | Control visibility |
| `clipped` | boolean | Below app-bar |
| `permanent` | boolean | Always visible |
| `temporary` | boolean | Overlay mode |
| `mini-variant` | boolean | Collapsed state |
| `expand-on-hover` | boolean | Expand on hover |
| `width` | number | Drawer width |
| `right` | boolean | Right side |
| `src` | string | Background image |

```vue
<!-- Basic drawer -->
<v-navigation-drawer app v-model="drawer">
  <v-list>
    <v-list-item to="/">
      <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- Mini variant with expand on hover -->
<v-navigation-drawer
  app
  v-model="drawer"
  mini-variant
  expand-on-hover
>
  <v-list>
    <v-list-item to="/">
      <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- With header -->
<v-navigation-drawer app v-model="drawer">
  <v-list-item>
    <v-list-item-avatar>
      <v-img src="avatar.jpg" />
    </v-list-item-avatar>
    <v-list-item-content>
      <v-list-item-title>User Name</v-list-item-title>
      <v-list-item-subtitle>user@email.com</v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>

  <v-divider />

  <v-list>
    <v-list-item to="/">
      <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</v-navigation-drawer>
```

### Drawer with Groups

```vue
<v-navigation-drawer app v-model="drawer">
  <v-list>
    <v-subheader>Navigation</v-subheader>
    <v-list-item to="/" exact>
      <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-subheader>Settings</v-subheader>
    <v-list-item to="/settings">
      <v-list-item-icon><v-icon>mdi-cog</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Settings</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</v-navigation-drawer>
```

### Nested Navigation (Expansion Panels)

```vue
<v-navigation-drawer app v-model="drawer">
  <v-list dense>
    <v-list-group
      v-for="item in menuItems"
      :key="item.title"
      :prepend-icon="item.icon"
      no-action
    >
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </template>

      <v-list-item
        v-for="subItem in item.children"
        :key="subItem.title"
        :to="subItem.to"
      >
        <v-list-item-content>
          <v-list-item-title>{{ subItem.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-group>
  </v-list>
</v-navigation-drawer>
```

## Tabs

### v-tabs

Content organization with tabbed navigation.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Active tab |
| `background-color` | string | Background color |
| `grow` | boolean | Fill available width |
| `icons-and-text` | boolean | Show icons with text |
| `vertical` | boolean | Vertical tabs |
| `right` | boolean | Align right |

```vue
<!-- Basic tabs -->
<v-tabs v-model="tab">
  <v-tab href="#tab-1">Tab 1</v-tab>
  <v-tab href="#tab-2">Tab 2</v-tab>
  <v-tab href="#tab-3">Tab 3</v-tab>
</v-tabs>

<v-tabs-items v-model="tab">
  <v-tab-item id="tab-1">Content 1</v-tab-item>
  <v-tab-item id="tab-2">Content 2</v-tab-item>
  <v-tab-item id="tab-3">Content 3</v-tab-item>
</v-tabs-items>

<!-- Tabs with icons -->
<v-tabs v-model="tab" icons-and-text>
  <v-tab href="#tab-1">
    Tab 1
    <v-icon>mdi-home</v-icon>
  </v-tab>
  <v-tab href="#tab-2">
    Tab 2
    <v-icon>mdi-cog</v-icon>
  </v-tab>
</v-tabs>

<!-- Vertical tabs -->
<v-tabs v-model="tab" vertical>
  <v-tab href="#tab-1">Tab 1</v-tab>
  <v-tab href="#tab-2">Tab 2</v-tab>
</v-tabs>
```

### Dynamic Tabs

```vue
<v-tabs v-model="tab">
  <v-tab
    v-for="item in items"
    :key="item.id"
    :href="`#tab-${item.id}`"
  >
    {{ item.title }}
  </v-tab>
</v-tabs>

<v-tabs-items v-model="tab">
  <v-tab-item
    v-for="item in items"
    :key="item.id"
    :id="`tab-${item.id}`"
  >
    <v-card flat>
      <v-card-text>{{ item.content }}</v-card-text>
    </v-card>
  </v-tab-item>
</v-tabs-items>
```

## Breadcrumbs

### v-breadcrumbs

Path indication for navigation.

```vue
<v-breadcrumbs :items="items">
  <template v-slot:item="{ item }">
    <v-breadcrumbs-item
      :href="item.href"
      :disabled="item.disabled"
    >
      {{ item.text }}
    </v-breadcrumbs-item>
  </template>
</v-breadcrumbs>

<script>
export default {
  data: () => ({
    items: [
      { text: 'Home', href: '/' },
      { text: 'Products', href: '/products' },
      { text: 'Details', disabled: true }
    ]
  })
}
</script>
```

### Breadcrumbs with Icons

```vue
<v-breadcrumbs :items="items" large>
  <template v-slot:item="{ item }">
    <v-breadcrumbs-item :href="item.href">
      <v-icon v-if="item.icon" small class="mr-2">{{ item.icon }}</v-icon>
      {{ item.text }}
    </v-breadcrumbs-item>
  </template>
</v-breadcrumbs>
```

## Pagination

### v-pagination

Navigate through paginated data.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | number | Current page |
| `length` | number | Total pages |
| `total-visible` | number | Visible page numbers |
| `disabled` | boolean | Disable pagination |

```vue
<v-pagination v-model="page" :length="totalPages" />

<!-- With limited visible pages -->
<v-pagination
  v-model="page"
  :length="totalPages"
  :total-visible="7"
/>

<!-- Circle style -->
<v-pagination
  v-model="page"
  :length="totalPages"
  circle
/>
```

## Footer

### v-footer

Bottom navigation area.

```vue
<!-- Basic footer -->
<v-footer app>
  <span>&copy; 2024 My App</span>
</v-footer>

<!-- With links -->
<v-footer app color="primary" dark>
  <v-spacer />
  <v-btn text href="/about">About</v-btn>
  <v-btn text href="/privacy">Privacy</v-btn>
  <v-btn text href="/terms">Terms</v-btn>
  <v-spacer />
  <span>&copy; 2024 My App</span>
</v-footer>

<!-- With social icons -->
<v-footer app color="primary" dark>
  <v-spacer />
  <v-btn icon href="https://twitter.com"><v-icon>mdi-twitter</v-icon></v-btn>
  <v-btn icon href="https://github.com"><v-icon>mdi-github</v-icon></v-btn>
  <v-btn icon href="https://linkedin.com"><v-icon>mdi-linkedin</v-icon></v-btn>
  <v-spacer />
  <span>&copy; 2024 My App</span>
</v-footer>
```

## Bottom Navigation

### v-bottom-navigation

Mobile-friendly navigation bar.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `app` | boolean | Register with layout system |
| `v-model` | number | Active item |
| `color` | string | Background color |
| `grow` | boolean | Fill available width |
| `fixed` | boolean | Fixed position |

```vue
<v-bottom-navigation app v-model="activeTab" color="primary">
  <v-btn value="home">
    <span>Home</span>
    <v-icon>mdi-home</v-icon>
  </v-btn>
  <v-btn value="search">
    <span>Search</span>
    <v-icon>mdi-magnify</v-icon>
  </v-btn>
  <v-btn value="profile">
    <span>Profile</span>
    <v-icon>mdi-account</v-icon>
  </v-btn>
</v-bottom-navigation>
```

## Floating Action Button

### v-fab / v-speed-dial

Primary action button.

**v-fab:**

```vue
<v-btn fab color="primary" dark absolute bottom right>
  <v-icon>mdi-plus</v-icon>
</v-btn>

<!-- Fixed position -->
<v-btn fab color="primary" dark fixed bottom right>
  <v-icon>mdi-plus</v-icon>
</v-btn>
```

**v-speed-dial (multiple actions):**

```vue
<v-speed-dial
  v-model="fab"
  direction="top"
  transition="slide-y-reverse-transition"
  fixed
  bottom
  right
>
  <template v-slot:activator>
    <v-btn v-model="fab" color="primary" dark fab>
      <v-icon v-if="fab">mdi-close</v-icon>
      <v-icon v-else>mdi-menu</v-icon>
    </v-btn>
  </template>
  <v-btn fab dark small color="green">
    <v-icon>mdi-pencil</v-icon>
  </v-btn>
  <v-btn fab dark small color="blue">
    <v-icon>mdi-share-variant</v-icon>
  </v-btn>
  <v-btn fab dark small color="red">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
</v-speed-dial>
```

## Complete Layout Pattern

```vue
<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>My App</v-toolbar-title>
      <v-spacer />
      <v-btn icon><v-icon>mdi-magnify</v-icon></v-btn>
      <v-menu left bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="() => {}">
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer app v-model="drawer" clipped>
      <v-list dense>
        <v-list-item to="/" exact>
          <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/about">
          <v-list-item-icon><v-icon>mdi-information</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app>
      <span>&copy; 2024 My App</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    drawer: true
  }),
  methods: {
    logout() {
      // Handle logout
    }
  }
}
</script>
```

## See Also

- [Vuetify App Bars](https://vuetifyjs.com/en/components/app-bars/)
- [Vuetify Navigation Drawers](https://vuetifyjs.com/en/components/navigation-drawers/)
- [Vuetify Tabs](https://vuetifyjs.com/en/components/tabs/)
- [Vuetify Breadcrumbs](https://vuetifyjs.com/en/components/breadcrumbs/)