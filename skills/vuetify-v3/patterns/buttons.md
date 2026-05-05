# Buttons Patterns

Comprehensive patterns for Vuetify V3 button components.

## Button Component

### v-btn

The primary button component for actions and navigation.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Background color (theme color or CSS color) |
| `variant` | string | Button style: `text`, `outlined`, `flat`, `elevated`, `tonal`, `plain` |
| `size` | string | Size: `x-small`, `small`, `default`, `large`, `x-large` |
| `density` | string | Density: `default`, `comfortable`, `compact` |
| `icon` | string | Icon name (MDI icon) |
| `prepend-icon` | string | Icon before text |
| `append-icon` | string | Icon after text |
| `loading` | boolean | Show loading spinner |
| `disabled` | boolean | Disable button |
| `block` | boolean | Full width button |
| `rounded` | string/boolean | Border radius: `0`, `sm`, `default`, `lg`, `xl`, `pill` |
| `elevation` | number/string | Shadow elevation (0-24) |
| `to` | string/object | Vue Router link |
| `href` | string | External link |
| `target` | string | Link target (`_blank`, `_self`, etc.) |

**V3 Changes:**
- `depressed` prop → `variant="flat"`
- `text` prop → `variant="text"`
- `outlined` prop → `variant="outlined"`
- `small`, `large`, etc. → use `size` prop or boolean props
- `active-class` → `selected-class`
- Use `icon` prop instead of slot for icon buttons

### Button Variants

```vue
<!-- Elevated (default) -->
<v-btn color="primary">Elevated Button</v-btn>

<!-- Flat (V3: variant="flat", was depressed) -->
<v-btn color="primary" variant="flat">Flat Button</v-btn>

<!-- Outlined -->
<v-btn color="primary" variant="outlined">Outlined Button</v-btn>

<!-- Text -->
<v-btn color="primary" variant="text">Text Button</v-btn>

<!-- Tonal -->
<v-btn color="primary" variant="tonal">Tonal Button</v-btn>

<!-- Plain -->
<v-btn color="primary" variant="plain">Plain Button</v-btn>
```

### Button Sizes

```vue
<v-btn size="x-small">Extra Small</v-btn>
<v-btn size="small">Small</v-btn>
<v-btn size="default">Default</v-btn>
<v-btn size="large">Large</v-btn>
<v-btn size="x-large">Extra Large</v-btn>

<!-- Or use boolean props -->
<v-btn x-small>Extra Small</v-btn>
<v-btn small>Small</v-btn>
<v-btn large>Large</v-btn>
<v-btn x-large>Extra Large</v-btn>
```

### Button Density

```vue
<v-btn density="default">Default</v-btn>
<v-btn density="comfortable">Comfortable</v-btn>
<v-btn density="compact">Compact</v-btn>
```

### Icon Buttons

```vue
<!-- Icon button with icon prop (V3 recommended) -->
<v-btn icon="mdi-home" color="primary" />

<!-- Icon button with prepend-icon -->
<v-btn prepend-icon="mdi-home" color="primary">Home</v-btn>

<!-- Icon button with append-icon -->
<v-btn append-icon="mdi-arrow-right" color="primary">Next</v-btn>

<!-- Icon button with icon slot -->
<v-btn icon color="primary">
  <v-icon icon="mdi-home" />
</v-btn>
```

### Loading State

```vue
<v-btn :loading="loading" color="primary" @click="submit">
  Submit
</v-btn>

<script setup>
import { ref } from 'vue'

const loading = ref(false)

const submit = async () => {
  loading.value = true
  await submitForm()
  loading.value = false
}
</script>
```

### Block Button

```vue
<v-btn block color="primary">Full Width Button</v-btn>
```

### Rounded Buttons

```vue
<v-btn rounded="0">Not Rounded</v-btn>
<v-btn rounded="sm">Small Rounded</v-btn>
<v-btn rounded="lg">Large Rounded</v-btn>
<v-btn rounded="xl">Extra Large Rounded</v-btn>
<v-btn rounded="pill">Pill Shaped</v-btn>
```

### Elevation

```vue
<v-btn elevation="0">No Shadow</v-btn>
<v-btn elevation="2">Small Shadow</v-btn>
<v-btn elevation="8">Medium Shadow</v-btn>
<v-btn elevation="16">Large Shadow</v-btn>
<v-btn elevation="24">Extra Large Shadow</v-btn>
```

### Router Link

```vue
<!-- Using to prop -->
<v-btn to="/home">Home</v-btn>

<!-- Using to object -->
<v-btn :to="{ name: 'user', params: { id: 123 } }">User Profile</v-btn>

<!-- With router link active class -->
<v-btn to="/home" exact>Home</v-btn>
```

### External Link

```vue
<v-btn href="https://example.com" target="_blank">
  External Link
  <v-icon end icon="mdi-open-in-new" />
</v-btn>
```

## Button Group

### v-btn-group

Group related buttons together.

```vue
<v-btn-group variant="outlined" divided>
  <v-btn>Option 1</v-btn>
  <v-btn>Option 2</v-btn>
  <v-btn>Option 3</v-btn>
</v-btn-group>

<!-- With selection (V3: v-btn-group instead of v-btn-toggle) -->
<v-btn-group v-model="selected" variant="outlined" divided mandatory>
  <v-btn value="left">
    <v-icon icon="mdi-format-align-left" />
  </v-btn>
  <v-btn value="center">
    <v-icon icon="mdi-format-align-center" />
  </v-btn>
  <v-btn value="right">
    <v-icon icon="mdi-format-align-right" />
  </v-btn>
</v-btn-group>
```

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `variant` | string | Button style: `text`, `outlined`, `flat`, `elevated`, `tonal` |
| `divided` | boolean | Add dividers between buttons |
| `mandatory` | boolean | Require one button to be selected |
| `multiple` | boolean | Allow multiple selection |

### Button Toggle (V3)

In V3, use `v-btn-group` with `v-model` for toggle behavior:

```vue
<v-btn-group v-model="selected" mandatory>
  <v-btn value="list">
    <v-icon icon="mdi-view-list" />
  </v-btn>
  <v-btn value="grid">
    <v-icon icon="mdi-view-grid" />
  </v-btn>
</v-btn-group>

<script setup>
import { ref } from 'vue'
const selected = ref('list')
</script>
```

## Floating Action Button

### v-fab

Floating action button for primary actions.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Background color |
| `icon` | string | Icon name |
| `size` | string | Size: `small`, `default`, `large` |
| `extended` | boolean | Extended FAB with text |
| `location` | string | Position: `top`, `bottom`, `left`, `right`, `start`, `end` |
| `absolute` | boolean | Absolute position |
| `app` | boolean | Fixed within app layout |

```vue
<!-- Basic FAB -->
<v-fab icon="mdi-plus" color="primary" />

<!-- FAB with text -->
<v-fab extended color="primary">
  <v-icon start icon="mdi-plus" />
  Create
</v-fab>

<!-- Positioned FAB -->
<v-fab
  icon="mdi-plus"
  color="primary"
  location="bottom end"
  absolute
/>

<!-- FAB in app layout -->
<v-fab icon="mdi-plus" color="primary" app />
```

### Speed Dial

Multiple FABs revealed from a main FAB.

```vue
<v-speed-dial v-model="fab" location="bottom end" absolute>
  <template #activator>
    <v-fab icon="mdi-plus" color="primary" />
  </template>

  <v-fab icon="mdi-pencil" color="secondary" size="small" />
  <v-fab icon="mdi-delete" color="error" size="small" />
  <v-fab icon="mdi-share" color="info" size="small" />
</v-speed-dial>

<script setup>
import { ref } from 'vue'
const fab = ref(false)
</script>
```

## Common Button Patterns

### Action Buttons

```vue
<!-- Save/Cancel pattern -->
<v-card-actions>
  <v-spacer />
  <v-btn variant="text" @click="cancel">Cancel</v-btn>
  <v-btn color="primary" @click="save">Save</v-btn>
</v-card-actions>

<!-- Delete with confirmation -->
<v-btn color="error" @click="showConfirmDialog = true">
  <v-icon start icon="mdi-delete" />
  Delete
</v-btn>

<!-- Edit button -->
<v-btn size="small" variant="outlined" color="primary">
  <v-icon start icon="mdi-pencil" />
  Edit
</v-btn>
```

### Status Buttons

```vue
<!-- Success -->
<v-btn color="success" variant="flat">
  <v-icon start icon="mdi-check" />
  Approved
</v-btn>

<!-- Warning -->
<v-btn color="warning" variant="tonal">
  <v-icon start icon="mdi-alert" />
  Pending
</v-btn>

<!-- Error -->
<v-btn color="error" variant="outlined">
  <v-icon start icon="mdi-close" />
  Rejected
</v-btn>
```

### Icon Action Buttons

```vue
<v-toolbar>
  <v-btn icon="mdi-magnify" @click="search" />
  <v-btn icon="mdi-refresh" @click="refresh" />
  <v-btn icon="mdi-dots-vertical" @click="showMenu" />
</v-toolbar>
```

### Pagination Buttons

```vue
<v-row class="align-center">
  <v-col>
    <v-btn icon="mdi-chevron-left" :disabled="page === 1" @click="prevPage" />
    <span class="mx-4">Page {{ page }} of {{ totalPages }}</span>
    <v-btn icon="mdi-chevron-right" :disabled="page === totalPages" @click="nextPage" />
  </v-col>
</v-row>
```

## Button Accessibility

```vue
<!-- Button with ARIA label -->
<v-btn icon="mdi-close" aria-label="Close dialog" @click="dialog = false" />

<!-- Button with tooltip for accessibility -->
<v-tooltip text="Save changes">
  <template #activator="{ props }">
    <v-btn icon="mdi-content-save" v-bind="props" @click="save" />
  </template>
</v-tooltip>

<!-- Button with disabled state -->
<v-btn :disabled="!isValid" @click="submit">
  Submit
</v-btn>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Button too dense | Use `density="default"` instead of `compact` |
| Icon not showing | Use `icon` prop: `icon="mdi-home"` |
| Depressed button missing | Use `variant="flat"` instead of `depressed` |
| Text button style | Use `variant="text"` instead of `text` prop |
| Outlined button style | Use `variant="outlined"` instead of `outlined` prop |
| Active class not working | Use `selected-class` instead of `active-class` |
| FAB positioning | Use `location` prop with `absolute` or `app` |
| Toggle behavior missing | Use `v-btn-group` with `v-model` |