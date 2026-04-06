# Layout Patterns

Comprehensive patterns for Vuetify V2 grid system and responsive layout.

## Grid System

Vuetify uses a 12-column grid system with responsive breakpoints.

### Basic Structure

```vue
<v-container>
  <v-row>
    <v-col cols="12">
      <!-- Full width -->
    </v-col>
  </v-row>
</v-container>
```

### v-container

Wraps content and centers it horizontally.

| Prop | Type | Description |
|------|------|-------------|
| `fluid` | boolean | Full-width container |
| `tag` | string | HTML tag (default: `div`) |

```vue
<!-- Centered container (max-width: 1200px) -->
<v-container>
  <!-- Content -->
</v-container>

<!-- Full-width container -->
<v-container fluid>
  <!-- Content -->
</v-container>
```

### v-row

Wrapper for columns with alignment options.

| Prop | Values | Description |
|------|--------|-------------|
| `align` | `start`, `center`, `end`, `baseline`, `stretch` | Vertical alignment |
| `justify` | `start`, `center`, `end`, `space-between`, `space-around` | Horizontal alignment |
| `no-gutters` | boolean | Remove column gutters |
| `dense` | boolean | Reduce column spacing |

```vue
<!-- Centered content -->
<v-row align="center" justify="center">
  <v-col cols="6">Centered</v-col>
</v-row>

<!-- Space between columns -->
<v-row justify="space-between">
  <v-col cols="3">Left</v-col>
  <v-col cols="3">Right</v-col>
</v-row>
```

### v-col

Content holder with responsive column spans.

| Prop | Values | Description |
|------|--------|-------------|
| `cols` | 1-12, "auto" | Default columns (xs breakpoint) |
| `sm` | 1-12, "auto" | Small screens (≥600px) |
| `md` | 1-12, "auto" | Medium screens (≥960px) |
| `lg` | 1-12, "auto" | Large screens (≥1264px) |
| `xl` | 1-12, "auto" | Extra large screens (≥1904px) |
| `offset` | 0-12 | Column offset |
| `order` | 1-12 | Order within row |

```vue
<!-- Responsive columns -->
<v-row>
  <v-col cols="12" sm="6" md="4" lg="3">
    <!-- Full width on mobile
         Half on small screens
         1/3 on medium screens
         1/4 on large screens -->
  </v-col>
</v-row>

<!-- Offset columns -->
<v-row>
  <v-col cols="8" offset="2">
    <!-- 8 columns wide, offset by 2 -->
  </v-col>
</v-row>

<!-- Ordering -->
<v-row>
  <v-col cols="4" order="2">First in code, second visually</v-col>
  <v-col cols="4" order="1">Second in code, first visually</v-col>
</v-row>

<!-- Auto sizing -->
<v-row>
  <v-col cols="auto">Auto-sized</v-col>
  <v-col>Remaining space</v-col>
</v-row>
```

### v-spacer

Flexible spacing between elements.

```vue
<v-row>
  <v-col cols="auto">Left</v-col>
  <v-spacer />
  <v-col cols="auto">Right</v-col>
</v-row>

<!-- In toolbars and cards -->
<v-toolbar>
  <v-toolbar-title>Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon><v-icon>mdi-cog</v-icon></v-btn>
</v-toolbar>
```

## Breakpoints

| Breakpoint | Code | Range | Devices |
|------------|------|-------|---------|
| Extra small | `xs` | < 600px | Phones |
| Small | `sm` | ≥ 600px | Tablets |
| Medium | `md` | ≥ 960px | Small laptops |
| Large | `lg` | ≥ 1264px | Laptops/desktops |
| Extra large | `xl` | ≥ 1904px | Large desktops |

### Key Behaviors

1. **No `xs` prop** - Use `cols` for smallest screens
2. **"And up" behavior** - Props apply to that size and larger
3. **12-column system** - Total columns per row = 12

## Common Layout Patterns

### Two-Column Layout

```vue
<v-container>
  <v-row>
    <v-col cols="12" md="8">
      <h2>Main Content</h2>
      <!-- Content -->
    </v-col>
    <v-col cols="12" md="4">
      <h3>Sidebar</h3>
      <!-- Sidebar -->
    </v-col>
  </v-row>
</v-container>
```

### Three-Column Layout

```vue
<v-container>
  <v-row>
    <v-col cols="12" md="4">Column 1</v-col>
    <v-col cols="12" md="4">Column 2</v-col>
    <v-col cols="12" md="4">Column 3</v-col>
  </v-row>
</v-container>
```

### Dashboard Grid

```vue
<v-container fluid>
  <v-row dense>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 1</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 2</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 3</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 4</v-card>
    </v-col>
  </v-row>

  <v-row>
    <v-col cols="12" lg="8">
      <v-card>Main Content</v-card>
    </v-col>
    <v-col cols="12" lg="4">
      <v-card>Side Panel</v-card>
    </v-col>
  </v-row>
</v-container>
```

### Centered Content

```vue
<v-container fill-height>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card>
        <v-card-title>Centered Card</v-card-title>
      </v-card>
    </v-col>
  </v-row>
</v-container>
```

### Equal Height Columns

Use `v-row` with `align="stretch"` (default):

```vue
<v-row>
  <v-col cols="4">
    <v-card>Short content</v-card>
  </v-col>
  <v-col cols="4">
    <v-card>Much longer content that takes more space</v-card>
  </v-col>
  <v-col cols="4">
    <v-card>Short content</v-card>
  </v-col>
</v-row>
```

### Nested Grids

```vue
<v-container>
  <v-row>
    <v-col cols="12" md="8">
      <v-row>
        <v-col cols="6">Nested 1</v-col>
        <v-col cols="6">Nested 2</v-col>
      </v-row>
    </v-col>
    <v-col cols="12" md="4">
      Sidebar
    </v-col>
  </v-row>
</v-container>
```

## Application Layout

### Full App Layout

```vue
<v-app>
  <!-- Navigation Drawer -->
  <v-navigation-drawer app v-model="drawer" clipped>
    <v-list>
      <v-list-item to="/">
        <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <!-- App Bar -->
  <v-app-bar app clipped-left color="primary" dark>
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-toolbar-title>App Title</v-toolbar-title>
    <v-spacer />
    <v-btn icon><v-icon>mdi-cog</v-icon></v-btn>
  </v-app-bar>

  <!-- Main Content -->
  <v-main>
    <v-container fluid>
      <router-view />
    </v-container>
  </v-main>

  <!-- Footer -->
  <v-footer app>
    <span>&copy; 2024</span>
  </v-footer>
</v-app>
```

### App Bar with Tabs

```vue
<v-app-bar app color="primary" dark>
  <v-app-bar-nav-icon @click="drawer = !drawer" />
  <v-toolbar-title>Page Title</v-toolbar-title>

  <template v-slot:extension>
    <v-tabs v-model="tab" background-color="primary" dark>
      <v-tab href="#tab-1">Tab 1</v-tab>
      <v-tab href="#tab-2">Tab 2</v-tab>
      <v-tab href="#tab-3">Tab 3</v-tab>
    </v-tabs>
  </template>
</v-app-bar>
```

## Responsive Visibility

### Display Helpers

```vue
<!-- Show only on specific breakpoints -->
<div class="hidden-sm-and-down">Hidden on sm and smaller</div>
<div class="hidden-md-and-up">Hidden on md and larger</div>
<div class="hidden-sm-only">Hidden only on sm</div>

<!-- Show only on specific breakpoints -->
<div class="hidden-xs-only">Not visible on xs</div>
<div class="hidden-lg-and-up">Not visible on lg and xl</div>
```

### Conditional Rendering

```vue
<template>
  <div>
    <!-- Only render on mobile -->
    <div v-if="$vuetify.breakpoint.mobile">
      Mobile view
    </div>

    <!-- Only render on desktop -->
    <div v-if="$vuetify.breakpoint.lgAndUp">
      Desktop view
    </div>

    <!-- Different layouts based on breakpoint -->
    <v-row>
      <v-col :cols="$vuetify.breakpoint.mobile ? 12 : 6">
        Dynamic column width
      </v-col>
    </v-row>
  </div>
</template>
```

## Spacing

Vuetify uses spacing classes: `{property}{direction}-{size}`

- **Property**: `m` (margin), `p` (padding)
- **Direction**: `t` (top), `b` (bottom), `l` (left), `r` (right), `x` (left+right), `y` (top+bottom), `a` (all)
- **Size**: 0-12 (4px increments: 0=0px, 1=4px, 2=8px, etc.)

```vue
<!-- Padding -->
<div class="pa-4">Padding all sides 16px</div>
<div class="px-2 py-4">Padding horizontal 8px, vertical 16px</div>

<!-- Margin -->
<div class="ma-2">Margin all sides 8px</div>
<div class="mt-4 mb-2">Margin top 16px, bottom 8px</div>

<!-- Negative margin -->
<div class="ml-n2">Negative margin left -8px</div>
```

## See Also

- [Vuetify Grid System](https://vuetifyjs.com/en/framework/grid)
- [Vuetify Display Helpers](https://vuetifyjs.com/en/framework/display)
- [Vuetify Spacing Helpers](https://vuetifyjs.com/en/framework/spacing)