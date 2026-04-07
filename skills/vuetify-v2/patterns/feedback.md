# Feedback Patterns

Comprehensive patterns for Vuetify V2 feedback components: alerts, snackbars, dialogs, and more.

## Alerts

### v-alert

Convey important information to users.

**V2 Banner Alternative:**
Vuetify V2 does not have a standalone `v-banner` component. Use `v-alert` for notifications or `v-sheet` for structural banners.

**Example (Banner style):**
```vue
<v-alert type="info" dismissible>
  This is a banner-style notification.
</v-alert>
```

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `type` | string | Contextual type: `success`, `info`, `warning`, `error` |
| `value` | boolean | Show/hide alert |
| `closable` | boolean | Add close icon |
| `prominent` | boolean | Larger icon |
| `outlined` | boolean | Outline style |
| `text` | boolean | Text style |
| `border` | string | Colored border: `left`, `right`, `top`, `bottom` |
| `dense` | boolean | Dense style |
| `icon` | string | Custom icon |

```vue
<!-- Basic alerts -->
<v-alert type="success">Success message</v-alert>
<v-alert type="info">Information message</v-alert>
<v-alert type="warning">Warning message</v-alert>
<v-alert type="error">Error message</v-alert>

<!-- Outlined -->
<v-alert type="success" outlined>Outlined alert</v-alert>

<!-- Text style -->
<v-alert type="info" text>Text alert</v-alert>

<!-- Border -->
<v-alert type="warning" border="left">Alert with left border</v-alert>

<!-- Closable -->
<v-alert type="info" closable v-model="showAlert">
  Dismissible alert
</v-alert>

<!-- Prominent -->
<v-alert type="error" prominent>
  <v-icon slot="prepend">mdi-alert-circle</v-icon>
  <span>This is an important error message</span>
</v-alert>

<!-- Custom icon -->
<v-alert type="success" icon="mdi-check-circle">
  Success with custom icon
</v-alert>
```

### Alert with Actions

```vue
<v-alert type="info" prominent>
  <v-row align="center">
    <v-col class="grow">
      New version available! Update now to get the latest features.
    </v-col>
    <v-col class="shrink">
      <v-btn color="primary" @click="update">Update</v-btn>
    </v-col>
  </v-row>
</v-alert>
```

## Snackbars

### v-snackbar

Toast notifications for transient messages.

**Key Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `v-model` | boolean | - | Show/hide snackbar |
| `timeout` | number | 6000 | Auto-hide time (0 = no auto-hide) |
| `color` | string | - | Background color |
| `bottom/top/left/right` | boolean | - | Positioning |
| `vertical` | boolean | - | Stack vertically |
| `app` | boolean | - | Respect app boundaries |
| `outlined` | boolean | - | Outlined style |
| `text` | boolean | - | Text style |
| `shaped` | boolean | - | Shaped style |

```vue
<template>
  <v-snackbar v-model="show" :timeout="3000" color="success">
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" @click="show = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data: () => ({
    show: false,
    message: ''
  }),
  methods: {
    showMessage(msg) {
      this.message = msg
      this.show = true
    }
  }
}
</script>
```

### Snackbar Service Pattern

```javascript
// store/snackbar.js
export default {
  state: {
    show: false,
    message: '',
    color: 'info',
    timeout: 3000
  },
  mutations: {
    SHOW_SNACKBAR(state, { message, color = 'info', timeout = 3000 }) {
      state.show = true
      state.message = message
      state.color = color
      state.timeout = timeout
    },
    HIDE_SNACKBAR(state) {
      state.show = false
    }
  }
}

// Usage in component
this.$store.commit('SHOW_SNACKBAR', {
  message: 'Operation successful',
  color: 'success'
})
```

### Error Handling with Snackbars

```javascript
// API error handler
async function handleApiError(error) {
  let message = 'An error occurred'
  if (error.response) {
    message = error.response.data.message || error.response.statusText
  }
  this.$store.commit('SHOW_SNACKBAR', {
    message,
    color: 'error',
    timeout: 5000
  })
}
```

## Dialogs

### v-dialog

Modal dialogs for user interaction.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | boolean | Show/hide dialog |
| `max-width` | string/number | Maximum width |
| `width` | string/number | Width |
| `persistent` | boolean | Don't close on outside click |
| `scrollable` | boolean | Scrollable content |
| `fullscreen` | boolean | Full screen |
| `hide-overlay` | boolean | Hide overlay |

```vue
<v-dialog v-model="dialog" max-width="500">
  <template v-slot:activator="{ on }">
    <v-btn color="primary" v-on="on">Open Dialog</v-btn>
  </template>
  <v-card>
    <v-card-title>Dialog Title</v-card-title>
    <v-card-text>
      Dialog content here
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="confirm">Confirm</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Confirmation Dialog

```vue
<template>
  <v-dialog v-model="show" max-width="400" persistent>
    <v-card>
      <v-card-title class="headline">
        {{ title }}
      </v-card-title>
      <v-card-text>
        {{ message }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="cancel">Cancel</v-btn>
        <v-btn color="primary" @click="confirm">Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    show: Boolean,
    title: { type: String, default: 'Confirm' },
    message: { type: String, default: 'Are you sure?' }
  },
  methods: {
    cancel() {
      this.$emit('cancel')
    },
    confirm() {
      this.$emit('confirm')
    }
  }
}
</script>
```

### Delete Confirmation Dialog

```vue
<v-dialog v-model="showDelete" max-width="400">
  <v-card>
    <v-card-title class="headline error--text">
      <v-icon left color="error">mdi-alert-circle</v-icon>
      Delete Item?
    </v-card-title>
    <v-card-text>
      This action cannot be undone. Are you sure you want to delete this item?
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="showDelete = false">Cancel</v-btn>
      <v-btn color="error" @click="deleteItem">Delete</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Form Dialog

```vue
<v-dialog v-model="showForm" max-width="600" persistent>
  <v-card>
    <v-card-title>
      <span class="headline">Edit User</span>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="editedItem.name"
          :rules="[v => !!v || 'Name is required']"
          label="Name"
        />
        <v-text-field
          v-model="editedItem.email"
          :rules="[v => /.+@.+\..+/.test(v) || 'Invalid email']"
          label="Email"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="showForm = false">Cancel</v-btn>
      <v-btn color="primary" :disabled="!valid" @click="save">
        Save
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Scrollable Dialog

```vue
<v-dialog v-model="show" scrollable max-width="500">
  <v-card>
    <v-card-title>Terms and Conditions</v-card-title>
    <v-divider />
    <v-card-text style="height: 300px;">
      <!-- Long content here -->
    </v-card-text>
    <v-divider />
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="show = false">Decline</v-btn>
      <v-btn color="primary" @click="accept">Accept</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

## Menus

### v-menu

Dropdown menus for actions.

```vue
<v-menu>
  <template v-slot:activator="{ on }">
    <v-btn icon v-on="on">
      <v-icon>mdi-dots-vertical</v-icon>
    </v-btn>
  </template>
  <v-list>
    <v-list-item @click="edit">
      <v-list-item-icon><v-icon>mdi-pencil</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Edit</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item @click="copy">
      <v-list-item-icon><v-icon>mdi-content-copy</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Copy</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider />
    <v-list-item @click="delete">
      <v-list-item-icon><v-icon>mdi-delete</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Delete</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</v-menu>
```

### Context Menu

```vue
<v-menu v-model="showMenu" :position-x="x" :position-y="y" absolute>
  <v-list>
    <v-list-item @click="action">
      <v-list-item-title>Action</v-list-item-title>
    </v-list-item>
  </v-list>
</v-menu>

<script>
export default {
  data: () => ({
    showMenu: false,
    x: 0,
    y: 0
  }),
  methods: {
    showContextMenu(e) {
      e.preventDefault()
      this.x = e.clientX
      this.y = e.clientY
      this.$nextTick(() => {
        this.showMenu = true
      })
    }
  }
}
</script>
```

## Chips and Badges

### v-chip

Small pieces of information (tags, filters, selections).

```vue
<!-- Basic chip -->
<v-chip>Basic Chip</v-chip>

<!-- Colored chip -->
<v-chip color="primary">Primary</v-chip>
<v-chip color="success">Success</v-chip>
<v-chip color="error">Error</v-chip>

<!-- Outlined -->
<v-chip outlined color="primary">Outlined</v-chip>

<!-- Closable -->
<v-chip close @click:close="remove">Closable</v-chip>

<!-- With icon -->
<v-chip color="primary">
  <v-icon left>mdi-account</v-icon>
  User
</v-chip>

<!-- Label style -->
<v-chip label>Label</v-chip>

<!-- Sizes -->
<v-chip small>Small</v-chip>
<v-chip>Default</v-chip>
<v-chip large>Large</v-chip>
```

### v-badge

Superscript/subscript on content.

```vue
<!-- Basic badge -->
<v-badge content="6">
  <v-icon>mdi-email</v-icon>
</v-badge>

<!-- Dot badge -->
<v-badge dot>
  <v-icon>mdi-email</v-icon>
</v-badge>

<!-- Colored badge -->
<v-badge content="3" color="error">
  <v-icon>mdi-bell</v-icon>
</v-badge>

<!-- Overlap -->
<v-badge content="10" overlap>
  <v-icon large>mdi-bell</v-icon>
</v-badge>

<!-- Avatar with status -->
<v-badge bordered bottom color="green" dot offset-x="10" offset-y="10">
  <v-avatar size="48">
    <v-img src="avatar.jpg" />
  </v-avatar>
</v-badge>
```

## Progress Indicators

### v-progress-circular

Circular loading indicator.

```vue
<!-- Basic -->
<v-progress-circular indeterminate />

<!-- With size and width -->
<v-progress-circular
  indeterminate
  :size="50"
  :width="5"
/>

<!-- With color -->
<v-progress-circular
  indeterminate
  color="primary"
/>

<!-- Determinate progress -->
<v-progress-circular
  :value="progress"
  color="primary"
/>

<!-- With percentage -->
<v-progress-circular
  :value="progress"
  color="primary"
>
  {{ progress }}%
</v-progress-circular>
```

### v-progress-linear

Linear progress bar.

```vue
<!-- Indeterminate -->
<v-progress-linear indeterminate />

<!-- Determinate -->
<v-progress-linear :value="progress" />

<!-- With color and height -->
<v-progress-linear
  :value="progress"
  color="primary"
  height="10"
/>

<!-- Buffer -->
<v-progress-linear
  :value="progress"
  :buffer-value="buffer"
  color="primary"
/>
```

### Skeleton Loader

Loading placeholder for content.

```vue
<v-skeleton-loader
  type="card"
/>

<!-- Types: card, article, actions, table-row, list-item, etc. -->
<v-skeleton-loader type="card-heading, list-item, list-item, actions" />

<!-- With boilerplate -->
<v-skeleton-loader
  type="card"
  :boilerplate="loading"
/>
```

## Ratings

### v-rating

Input/Display for star ratings.

**Key Props:**

| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | number | Current rating |
| `length` | number | Total stars (default 5) |
| `readonly` | boolean | Non-interactive |
| `half-increments` | boolean | Allows half-stars |

**Example:**

```vue
<v-rating v-model="rating" color="amber" length="5" half-increments></v-rating>
```

## See Also

- [Vuetify Alerts](https://vuetifyjs.com/en/components/alerts/)
- [Vuetify Snackbars](https://vuetifyjs.com/en/components/snackbars/)
- [Vuetify Dialogs](https://vuetifyjs.com/en/components/dialogs/)
- [Vuetify Progress](https://vuetifyjs.com/en/components/progress/)