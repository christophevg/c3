# Vuetify 1.5 Feedback Patterns

## v-alert

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | string | undefined | Background color |
| `dark` | boolean | false | Dark theme |
| `dismissible` | boolean | false | Show close button |
| `icon` | string | - | Icon name |
| `light` | boolean | false | Light theme |
| `outline` | boolean | false | Outlined style |
| `transition` | string | 'scale-transition' | Transition name |
| `type` | string | - | Type: 'success', 'info', 'warning', 'error' |
| `value` | boolean | true | Visibility |

### Basic Alerts

```vue
<v-alert type="success">Success message</v-alert>
<v-alert type="info">Info message</v-alert>
<v-alert type="warning">Warning message</v-alert>
<v-alert type="error">Error message</v-alert>
```

### Custom Color

```vue
<v-alert color="purple" dark>
  Custom colored alert
</v-alert>
```

### Outlined Alert

```vue
<v-alert outline type="error">
  Outlined error alert
</v-alert>
```

### Dismissible Alert

```vue
<template>
  <v-alert
    v-model="show"
    dismissible
    type="success"
    @input="onClose"
  >
    Operation completed successfully
  </v-alert>
</template>

<script>
export default {
  data() {
    return { show: true }
  },
  methods: {
    onClose() {
      console.log('Alert dismissed')
    }
  }
}
</script>
```

### Alert with Icon

```vue
<v-alert type="info" icon="info">
  <v-icon slot="icon">info</v-icon>
  Custom icon alert
</v-alert>
```

## v-snackbar

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `absolute` | boolean | false | Position absolutely |
| `app` | boolean | false | Respect app layout |
| `auto-height` | boolean | false | Auto height |
| `bottom` | boolean | false | Position bottom |
| `color` | string | undefined | Background color |
| `dark` | boolean | false | Dark theme |
| `left` | boolean | false | Position left |
| `light` | boolean | false | Light theme |
| `multi-line` | boolean | false | Multi-line mode |
| `right` | boolean | false | Position right |
| `timeout` | number | 6000 | Auto-close timeout (ms) |
| `top` | boolean | false | Position top |
| `value` | boolean | false | Visibility |
| `vertical` | boolean | false | Vertical layout |

### Basic Snackbar

```vue
<template>
  <div>
    <v-btn @click="snackbar = true">Show Snackbar</v-btn>
    <v-snackbar v-model="snackbar">
      Message sent successfully
      <v-btn flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return { snackbar: false }
  }
}
</script>
```

### Positioned Snackbar

```vue
<v-snackbar v-model="snackbar" top right>
  Positioned top-right
  <v-btn flat color="pink" @click="snackbar = false">Close</v-btn>
</v-snackbar>
```

### Multi-line Snackbar

```vue
<v-snackbar v-model="snackbar" multi-line>
  This is a longer message that spans multiple lines.
  <v-btn flat @click="snackbar = false">Close</v-btn>
</v-snackbar>
```

### Vertical Snackbar

```vue
<v-snackbar v-model="snackbar" vertical>
  Vertical layout snackbar
  <v-btn flat @click="snackbar = false">Close</v-btn>
</v-snackbar>
```

### Colored Snackbar

```vue
<v-snackbar v-model="snackbar" color="success">
  Success message
  <v-btn flat @click="snackbar = false">Close</v-btn>
</v-snackbar>
```

### No Timeout

```vue
<v-snackbar v-model="snackbar" :timeout="-1">
  This won't auto-close
  <v-btn flat @click="snackbar = false">Close</v-btn>
</v-snackbar>
```

## v-dialog (V1.5 Activator Syntax)

**CRITICAL**: V1.5 uses `slot="activator"` syntax (different from V2's `v-slot:activator`).

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `attach` | any | false | Attach to element |
| `content-class` | string | - | Custom content class |
| `dark` | boolean | false | Dark theme |
| `disabled` | boolean | false | Disable dialog |
| `full-width` | boolean | false | 100% width |
| `fullscreen` | boolean | false | Fullscreen mode |
| `hide-overlay` | boolean | false | Hide overlay |
| `lazy` | boolean | false | Lazy render |
| `light` | boolean | false | Light theme |
| `max-width` | number/string | - | Maximum width |
| `no-click-animation` | boolean | false | Disable bounce |
| `origin` | string | 'center center' | Transition origin |
| `persistent` | boolean | false | No outside-click dismiss |
| `scrollable` | boolean | false | Enable scrolling |
| `transition` | string | 'dialog-transition' | Transition name |
| `value` | boolean | - | Visibility |
| `width` | number/string | - | Width |

### Basic Dialog (V1.5 Syntax)

```vue
<template>
  <div>
    <v-dialog v-model="dialog" max-width="500">
      <v-btn slot="activator" color="primary">Open Dialog</v-btn>
      <v-card>
        <v-card-title class="headline">Dialog Title</v-card-title>
        <v-card-text>
          Dialog content goes here.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn flat @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="dialog = false">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return { dialog: false }
  }
}
</script>
```

### Persistent Dialog

```vue
<v-dialog v-model="dialog" persistent max-width="500">
  <v-btn slot="activator">Open</v-btn>
  <v-card>
    <v-card-title>Cannot Close by Clicking Outside</v-card-title>
    <v-card-actions>
      <v-btn @click="dialog = false">Close</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Fullscreen Dialog

```vue
<v-dialog v-model="dialog" fullscreen>
  <v-btn slot="activator">Open Fullscreen</v-btn>
  <v-card>
    <v-toolbar>
      <v-btn icon @click="dialog = false">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>Fullscreen Dialog</v-toolbar-title>
    </v-toolbar>
    <v-card-text>Content here</v-card-text>
  </v-card>
</v-dialog>
```

### Scrollable Dialog

```vue
<v-dialog v-model="dialog" scrollable max-width="500">
  <v-btn slot="activator">Open</v-btn>
  <v-card>
    <v-card-title>Select Country</v-card-title>
    <v-card-text style="max-height: 300px">
      <v-radio-group v-model="selected" column>
        <v-radio
          v-for="country in countries"
          :key="country.code"
          :label="country.name"
          :value="country.code"
        />
      </v-radio-group>
    </v-card-text>
    <v-card-actions>
      <v-btn flat @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="select">Select</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Confirmation Dialog

```vue
<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title class="headline">Confirm Delete</v-card-title>
      <v-card-text>
        Are you sure you want to delete this item? This action cannot be undone.
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn flat @click="dialog = false">Cancel</v-btn>
        <v-btn color="error" @click="confirm">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
```

### Dialog Without Activator

```vue
<template>
  <div>
    <v-btn @click="openDialog">Open</v-btn>
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-title>Dialog</v-card-title>
        <v-card-actions>
          <v-btn @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return { dialog: false }
  },
  methods: {
    openDialog() {
      this.dialog = true
    }
  }
}
</script>
```

## v-menu (V1.5 Activator Syntax)

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `absolute` | boolean | false | Absolute positioning |
| `activator` | any | - | Custom activator |
| `allow-overflow` | boolean | false | Allow overflow |
| `auto` | boolean | false | Auto center |
| `bottom` | boolean | false | Position bottom |
| `close-delay` | number | 0 | Close delay (ms) |
| `close-on-click` | boolean | true | Close on outside click |
| `close-on-content-click` | boolean | true | Close on content click |
| `disabled` | boolean | false | Disabled state |
| `full-width` | boolean | false | Full width |
| `left` | boolean | false | Position left |
| `max-height` | number/string | auto | Max height |
| `max-width` | number/string | auto | Max width |
| `min-width` | number/string | - | Min width |
| `nudge-bottom` | number | 0 | Nudge from bottom |
| `nudge-left` | number | 0 | Nudge from left |
| `nudge-right` | number | 0 | Nudge from right |
| `nudge-top` | number | 0 | Nudge from top |
| `nudge-width` | number | 0 | Nudge width |
| `offset-x` | boolean | false | Offset on X axis |
| `offset-y` | boolean | false | Offset on Y axis |
| `open-delay` | number | 0 | Open delay (ms) |
| `open-on-click` | boolean | true | Open on click |
| `open-on-hover` | boolean | false | Open on hover |
| `origin` | string | 'top left' | Transition origin |
| `position-x` | number | - | X position (no activator) |
| `position-y` | number | - | Y position (no activator) |
| `right` | boolean | false | Position right |
| `top` | boolean | false | Position top |
| `transition` | string | - | Transition name |
| `value` | boolean | - | Visibility |
| `z-index` | number | - | Z-index |

### Basic Menu (V1.5 Syntax)

```vue
<v-menu offset-y>
  <v-btn slot="activator">
    Menu
    <v-icon>arrow_drop_down</v-icon>
  </v-btn>
  <v-list>
    <v-list-tile @click="action1">
      <v-list-tile-title>Action 1</v-list-tile-title>
    </v-list-tile>
    <v-list-tile @click="action2">
      <v-list-tile-title>Action 2</v-list-tile-title>
    </v-list-tile>
  </v-list>
</v-menu>
```

### Menu with Icons

```vue
<v-menu offset-y>
  <v-btn slot="activator" icon>
    <v-icon>more_vert</v-icon>
  </v-btn>
  <v-list>
    <v-list-tile @click="edit">
      <v-list-tile-action>
        <v-icon>edit</v-icon>
      </v-list-tile-action>
      <v-list-tile-content>
        <v-list-tile-title>Edit</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
    <v-list-tile @click="delete">
      <v-list-tile-action>
        <v-icon>delete</v-icon>
      </v-list-tile-action>
      <v-list-tile-content>
        <v-list-tile-title>Delete</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
  </v-list>
</v-menu>
```

### Hover Menu

```vue
<v-menu open-on-hover offset-y>
  <v-btn slot="activator">Hover Menu</v-btn>
  <v-list>
    <v-list-tile>
      <v-list-tile-title>Option 1</v-list-tile-title>
    </v-list-tile>
    <v-list-tile>
      <v-list-tile-title>Option 2</v-list-tile-title>
    </v-list-tile>
  </v-list>
</v-menu>
```

## v-tooltip

### Basic Tooltip (V1.5 Syntax)

```vue
<v-tooltip bottom>
  <v-btn slot="activator" icon>
    <v-icon>help</v-icon>
  </v-btn>
  <span>Tooltip text</span>
</v-tooltip>
```

### Positioned Tooltips

```vue
<v-tooltip top>
  <v-btn slot="activator">Top</v-btn>
  <span>Top tooltip</span>
</v-tooltip>

<v-tooltip bottom>
  <v-btn slot="activator">Bottom</v-btn>
  <span>Bottom tooltip</span>
</v-tooltip>

<v-tooltip left>
  <v-btn slot="activator">Left</v-btn>
  <span>Left tooltip</span>
</v-tooltip>

<v-tooltip right>
  <v-btn slot="activator">Right</v-btn>
  <span>Right tooltip</span>
</v-tooltip>
```

## v-badge

```vue
<v-badge left overlap color="primary">
  <v-icon slot="badge">notifications</v-icon>
  <v-icon large>mail</v-icon>
</v-badge>

<v-badge color="error">
  <span slot="badge">5</span>
  <v-icon>shopping_cart</v-icon>
</v-badge>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `bottom` | boolean | false | Position bottom |
| `color` | string | 'primary' | Badge color |
| `left` | boolean | false | Position left |
| `overlap` | boolean | false | Overlap badge |
| `value` | boolean | true | Visibility |

## Progress Indicators

### Circular Progress

```vue
<v-progress-circular
  :value="75"
  :size="100"
  :width="5"
  color="primary"
>
  75%
</v-progress-circular>

<!-- Indeterminate -->
<v-progress-circular
  indeterminate
  color="primary"
/>
```

### Linear Progress

```vue
<v-progress-linear
  :value="50"
  color="primary"
/>

<!-- Indeterminate -->
<v-progress-linear
  indeterminate
  color="primary"
/>

<!-- Query mode -->
<v-progress-linear
  :active="loading"
  :indeterminate="true"
  query
/>
```

### Linear Progress Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `active` | boolean | true | Active state |
| `background-color` | string | - | Background color |
| `buffer-value` | number | 100 | Buffer value |
| `color` | string | 'primary' | Progress color |
| `height` | number/string | 4 | Height |
| `indeterminate` | boolean | false | Indeterminate mode |
| `query` | boolean | false | Query mode |
| `value` | number | - | Progress value |