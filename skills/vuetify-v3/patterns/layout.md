# Layout Patterns

Comprehensive patterns for Vuetify V3 layout components.

## App Layout

### v-app

Root component for Vuetify application.

```vue
<template>
  <v-app>
    <v-app-bar app>...</v-app-bar>
    <v-navigation-drawer app>...</v-navigation-drawer>
    <v-main>
      <v-container>...</v-container>
    </v-main>
    <v-footer app>...</v-footer>
  </v-app>
</template>
```

### v-main

Main content area that adjusts for navigation and app bar.

```vue
<v-app>
  <v-app-bar app>My App</v-app-bar>
  <v-navigation-drawer app>...</v-navigation-drawer>
  <v-main>
    <v-container>
      <router-view />
    </v-container>
  </v-main>
</v-app>
```

## Grid System

### v-container

Center and pad content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `fluid` | boolean | Full width (no padding) |
| `tag` | string | HTML tag (default: 'div') |
| `max-width` | number/string | Maximum width |

```vue
<!-- Fixed width container -->
<v-container>
  <v-row>
    <v-col>Content</v-col>
  </v-row>
</v-container>

<!-- Fluid (full width) container -->
<v-container fluid>
  <v-row>
    <v-col>Content</v-col>
  </v-row>
</v-container>

<!-- With max width -->
<v-container max-width="800">
  <v-row>
    <v-col>Content</v-col>
  </v-row>
</v-container>
```

### v-row

Row wrapper for columns.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `justify` | string | Horizontal alignment: `start`, `center`, `end`, `space-between`, `space-around`, `space-evenly` |
| `align` | string | Vertical alignment: `start`, `center`, `end`, `baseline`, `stretch` |
| `align-content` | string | Multi-line alignment: `start`, `center`, `end`, `space-between`, `space-around`, `stretch` |
| `no-gutters` | boolean | Remove gutters |
| `dense` | boolean | Reduce gutter size |
| `tag` | string | HTML tag |

```vue
<!-- Justify content -->
<v-row justify="center">
  <v-col cols="auto">Centered</v-col>
</v-row>

<!-- Align items -->
<v-row align="center" style="height: 200px;">
  <v-col>Vertically Centered</v-col>
</v-row>

<!-- No gutters -->
<v-row no-gutters>
  <v-col>No Gutter</v-col>
</v-row>

<!-- Dense row -->
<v-row dense>
  <v-col>Dense</v-col>
</v-row>

<!-- Space between -->
<v-row justify="space-between">
  <v-col>Left</v-col>
  <v-col>Right</v-col>
</v-row>
```

### v-col

Column within a row.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `cols` | string/number | Columns (1-12, auto) |
| `sm` | string/number | Columns on sm breakpoint |
| `md` | string/number | Columns on md breakpoint |
| `lg` | string/number | Columns on lg breakpoint |
| `xl` | string/number | Columns on xl breakpoint |
| `xxl` | string/number | Columns on xxl breakpoint |
| `offset` | string/number | Offset columns |
| `order` | string/number | Order |

**V3 Changes:**
- Same as V2, breakpoint props work identically

```vue
<!-- Basic column -->
<v-col cols="12">Full Width</v-col>

<!-- Responsive columns -->
<v-col cols="12" sm="6" md="4" lg="3">
  12 on xs, 6 on sm, 4 on md, 3 on lg
</v-col>

<!-- Auto width -->
<v-col cols="auto">Auto Width</v-col>

<!-- Offset -->
<v-col cols="6" offset="6">Offset by 6</v-col>

<!-- Order -->
<v-col cols="6" order="2">Second</v-col>
<v-col cols="6" order="1">First</v-col>
```

### Common Layout Patterns

```vue
<!-- Two columns -->
<v-container>
  <v-row>
    <v-col cols="6">Left</v-col>
    <v-col cols="6">Right</v-col>
  </v-row>
</v-container>

<!-- Three columns -->
<v-container>
  <v-row>
    <v-col cols="4">First</v-col>
    <v-col cols="4">Second</v-col>
    <v-col cols="4">Third</v-col>
  </v-row>
</v-container>

<!-- Sidebar + Main -->
<v-container>
  <v-row>
    <v-col cols="3">Sidebar</v-col>
    <v-col cols="9">Main Content</v-col>
  </v-row>
</v-container>

<!-- Header + Content + Footer -->
<v-container>
  <v-row>
    <v-col cols="12">Header</v-col>
  </v-row>
  <v-row>
    <v-col cols="12">Content</v-col>
  </v-row>
  <v-row>
    <v-col cols="12">Footer</v-col>
  </v-row>
</v-container>

<!-- Responsive grid -->
<v-container>
  <v-row>
    <v-col
      v-for="item in items"
      :key="item.id"
      cols="12"
      sm="6"
      md="4"
      lg="3"
    >
      <v-card>{{ item.title }}</v-card>
    </v-col>
  </v-row>
</v-container>

<!-- Centered content -->
<v-container>
  <v-row justify="center">
    <v-col cols="auto">
      <v-card>Centered</v-card>
    </v-col>
  </v-row>
</v-container>
```

## Spacing

### v-spacer

Fill available space between components.

```vue
<v-row>
  <v-col>Left</v-col>
  <v-spacer />
  <v-col>Right</v-col>
</v-row>

<!-- In toolbar -->
<v-toolbar>
  <v-toolbar-title>Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon="mdi-magnify" />
</v-toolbar>

<!-- In card actions -->
<v-card-actions>
  <v-btn>Cancel</v-btn>
  <v-spacer />
  <v-btn color="primary">Save</v-btn>
</v-card-actions>
```

## Responsive Design

### Display Utilities

```vue
<!-- Hide on breakpoint -->
<div class="d-none d-md-block">Hidden on xs, sm</div>
<div class="d-md-none">Only visible on xs, sm</div>

<!-- Show on breakpoint -->
<div class="d-none d-lg-block">Only visible on lg, xl, xxl</div>

<!-- Flex utilities -->
<div class="d-flex">
  <div>Flex Item 1</div>
  <div>Flex Item 2</div>
</div>

<!-- Flex responsive -->
<div class="d-flex flex-column flex-md-row">
  <div>Column on mobile, row on tablet+</div>
</div>
```

### Breakpoint Checks

```vue
<template>
  <v-card>
    <v-card-title v-if="smAndDown">Mobile Title</v-card-title>
    <v-card-title v-else>Desktop Title</v-card-title>
  </v-card>
</template>

<script setup>
import { useDisplay } from 'vuetify'

const { smAndDown, mdAndUp } = useDisplay()
</script>
```

## Sheet

### v-sheet

Simple styled container.

```vue
<!-- Basic sheet -->
<v-sheet>
  Content
</v-sheet>

<!-- Colored sheet -->
<v-sheet color="primary" class="pa-4">
  Primary colored sheet
</v-sheet>

<!-- Elevated sheet -->
<v-sheet elevation="8">
  Elevated sheet
</v-sheet>

<!-- Rounded sheet -->
<v-sheet rounded="lg">
  Rounded sheet
</v-sheet>

<!-- Bordered sheet -->
<v-sheet border>
  Bordered sheet
</v-sheet>
```

## Responsive

### v-responsive

Maintain aspect ratios.

```vue
<!-- 16:9 aspect ratio -->
<v-responsive aspect-ratio="16/9">
  <v-img src="image.jpg" />
</v-responsive>

<!-- 1:1 (square) -->
<v-responsive aspect-ratio="1">
  <v-img src="square.jpg" />
</v-responsive>

<!-- 4:3 -->
<v-responsive aspect-ratio="4/3">
  <v-img src="image.jpg" />
</v-responsive>

<!-- Custom height -->
<v-responsive :height="300">
  <v-img src="image.jpg" />
</v-responsive>
```

## App Layout Patterns

### Full App Layout

```vue
<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list nav>
        <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard">
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item to="/profile" prepend-icon="mdi-account">
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar color="primary" app>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>My App</v-app-bar-title>
      <v-spacer />
      <v-btn icon="mdi-magnify" />
      <v-btn icon="mdi-bell" />
      <v-menu>
        <template #activator="{ props }">
          <v-btn v-bind="props" icon="mdi-account" />
        </template>
        <v-list>
          <v-list-item to="/profile">Profile</v-list-item>
          <v-list-item @click="logout">Logout</v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="primary">
      <v-col class="text-center">
        © {{ new Date().getFullYear() }} — My App
      </v-col>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const drawer = ref(true)
</script>
```

### Two-Column Layout

```vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-title>Sidebar</v-card-title>
          <v-list>
            <v-list-item to="/page1">Page 1</v-list-item>
            <v-list-item to="/page2">Page 2</v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="12" md="9">
        <v-card>
          <v-card-title>Main Content</v-card-title>
          <v-card-text>
            <router-view />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
```

### Card Grid Layout

```vue
<template>
  <v-container>
    <v-row>
      <v-col
        v-for="item in items"
        :key="item.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card>
          <v-img :src="item.image" height="200" cover />
          <v-card-title>{{ item.title }}</v-card-title>
          <v-card-text>{{ item.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
```

### Form Layout

```vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Form</v-card-title>
          <v-card-text>
            <v-form>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field v-model="form.firstName" label="First Name" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="form.lastName" label="Last Name" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="form.email" label="Email" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="form.phone" label="Phone" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select v-model="form.country" :items="countries" label="Country" />
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="reset">Reset</v-btn>
            <v-btn color="primary" @click="submit">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Content overlapping app bar | Add `app` prop to `v-app-bar` and use `v-main` |
| Content not centered | Use `v-container` for centered content |
| Grid not responsive | Use breakpoint props: `cols`, `sm`, `md`, `lg`, `xl`, `xxl` |
| Spacing too large | Use `dense` on `v-row` or `no-gutters` |
| Flex alignment wrong | Use `justify` for horizontal, `align` for vertical |
| Responsive issues | Use `useDisplay()` composable for breakpoint checks |
| Sheet not styled | Add elevation, color, or border props |
| Aspect ratio not working | Use `v-responsive` with `aspect-ratio` prop |