# Navigation Patterns

Comprehensive patterns for Vuetify V3 navigation components.

## App Bar

### v-app-bar

Top-level navigation bar with app-like appearance.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Background color |
| `density` | string | Density: `default`, `comfortable`, `compact`, `prominent` |
| `flat` | boolean | Remove elevation |
| `elevation` | number | Shadow elevation |
| `extended` | boolean | Extend height for more content |
| `extension-height` | number | Height of extension |
| `scroll-target` | string | CSS selector for scroll container |
| `scroll-threshold` | number | Scroll threshold for collapse |
| `app` | boolean | Fixed within app layout |

**V3 Changes:**
- `app` prop for app layout integration
- Use `density` instead of separate props for height

```vue
<!-- Basic app bar -->
<v-app-bar color="primary">
  <v-app-bar-title>My App</v-app-bar-title>
  <v-spacer />
  <v-btn icon="mdi-magnify" />
  <v-btn icon="mdi-dots-vertical" />
</v-app-bar>

<!-- App bar with navigation -->
<v-app-bar color="primary" density="prominent">
  <v-app-bar-nav-icon @click="drawer = !drawer" />
  <v-app-bar-title>My App</v-app-bar-title>
  <v-spacer />
  <v-btn icon="mdi-magnify" />
  <v-btn icon="mdi-bell" />
</v-app-bar>

<!-- App bar with extension -->
<v-app-bar color="primary" extended>
  <v-app-bar-title>My App</v-app-bar-title>
  <v-spacer />
  <v-btn icon="mdi-magnify" />
  <template #extension>
    <v-tabs>
      <v-tab to="/home">Home</v-tab>
      <v-tab to="/about">About</v-tab>
    </v-tabs>
  </template>
</v-app-bar>

<!-- Collapsing app bar -->
<v-app-bar
  color="primary"
  scroll-behavior="collapse"
  scroll-threshold="100"
>
  <v-app-bar-title>My App</v-app-bar-title>
</v-app-bar>
```

### v-app-bar-nav-icon

Hamburger menu icon for navigation drawer.

```vue
<v-app-bar color="primary">
  <v-app-bar-nav-icon @click="drawer = !drawer" />
  <v-app-bar-title>My App</v-app-bar-title>
</v-app-bar>
```

### v-app-bar-title

Title component for app bar.

```vue
<v-app-bar color="primary">
  <v-app-bar-title>
    <v-icon icon="mdi-home" class="mr-2" />
    My App
  </v-app-bar-title>
</v-app-bar>
```

## Navigation Drawer

### v-navigation-drawer

Side navigation panel.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | boolean | Control visibility |
| `color` | string | Background color |
| `permanent` | boolean | Always visible |
| `temporary` | boolean | Overlay drawer (closes on outside click) |
| `mini-variant` | boolean | Collapsed state with icons only |
| `expand-on-hover` | boolean | Expand on hover when mini |
| `location` | string | Position: `left`, `right`, `start`, `end` |
| `width` | number/string | Drawer width (default: 256) |
| `app` | boolean | Fixed within app layout |
| `clipped` | boolean | Clip below app bar |
| `floating` | boolean | No visible border |

**V3 Changes:**
- Use `v-model` instead of `value` prop
- `location` prop for positioning

```vue
<!-- Basic drawer -->
<v-navigation-drawer v-model="drawer" app>
  <v-list>
    <v-list-item to="/home">
      <template #prepend>
        <v-icon icon="mdi-home" />
      </template>
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item>
    <v-list-item to="/about">
      <template #prepend>
        <v-icon icon="mdi-information" />
      </template>
      <v-list-item-title>About</v-list-item-title>
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- Mini variant -->
<v-navigation-drawer v-model="drawer" mini-variant app>
  <v-list>
    <v-list-item to="/home">
      <v-icon icon="mdi-home" />
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- Expand on hover -->
<v-navigation-drawer
  v-model="drawer"
  mini-variant
  expand-on-hover
  app
>
  <v-list>
    <v-list-item to="/home">
      <template #prepend>
        <v-icon icon="mdi-home" />
      </template>
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- Permanent drawer -->
<v-navigation-drawer permanent app>
  <v-list>
    <v-list-item to="/home">
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item>
  </v-list>
</v-navigation-drawer>

<!-- Temporary (overlay) drawer -->
<v-navigation-drawer v-model="drawer" temporary app>
  <v-list>
    <v-list-item to="/home">
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item>
  </v-list>
</v-navigation-drawer>
```

### List Items in Drawer

```vue
<v-navigation-drawer v-model="drawer" app>
  <!-- User profile -->
  <v-list-item>
    <template #prepend>
      <v-avatar :image="user.avatar" />
    </template>
    <v-list-item-title>{{ user.name }}</v-list-item-title>
    <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
  </v-list-item>

  <v-divider />

  <!-- Navigation items -->
  <v-list nav>
    <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard">
      <v-list-item-title>Dashboard</v-list-item-title>
    </v-list-item>

    <v-list-item to="/profile" prepend-icon="mdi-account">
      <v-list-item-title>Profile</v-list-item-title>
    </v-list-item>

    <v-list-group value="settings">
      <template #activator="{ props }">
        <v-list-item v-bind="props" prepend-icon="mdi-cog">
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item>
      </template>

      <v-list-item to="/settings/general">
        <v-list-item-title>General</v-list-item-title>
      </v-list-item>

      <v-list-item to="/settings/security">
        <v-list-item-title>Security</v-list-item-title>
      </v-list-item>
    </v-list-group>
  </v-list>

  <v-spacer />

  <!-- Logout -->
  <v-list-item @click="logout" prepend-icon="mdi-logout">
    <v-list-item-title>Logout</v-list-item-title>
  </v-list-item>
</v-navigation-drawer>
```

## Tabs

### v-tabs

Tabbed navigation for content sections.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Selected tab value |
| `align-tabs` | string | Tab alignment: `start`, `center`, `end`, `title` |
| `bg-color` | string | Background color |
| `color` | string | Active tab indicator color |
| `grow` | boolean | Expand tabs to fill width |
| `center-active` | boolean | Center active tab |
| `show-arrows` | boolean | Show navigation arrows |

**V3 Changes:**
- `v-tabs-items` removed, use `v-window` instead
- `v-tab-item` removed, use `v-window-item` instead
- Use `v-model` instead of `value`

```vue
<!-- Basic tabs -->
<v-tabs v-model="tab">
  <v-tab value="tab1">Tab 1</v-tab>
  <v-tab value="tab2">Tab 2</v-tab>
  <v-tab value="tab3">Tab 3</v-tab>
</v-tabs>

<v-window v-model="tab">
  <v-window-item value="tab1">
    <v-card>Content for Tab 1</v-card>
  </v-window-item>
  <v-window-item value="tab2">
    <v-card>Content for Tab 2</v-card>
  </v-window-item>
  <v-window-item value="tab3">
    <v-card>Content for Tab 3</v-card>
  </v-window-item>
</v-window>

<!-- Tabs with router -->
<v-tabs>
  <v-tab to="/home">Home</v-tab>
  <v-tab to="/about">About</v-tab>
  <v-tab to="/contact">Contact</v-tab>
</v-tabs>

<!-- Tabs with icons -->
<v-tabs v-model="tab" color="primary">
  <v-tab value="tab1">
    <v-icon icon="mdi-home" start />
    Home
  </v-tab>
  <v-tab value="tab2">
    <v-icon icon="mdi-account" start />
    Profile
  </v-tab>
</v-tabs>

<!-- Growing tabs -->
<v-tabs v-model="tab" grow>
  <v-tab value="tab1">Tab 1</v-tab>
  <v-tab value="tab2">Tab 2</v-tab>
</v-tabs>

<!-- Centered tabs -->
<v-tabs v-model="tab" centered>
  <v-tab value="tab1">Tab 1</v-tab>
  <v-tab value="tab2">Tab 2</v-tab>
</v-tabs>

<!-- Tabs with arrows for overflow -->
<v-tabs v-model="tab" show-arrows>
  <v-tab value="tab1">Tab 1</v-tab>
  <v-tab value="tab2">Tab 2</v-tab>
  <!-- ... more tabs -->
</v-tabs>
```

## Breadcrumbs

### v-breadcrumbs

Path indication for navigation.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `items` | array | Breadcrumb items |
| `divider` | string | Divider between items |

```vue
<!-- With items array -->
<v-breadcrumbs
  :items="[
    { title: 'Home', to: '/' },
    { title: 'Products', to: '/products' },
    { title: 'Details', disabled: true }
  ]"
/>

<!-- With custom divider -->
<v-breadcrumbs
  :items="items"
  divider="/"
/>

<!-- With slots -->
<v-breadcrumbs>
  <v-breadcrumbs-item to="/">Home</v-breadcrumbs-item>
  <v-breadcrumbs-divider>/</v-breadcrumbs-divider>
  <v-breadcrumbs-item to="/products">Products</v-breadcrumbs-item>
  <v-breadcrumbs-divider>/</v-breadcrumbs-divider>
  <v-breadcrumbs-item disabled>Details</v-breadcrumbs-item>
</v-breadcrumbs>

<!-- With icons -->
<v-breadcrumbs :items="items">
  <template #prepend>
    <v-icon icon="mdi-home" />
  </template>
</v-breadcrumbs>
```

## Pagination

### v-pagination

Pagination for long data sets.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | number | Current page |
| `length` | number | Total pages |
| `total-visible` | number | Visible page buttons |
| `disabled` | boolean | Disable pagination |
| `show-first-last` | boolean | Show first/last buttons |
| `prev-icon` | string | Previous button icon |
| `next-icon` | string | Next button icon |

**V3 Changes:**
- Use `v-model` instead of `value`
- `@input` event → `@update:model-value`

```vue
<!-- Basic pagination -->
<v-pagination
  v-model="page"
  :length="totalPages"
/>

<!-- With first/last buttons -->
<v-pagination
  v-model="page"
  :length="totalPages"
  show-first-last
/>

<!-- Limited visible pages -->
<v-pagination
  v-model="page"
  :length="totalPages"
  :total-visible="7"
/>

<!-- With custom icons -->
<v-pagination
  v-model="page"
  :length="totalPages"
  prev-icon="mdi-chevron-left"
  next-icon="mdi-chevron-right"
/>

<!-- Circle buttons -->
<v-pagination
  v-model="page"
  :length="totalPages"
  rounded="circle"
/>
```

## Bottom Navigation

### v-bottom-navigation

Mobile-friendly bottom navigation.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Selected value |
| `color` | string | Active color |
| `grow` | boolean | Expand items to fill width |
| `bg-color` | string | Background color |
| `mode` | string | Behavior: `shift`, `hide-on-scroll` |

**V3 Changes:**
- Renamed from `v-bottom-nav` to `v-bottom-navigation`
- Use `v-model` for selection

```vue
<v-bottom-navigation v-model="selected" color="primary" grow>
  <v-btn value="home">
    <v-icon icon="mdi-home" />
    <span>Home</span>
  </v-btn>

  <v-btn value="search">
    <v-icon icon="mdi-magnify" />
    <span>Search</span>
  </v-btn>

  <v-btn value="profile">
    <v-icon icon="mdi-account" />
    <span>Profile</v-btn>
  </v-btn>
</v-bottom-navigation>

<!-- Hide on scroll -->
<v-bottom-navigation v-model="selected" mode="hide-on-scroll">
  <v-btn value="home">
    <v-icon icon="mdi-home" />
  </v-btn>
</v-bottom-navigation>

<!-- Shift mode (icon only when not selected) -->
<v-bottom-navigation v-model="selected" mode="shift">
  <v-btn value="home">
    <v-icon icon="mdi-home" />
    <span>Home</span>
  </v-btn>
</v-bottom-navigation>
```

## Footer

### v-footer

Footer area with content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Background color |
| `height` | number/string | Footer height |
| `app` | boolean | Fixed within app layout |
| `inset` | boolean | Inset from navigation drawer |
| `absolute` | boolean | Absolute position |
| `padless` | boolean | Remove padding |

```vue
<!-- Basic footer -->
<v-footer color="primary">
  <v-row justify="center" no-gutters>
    <v-col class="text-center" cols="12">
      {{ new Date().getFullYear() }} — <strong>My App</strong>
    </v-col>
  </v-row>
</v-footer>

<!-- App footer -->
<v-footer app color="primary">
  <v-col class="text-center">
    © {{ new Date().getFullYear() }} — My App
  </v-col>
</v-footer>

<!-- Footer with links -->
<v-footer color="primary">
  <v-row>
    <v-col>
      <v-list density="compact" bg-color="transparent">
        <v-list-item to="/about">About</v-list-item>
        <v-list-item to="/contact">Contact</v-list-item>
      </v-list>
    </v-col>
    <v-col>
      <v-list density="compact" bg-color="transparent">
        <v-list-item to="/privacy">Privacy</v-list-item>
        <v-list-item to="/terms">Terms</v-list-item>
      </v-list>
    </v-col>
  </v-row>
</v-footer>
```

## System Bar

### v-system-bar

Status bar for app-like appearance.

```vue
<v-system-bar color="primary">
  <span class="mr-2">My App</span>
  <v-spacer />
  <span>{{ currentTime }}</span>
  <v-icon icon="mdi-wifi" class="ml-2" />
  <v-icon icon="mdi-battery" class="ml-2" />
</v-system-bar>
```

## Common Navigation Patterns

### App Layout with All Components

```vue
<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar color="primary" app>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>My App</v-app-bar-title>
      <v-spacer />
      <v-btn icon="mdi-magnify" />
      <v-btn icon="mdi-bell" />
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list nav>
        <v-list-item to="/dashboard">
          <template #prepend>
            <v-icon icon="mdi-view-dashboard" />
          </template>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item to="/profile">
          <template #prepend>
            <v-icon icon="mdi-account" />
          </template>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="primary">
      <v-col class="text-center">
        © {{ new Date().getFullYear() }} — My App
      </v-col>
    </v-footer>

    <!-- Bottom Navigation (mobile) -->
    <v-bottom-navigation v-model="selected" app>
      <v-btn value="home">
        <v-icon icon="mdi-home" />
        <span>Home</span>
      </v-btn>
      <v-btn value="search">
        <v-icon icon="mdi-magnify" />
        <span>Search</span>
      </v-btn>
      <v-btn value="profile">
        <v-icon icon="mdi-account" />
        <span>Profile</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Drawer not closing | Use `temporary` for overlay drawers |
| Tab content not showing | Use `v-window` with `v-window-item`, not `v-tabs-items` |
| App bar overlapping content | Add `app` prop to `v-app-bar` |
| Bottom nav on desktop | Use `v-bottom-navigation` with `app` for proper layout |
| Mini drawer not expanding | Add `expand-on-hover` prop |
| Router links not working | Ensure `vue-router` is configured |
| Breadcrumbs not showing | Check `items` array has `title` and `to` properties |
| Pagination not updating | Use `v-model` and listen to `@update:model-value` |