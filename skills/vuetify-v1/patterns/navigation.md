# Vuetify 1.5 Navigation Patterns

## v-toolbar (V1 uses v-toolbar, V2 uses v-app-bar)

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `absolute` | boolean | false | Position absolutely |
| `app` | boolean | false | Part of app layout |
| `card` | boolean | false | Remove elevation |
| `clipped-left` | boolean | false | Clip for left drawer |
| `clipped-right` | boolean | false | Clip for right drawer |
| `color` | string | undefined | Theme color |
| `dark` | boolean | false | Dark theme |
| `dense` | boolean | false | Dense mode |
| `extended` | boolean | false | Extension slot |
| `extension-height` | number/string | 48 | Extension height |
| `fixed` | boolean | false | Position fixed |
| `flat` | boolean | false | Remove elevation |
| `floating` | boolean | false | Floating style |
| `height` | number/string | 56 | Toolbar height |
| `light` | boolean | false | Light theme |
| `prominent` | boolean | false | Prominent mode |
| `scroll-off-screen` | boolean | false | Hide on scroll |
| `scroll-target` | string | - | Scroll target selector |
| `scroll-threshold` | number | 300 | Scroll threshold |

### Basic Toolbar

```vue
<v-toolbar>
  <v-toolbar-side-icon @click="drawer = !drawer" />
  <v-toolbar-title>App Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon>
    <v-icon>search</v-icon>
  </v-btn>
  <v-btn icon>
    <v-icon>more_vert</v-icon>
  </v-btn>
</v-toolbar>
```

### Toolbar with Tabs

```vue
<v-toolbar extended>
  <v-toolbar-side-icon />
  <v-toolbar-title>Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon><v-icon>search</v-icon></v-btn>

  <v-tabs slot="extension" v-model="tab" grow>
    <v-tab>Tab 1</v-tab>
    <v-tab>Tab 2</v-tab>
    <v-tab>Tab 3</v-tab>
  </v-tabs>
</v-toolbar>
```

### Dense Toolbar

```vue
<v-toolbar dense>
  <v-toolbar-title>Compact Toolbar</v-toolbar-title>
</v-toolbar>
```

### Prominent Toolbar

```vue
<v-toolbar prominent extended>
  <v-toolbar-side-icon />
  <v-toolbar-title>Larger Toolbar</v-toolbar-title>
</v-toolbar>
```

## v-navigation-drawer

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `absolute` | boolean | false | Position absolutely |
| `app` | boolean | false | Part of app layout |
| `clipped` | boolean | false | Clip under toolbar |
| `dark` | boolean | false | Dark theme |
| `disable-route-watcher` | boolean | false | Disable route watch |
| `fixed` | boolean | false | Position fixed |
| `floating` | boolean | false | No visible border |
| `height` | number/string | 100% | Drawer height |
| `hide-overlay` | boolean | false | Hide overlay |
| `light` | boolean | false | Light theme |
| `mini-variant` | boolean | false | Mini collapsed mode |
| `mini-variant-width` | number/string | 80 | Mini width |
| `mobile-break-point` | number/string | 1264 | Mobile breakpoint |
| `permanent` | boolean | false | Always visible |
| `right` | boolean | false | Right position |
| `stateless` | boolean | false | No automatic state |
| `temporary` | boolean | false | Overlay mode |
| `touchless` | boolean | false | Disable touch |
| `value` | any | - | Visibility |
| `width` | number/string | 300 | Drawer width |

### Drawer Types

```vue
<!-- Temporary (overlay) -->
<v-navigation-drawer v-model="drawer" temporary app>
  <v-list>...</v-list>
</v-navigation-drawer>

<!-- Permanent (always visible) -->
<v-navigation-drawer permanent app>
  <v-list>...</v-list>
</v-navigation-drawer>

<!-- Mini Variant -->
<v-navigation-drawer
  v-model="drawer"
  :mini-variant.sync="mini"
  permanent
  app
>
  <v-list>...</v-list>
</v-navigation-drawer>

<!-- Clipped (under toolbar) -->
<v-navigation-drawer clipped app>
  <v-list>...</v-list>
</v-navigation-drawer>
```

### App Layout Pattern

```vue
<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list>
        <v-list-tile to="/">
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar app clipped-left>
      <v-toolbar-side-icon @click="drawer = !drawer" />
      <v-toolbar-title>My App</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>

    <v-footer app>
      <span>&copy; 2024</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: null
    }
  }
}
</script>
```

## v-tabs

### Basic Tabs

```vue
<v-tabs v-model="activeTab">
  <v-tab>Tab One</v-tab>
  <v-tab>Tab Two</v-tab>
  <v-tab>Tab Three</v-tab>

  <v-tabs-items v-model="activeTab">
    <v-tab-item>Content One</v-tab-item>
    <v-tab-item>Content Two</v-tab-item>
    <v-tab-item>Content Three</v-tab-item>
  </v-tabs-items>
</v-tabs>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `active` | number | - | Active tab index |
| `align-with-title` | boolean | false | Align with toolbar title |
| `color` | string | undefined | Background color |
| `dark` | boolean | false | Dark theme |
| `fixed-tabs` | boolean | false | Fixed width tabs |
| `grow` | boolean | false | Expand to fill |
| `height` | number/string | undefined | Custom height |
| `hide-slider` | boolean | false | Hide slider |
| `icons-and-text` | boolean | false | Show icons above text |
| `light` | boolean | false | Light theme |
| `mobile-break-point` | number | 1264 | Mobile breakpoint |
| `next-icon` | string | '$vuetify.icons.next' | Next icon |
| `prev-icon` | string | '$vuetify.icons.prev' | Previous icon |
| `right` | boolean | false | Align right |
| `show-arrows` | boolean | false | Show navigation arrows |
| `slider-color` | string | 'primary' | Slider color |

### Tabs with Icons

```vue
<v-tabs icons-and-text centered>
  <v-tab>
    Profile
    <v-icon>account_circle</v-icon>
  </v-tab>
  <v-tab>
    Settings
    <v-icon>settings</v-icon>
  </v-tab>
  <v-tab>
    Messages
    <v-icon>message</v-icon>
  </v-tab>
</v-tabs>
```

### Centered Tabs

```vue
<v-tabs centered grow>
  <v-tab>Home</v-tab>
  <v-tab>About</v-tab>
  <v-tab>Contact</v-tab>
</v-tabs>
```

## v-bottom-nav (V1 naming, V2 uses v-bottom-navigation)

```vue
<v-bottom-nav :value="true" fixed app>
  <v-btn color="primary" flat value="recent">
    <span>Recent</span>
    <v-icon>history</v-icon>
  </v-btn>
  <v-btn color="primary" flat value="favorites">
    <span>Favorites</span>
    <v-icon>favorite</v-icon>
  </v-btn>
  <v-btn color="primary" flat value="nearby">
    <span>Nearby</span>
    <v-icon>place</v-icon>
  </v-btn>
</v-bottom-nav>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `active` | number | - | Active button |
| `app` | boolean | false | Part of app layout |
| `color` | string | undefined | Background color |
| `dark` | boolean | false | Dark theme |
| `fixed` | boolean | false | Position fixed |
| `height` | number/string | 56 | Height |
| `light` | boolean | false | Light theme |
| `shift` | boolean | false | Shift on hover |
| `value` | any | - | Visibility |

## v-breadcrumbs

```vue
<v-breadcrumbs>
  <v-breadcrumbs-item to="/">Home</v-breadcrumbs-item>
  <v-breadcrumbs-divider>/</v-breadcrumbs-divider>
  <v-breadcrumbs-item to="/products">Products</v-breadcrumbs-item>
  <v-breadcrumbs-divider>/</v-breadcrumbs-divider>
  <v-breadcrumbs-item disabled>Details</v-breadcrumbs-item>
</v-breadcrumbs>
```

### With Items Array

```vue
<v-breadcrumbs :items="items" divider="/">
  <template slot="item" slot-scope="props">
    <v-breadcrumbs-item
      :to="props.item.to"
      :disabled="props.item.disabled"
    >
      {{ props.item.text }}
    </v-breadcrumbs-item>
  </template>
</v-breadcrumbs>

<script>
export default {
  data() {
    return {
      items: [
        { text: 'Home', to: '/', disabled: false },
        { text: 'Products', to: '/products', disabled: false },
        { text: 'Details', to: '/products/1', disabled: true }
      ]
    }
  }
}
</script>
```

## v-pagination

```vue
<v-pagination
  v-model="page"
  :length="totalPages"
  :total-visible="7"
  @input="onPageChange"
/>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `circle` | boolean | false | Circular buttons |
| `color` | string | 'primary' | Button color |
| `dark` | boolean | false | Dark theme |
| `disabled` | boolean | false | Disabled state |
| `length` | number | - | Total pages (required) |
| `light` | boolean | false | Light theme |
| `next-icon` | string | '$vuetify.icons.next' | Next icon |
| `prev-icon` | string | '$vuetify.icons.prev' | Previous icon |
| `total-visible` | number | - | Visible buttons |
| `value` | number | - | Current page |

## v-stepper (Multi-Step Forms)

```vue
<v-stepper v-model="step">
  <v-stepper-header>
    <v-stepper-step :complete="step > 1" step="1">
      Step 1
    </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 2" step="2">
      Step 2
    </v-stepper-step>
    <v-divider />
    <v-stepper-step step="3">Step 3</v-stepper-step>
  </v-stepper-header>

  <v-stepper-items>
    <v-stepper-content step="1">
      <v-card>
        <v-card-text>Step 1 content</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="step = 2">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>

    <v-stepper-content step="2">
      <v-card>
        <v-card-text>Step 2 content</v-card-text>
        <v-card-actions>
          <v-btn flat @click="step = 1">Back</v-btn>
          <v-btn color="primary" @click="step = 3">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>

    <v-stepper-content step="3">
      <v-card>
        <v-card-text>Step 3 content</v-card-text>
        <v-card-actions>
          <v-btn flat @click="step = 2">Back</v-btn>
          <v-btn color="primary" @click="submit">Finish</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>
  </v-stepper-items>
</v-stepper>
```

### Vertical Stepper

```vue
<v-stepper v-model="step" vertical>
  <v-stepper-step :complete="step > 1" step="1">
    Select campaign
    <small>Choose your campaign</small>
  </v-stepper-step>
  <v-stepper-content step="1">
    <!-- Content -->
    <v-btn color="primary" @click="step = 2">Continue</v-btn>
  </v-stepper-content>

  <v-stepper-step :complete="step > 2" step="2">
    Create ad
  </v-stepper-step>
  <v-stepper-content step="2">
    <!-- Content -->
    <v-btn flat @click="step = 1">Back</v-btn>
    <v-btn color="primary" @click="step = 3">Continue</v-btn>
  </v-stepper-content>
</v-stepper>
```