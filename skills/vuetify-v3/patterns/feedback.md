# Feedback Patterns

Comprehensive patterns for Vuetify V3 feedback components.

## Alerts

### v-alert

Important messages for warnings, errors, and success states.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `type` | string | Alert type: `success`, `info`, `warning`, `error` |
| `variant` | string | Style: `elevated`, `flat`, `tonal`, `outlined`, `text`, `plain` |
| `color` | string | Custom background color |
| `density` | string | Density: `default`, `comfortable`, `compact` |
| `title` | string | Alert title |
| `text` | string | Alert text content |
| `closable` | boolean | Show close button |
| `icon` | string | Custom icon |
| `border` | string | Border position: `start`, `end`, `top`, `bottom` |
| `prominent` | boolean | Larger icon and text |

**V3 Changes:**
- `dismissible` prop → `closable`
- `outlined` prop → `variant="outlined"`
- `text` prop → `variant="text"` (conflicts with `text` content prop)

```vue
<!-- Success alert -->
<v-alert type="success">
  Operation completed successfully.
</v-alert>

<!-- Error alert -->
<v-alert type="error">
  An error occurred while processing your request.
</v-alert>

<!-- Warning alert -->
<v-alert type="warning">
  This action cannot be undone.
</v-alert>

<!-- Info alert -->
<v-alert type="info">
  New features are available.
</v-alert>

<!-- Closable alert -->
<v-alert
  v-model="alert"
  closable
  type="info"
  title="Information"
  text="This alert can be dismissed."
/>

<!-- Alert with custom icon -->
<v-alert
  type="info"
  icon="mdi-bell"
>
  Custom icon alert.
</v-alert>

<!-- Outlined alert -->
<v-alert type="success" variant="outlined">
  Outlined alert style.
</v-alert>

<!-- Tonal alert -->
<v-alert type="info" variant="tonal">
  Tonal alert style.
</v-alert>

<!-- Prominent alert -->
<v-alert type="warning" prominent>
  Prominent alert with larger icon.
</v-alert>

<!-- Alert with border -->
<v-alert type="info" border="start">
  Alert with left border.
</v-alert>

<!-- Alert with title -->
<v-alert
  type="success"
  title="Success"
  text="Your changes have been saved."
/>
```

## Snackbars

### v-snackbar

Toast notifications for brief messages.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | boolean | Control visibility |
| `color` | string | Background color |
| `timeout` | number | Auto-close timeout (ms), -1 for no timeout |
| `location` | string | Position: `top`, `bottom`, `start`, `end`, `top start`, etc. |
| `multi-line` | boolean | Multi-line text |
| `vertical` | boolean | Vertical layout |
| `elevation` | number | Shadow elevation |
| `rounded` | string/boolean | Border radius |

**V3 Changes:**
- `top`, `bottom`, `left`, `right` props → use `location` prop
- Use `v-model` instead of `value`

```vue
<!-- Basic snackbar -->
<v-snackbar v-model="snackbar">
  {{ message }}
  <template #actions>
    <v-btn
      color="pink"
      variant="text"
      @click="snackbar = false"
    >
      Close
    </v-btn>
  </template>
</v-snackbar>

<!-- Positioned snackbar -->
<v-snackbar
  v-model="snackbar"
  location="top end"
>
  Top right snackbar.
</v-snackbar>

<!-- Persistent snackbar -->
<v-snackbar
  v-model="snackbar"
  :timeout="-1"
>
  This snackbar won't auto-close.
  <template #actions>
    <v-btn @click="snackbar = false">Close</v-btn>
  </template>
</v-snackbar>

<!-- Multi-line snackbar -->
<v-snackbar
  v-model="snackbar"
  multi-line
>
  <div>
    Line 1<br>
    Line 2
  </div>
</v-snackbar>

<!-- Colored snackbar -->
<v-snackbar
  v-model="snackbar"
  color="success"
>
  Success message!
</v-snackbar>

<!-- With actions -->
<v-snackbar v-model="snackbar">
  File deleted.
  <template #actions>
    <v-btn
      color="primary"
      variant="text"
      @click="undo"
    >
      Undo
    </v-btn>
    <v-btn
      variant="text"
      @click="snackbar = false"
    >
      Close
    </v-btn>
  </template>
</v-snackbar>

<script setup>
import { ref } from 'vue'

const snackbar = ref(false)
const message = ref('Hello!')

const showSnackbar = (msg) => {
  message.value = msg
  snackbar.value = true
}
</script>
```

## Badges

### v-badge

Notifications and counts on elements.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `content` | string/number | Badge content |
| `color` | string | Badge color |
| `dot` | boolean | Dot badge (no content) |
| `floating` | boolean | Float above element |
| `inline` | boolean | Inline with content |
| `location` | string | Position: `top end`, `bottom start`, etc. |
| `bordered` | boolean | Border around badge |

**V3 Changes:**
- Use `content` prop instead of default slot for badge content
- `overlap` prop removed (use `floating` instead)

```vue
<!-- Badge on icon -->
<v-badge content="6" color="error">
  <v-icon icon="mdi-bell" />
</v-badge>

<!-- Dot badge -->
<v-badge dot color="success">
  <v-icon icon="mdi-account" />
</v-badge>

<!-- Floating badge -->
<v-badge content="99+" floating color="error">
  <v-icon icon="mdi-email" />
</v-badge>

<!-- Bordered badge -->
<v-badge content="5" bordered color="primary">
  <v-icon icon="mdi-cart" />
</v-badge>

<!-- Inline badge -->
<v-badge content="new" inline color="success">
  Feature
</v-badge>

<!-- Badge on avatar -->
<v-badge
  dot
  location="bottom end"
  color="success"
  bordered
>
  <v-avatar image="avatar.jpg" />
</v-badge>

<!-- Badge on button -->
<v-badge content="3" color="error">
  <v-btn icon="mdi-cart" />
</v-badge>
```

## Dialogs

### v-dialog

Modal dialogs for focused content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | boolean | Control visibility |
| `max-width` | number/string | Maximum width |
| `width` | number/string | Width |
| `persistent` | boolean | Don't close on outside click |
| `fullscreen` | boolean | Fullscreen dialog |
| `scrollable` | boolean | Enable scrolling |
| `transition` | string | Transition name |

**V3 Changes:**
- Activator slot: `{ on, attrs }` → `{ props }`
- Use `v-model` instead of `value`

```vue
<!-- Dialog with activator (V3 syntax) -->
<v-dialog v-model="dialog">
  <template #activator="{ props }">
    <v-btn color="primary" v-bind="props">
      Open Dialog
    </v-btn>
  </template>

  <v-card>
    <v-card-title>Dialog Title</v-card-title>
    <v-card-text>
      Dialog content goes here.
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="save">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<script setup>
import { ref } from 'vue'

const dialog = ref(false)

const save = () => {
  // Save logic
  dialog.value = false
}
</script>

<!-- Persistent dialog -->
<v-dialog v-model="dialog" persistent>
  <v-card>
    <v-card-title>Confirm Action</v-card-title>
    <v-card-text>
      This action cannot be undone. Are you sure?
    </v-card-text>
    <v-card-actions>
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="error" @click="confirm">Confirm</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<!-- Fullscreen dialog -->
<v-dialog v-model="dialog" fullscreen>
  <v-card>
    <v-toolbar>
      <v-btn icon @click="dialog = false">
        <v-icon icon="mdi-close" />
      </v-btn>
      <v-toolbar-title>Fullscreen Dialog</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      Fullscreen content.
    </v-card-text>
  </v-card>
</v-dialog>

<!-- Scrollable dialog -->
<v-dialog v-model="dialog" scrollable max-width="500">
  <v-card>
    <v-card-title>Scrollable Content</v-card-title>
    <v-card-text style="height: 300px;">
      <!-- Long content here -->
    </v-card-text>
    <v-card-actions>
      <v-btn @click="dialog = false">Close</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<!-- Confirmation dialog pattern -->
<v-dialog v-model="confirmDialog" max-width="400">
  <v-card>
    <v-card-title class="text-h5">
      Confirm Delete
    </v-card-title>
    <v-card-text>
      Are you sure you want to delete this item? This action cannot be undone.
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="confirmDialog = false">Cancel</v-btn>
      <v-btn color="error" @click="deleteItem">Delete</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

## Menus

### v-menu

Dropdown menu for actions.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | boolean | Control visibility |
| `location` | string | Position: `bottom`, `top`, `start`, `end`, etc. |
| `offset` | number/array | Offset from activator |
| `close-on-content-click` | boolean | Close on item click |
| `transition` | string | Transition name |

**V3 Changes:**
- Activator slot: `{ on, attrs }` → `{ props }`

```vue
<!-- Basic menu (V3 syntax) -->
<v-menu>
  <template #activator="{ props }">
    <v-btn v-bind="props">
      <span>Options</span>
      <v-icon end icon="mdi-chevron-down" />
    </v-btn>
  </template>

  <v-list>
    <v-list-item @click="action1">
      <v-list-item-title>Action 1</v-list-item-title>
    </v-list-item>
    <v-list-item @click="action2">
      <v-list-item-title>Action 2</v-list-item-title>
    </v-list-item>
    <v-divider />
    <v-list-item @click="action3">
      <v-list-item-title>Action 3</v-list-item-title>
    </v-list-item>
  </v-list>
</v-menu>

<!-- Menu with icons -->
<v-menu>
  <template #activator="{ props }">
    <v-btn icon="mdi-dots-vertical" v-bind="props" />
  </template>

  <v-list>
    <v-list-item @click="edit">
      <template #prepend>
        <v-icon icon="mdi-pencil" />
      </template>
      <v-list-item-title>Edit</v-list-item-title>
    </v-list-item>
    <v-list-item @click="delete">
      <template #prepend>
        <v-icon icon="mdi-delete" />
      </template>
      <v-list-item-title>Delete</v-list-item-title>
    </v-list-item>
  </v-list>
</v-menu>

<!-- Positioned menu -->
<v-menu location="bottom end">
  <template #activator="{ props }">
    <v-btn v-bind="props">Bottom Right</v-btn>
  </template>
  <v-list>
    <v-list-item>Option 1</v-list-item>
    <v-list-item>Option 2</v-list-item>
  </v-list>
</v-menu>

<!-- Menu with offset -->
<v-menu :offset="[0, 10]">
  <template #activator="{ props }">
    <v-btn v-bind="props">With Offset</v-btn>
  </template>
  <v-list>
    <v-list-item>Option 1</v-list-item>
  </v-list>
</v-menu>
```

## Tooltips

### v-tooltip

Additional information on hover.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `text` | string | Tooltip text |
| `location` | string | Position: `top`, `bottom`, `start`, `end` |
| `open-delay` | number | Delay before showing (ms) |
| `close-delay` | number | Delay before hiding (ms) |

**V3 Changes:**
- Activator slot: `{ on, attrs }` → `{ props }`
- `text` prop instead of default slot for text content

```vue
<!-- Basic tooltip (V3 syntax) -->
<v-tooltip text="Edit item">
  <template #activator="{ props }">
    <v-btn icon="mdi-pencil" v-bind="props" />
  </template>
</v-tooltip>

<!-- Tooltip with custom location -->
<v-tooltip text="Save changes" location="bottom">
  <template #activator="{ props }">
    <v-btn icon="mdi-content-save" v-bind="props" />
  </template>
</v-tooltip>

<!-- Tooltip on icon button -->
<v-tooltip text="Delete">
  <template #activator="{ props }">
    <v-btn icon="mdi-delete" color="error" v-bind="props" />
  </template>
</v-tooltip>

<!-- Tooltip with delay -->
<v-tooltip text="Info" :open-delay="500">
  <template #activator="{ props }">
    <v-icon icon="mdi-information" v-bind="props" />
  </template>
</v-tooltip>
```

## Banners

### v-banner

Announcements and important messages.

```vue
<v-banner
  text="This feature is deprecated and will be removed in version 3.0"
  color="warning"
  :sticky="true"
  lines="one"
>
  <template #actions>
    <v-btn @click="dismiss">Dismiss</v-btn>
  </template>
</v-banner>

<!-- Banner with icon -->
<v-banner
  text="Your subscription expires in 7 days"
  color="info"
  lines="one"
>
  <template #prepend>
    <v-icon icon="mdi-bell" />
  </template>
  <template #actions>
    <v-btn @click="renew">Renew</v-btn>
    <v-btn @click="dismiss">Dismiss</v-btn>
  </template>
</v-banner>
```

## Skeleton Loader

### v-skeleton-loader

Loading state placeholders.

```vue
<!-- Card skeleton -->
<v-card>
  <v-skeleton-loader type="card" />
</v-card>

<!-- List item skeleton -->
<v-list>
  <v-skeleton-loader type="list-item" />
  <v-skeleton-loader type="list-item" />
  <v-skeleton-loader type="list-item" />
</v-list>

<!-- Table skeleton -->
<v-skeleton-loader type="table" />

<!-- Custom skeleton types -->
<v-skeleton-loader type="card-avatar, actions" />

<v-skeleton-loader type="article, actions" />

<!-- Skeleton while loading -->
<v-card v-if="loading">
  <v-skeleton-loader type="card" />
</v-card>
<v-card v-else>
  <v-card-title>{{ title }}</v-card-title>
  <v-card-text>{{ content }}</v-card-text>
</v-card>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const data = ref(null)

onMounted(async () => {
  data.value = await fetchData()
  loading.value = false
})
</script>
```

## Progress Indicators

### v-progress-circular

Circular progress indicator.

```vue
<!-- Indeterminate -->
<v-progress-circular indeterminate color="primary" />

<!-- Determinate -->
<v-progress-circular
  :model-value="progress"
  color="primary"
/>

<!-- With size -->
<v-progress-circular
  :model-value="progress"
  size="64"
  width="6"
  color="primary"
/>

<!-- With rotate -->
<v-progress-circular
  :model-value="progress"
  :rotate="-90"
  color="primary"
/>
```

### v-progress-linear

Linear progress indicator.

```vue
<!-- Indeterminate -->
<v-progress-linear indeterminate color="primary" />

<!-- Determinate -->
<v-progress-linear :model-value="progress" color="primary" />

<!-- With height -->
<v-progress-linear
  :model-value="progress"
  height="10"
  color="primary"
/>

<!-- Striped -->
<v-progress-linear
  :model-value="progress"
  striped
  color="primary"
/>

<!-- With buffer (streaming) -->
<v-progress-linear
  :model-value="progress"
  :buffer-value="buffer"
  color="primary"
/>

<!-- Query mode (background task) -->
<v-progress-linear
  :model-value="progress"
  query
  color="primary"
/>
```

## Rating

### v-rating

User feedback rating.

```vue
<!-- Basic rating -->
<v-rating v-model="rating" />

<!-- With colors -->
<v-rating
  v-model="rating"
  color="yellow-darken-3"
  background-color="grey-lighten-1"
/>

<!-- Half increments -->
<v-rating
  v-model="rating"
  half-increments
  hover
/>

<!-- Readonly -->
<v-rating
  v-model="rating"
  readonly
/>

<!-- Custom length -->
<v-rating
  v-model="rating"
  :length="10"
/>

<!-- With custom icons -->
<v-rating
  v-model="rating"
  :empty-icon="mdiHeartOutline"
  :full-icon="mdiHeart"
  color="red"
/>

<!-- Small rating -->
<v-rating
  v-model="rating"
  density="compact"
  size="small"
/>
```

## Hover

### v-hover

Detect hover state on elements.

```vue
<v-hover v-slot="hover">
  <v-card
    :elevation="hover ? 12 : 2"
    :class="{ 'on-hover': hover }"
  >
    <v-card-title>Hover Card</v-card-title>
  </v-card>
</v-hover>

<!-- Hover with transition -->
<v-hover v-slot="hover">
  <v-card
    :elevation="hover ? 8 : 2"
    class="transition-elevation"
  >
    <v-card-title>Card with Hover Effect</v-card-title>
  </v-card>
</v-hover>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Dialog not closing | Add `v-model` and set to false |
| Snackbar timeout too short | Increase `timeout` prop (default 5000ms) |
| Tooltip not showing | Ensure activator template has `v-bind="props"` |
| Alert not dismissible | Add `closable` prop |
| Menu position wrong | Use `location` prop with correct value |
| Badge position wrong | Use `location` prop (e.g., `bottom end`) |
| Skeleton not loading | Check `type` prop has correct type name |
| Progress not updating | Use `v-model` or `model-value` prop |