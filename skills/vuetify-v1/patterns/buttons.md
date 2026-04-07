# Vuetify 1.5 Button Patterns

## v-btn Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `absolute` | boolean | false | Position element absolutely |
| `block` | boolean | false | Expand to 100% width |
| `color` | string | undefined | Theme color or CSS color |
| `dark` | boolean | false | Apply dark theme variant |
| `depressed` | boolean | false | Remove button box shadow |
| `disabled` | boolean | false | Disable the button |
| `fab` | boolean | false | Round floating action button |
| `fixed` | boolean | false | Position element fixed |
| `flat` | boolean | false | Remove background color (V1.5 specific!) |
| `icon` | boolean | false | Designate as icon button |
| `large` | boolean | false | Large size |
| `light` | boolean | false | Apply light theme variant |
| `loading` | boolean | false | Show loading animation |
| `outline` | boolean | false | Outline style (V1.5 specific!) |
| `ripple` | boolean/object | undefined | Apply ripple effect |
| `round` | boolean | false | Rounded edges |
| `small` | boolean | false | Small size |
| `to` | string/object | undefined | Vue Router link |

## Button Variants

### Raised (Default)

```vue
<v-btn color="primary">Primary</v-btn>
<v-btn color="secondary">Secondary</v-btn>
<v-btn color="error">Error</v-btn>
```

### Flat (No Background)

```vue
<!-- V1.5 uses 'flat', V2 uses 'text' -->
<v-btn flat>Flat Button</v-btn>
<v-btn flat color="primary">Flat Primary</v-btn>
```

### Outlined

```vue
<!-- V1.5 uses 'outline', V2 uses 'outlined' -->
<v-btn outline color="primary">Outlined</v-btn>
<v-btn outline color="error">Outlined Error</v-btn>
```

### Depressed (No Shadow)

```vue
<v-btn depressed>Depressed</v-btn>
<v-btn depressed color="primary">Depressed Primary</v-btn>
```

### Icon Button

```vue
<v-btn icon>
  <v-icon>favorite</v-icon>
</v-btn>

<v-btn icon color="primary">
  <v-icon>add</v-icon>
</v-btn>
```

### Round

```vue
<v-btn round>Rounded Button</v-btn>
<v-btn round color="primary" dark>
  <v-icon left>favorite</v-icon>
  Round with Icon
</v-btn>
```

### Block

```vue
<v-btn block color="primary">Full Width Button</v-btn>
```

### FAB (Floating Action Button)

```vue
<!-- Regular FAB -->
<v-btn fab color="primary">
  <v-icon>add</v-icon>
</v-btn>

<!-- Small FAB -->
<v-btn fab small color="secondary">
  <v-icon>edit</v-icon>
</v-btn>

<!-- Large FAB -->
<v-btn fab large color="accent">
  <v-icon>navigation</v-icon>
</v-btn>
```

## Button Sizes

| Prop | Size |
|------|------|
| `small` | 28px (36px for FAB) |
| default | 36px (56px for FAB) |
| `large` | 44px (64px for FAB) |

Note: V1.5 does NOT have `x-small` or `x-large` (those are V2 only).

## Button Colors

### Theme Colors

```vue
<v-btn color="primary">Primary</v-btn>
<v-btn color="secondary">Secondary</v-btn>
<v-btn color="accent">Accent</v-btn>
<v-btn color="error">Error</v-btn>
<v-btn color="warning">Warning</v-btn>
<v-btn color="info">Info</v-btn>
<v-btn color="success">Success</v-btn>
```

### Custom Colors

```vue
<v-btn color="#FF5722">Custom Hex</v-btn>
<v-btn color="teal">Material Color</v-btn>
<v-btn color="purple darken-2">Material Color Variant</v-btn>
```

## Icons in Buttons

### Left Icon

```vue
<v-btn color="primary">
  <v-icon left>add</v-icon>
  Add Item
</v-btn>
```

### Right Icon

```vue
<v-btn color="primary">
  Continue
  <v-icon right>arrow_forward</v-icon>
</v-btn>
```

### Icon Only

```vue
<v-btn icon color="primary">
  <v-icon>settings</v-icon>
</v-btn>
```

## Loading State

```vue
<template>
  <v-btn
    :loading="loading"
    :disabled="loading"
    color="primary"
    @click="save"
  >
    Save
  </v-btn>
</template>

<script>
export default {
  data() {
    return {
      loading: false
    }
  },
  methods: {
    async save() {
      this.loading = true
      await this.saveData()
      this.loading = false
    }
  }
}
</script>
```

## Router Links

### Named Route

```vue
<v-btn :to="{ name: 'home' }">Home</v-btn>
```

### Path Route

```vue
<v-btn to="/dashboard">Dashboard</v-btn>
```

### External Link

```vue
<v-btn href="https://example.com" target="_blank">
  External Link
</v-btn>
```

## v-btn-toggle (Button Groups)

V1.5 uses `v-btn-toggle` for grouped selection (V2 uses `v-btn-group`):

### Single Selection

```vue
<v-btn-toggle v-model="selection">
  <v-btn flat>
    <v-icon>format_align_left</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_center</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_right</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_justify</v-icon>
  </v-btn>
</v-btn-toggle>
```

### Multiple Selection

```vue
<v-btn-toggle v-model="selected" multiple>
  <v-btn flat>
    <v-icon>format_bold</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_italic</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_underlined</v-icon>
  </v-btn>
</v-btn-toggle>
```

### Mandatory Selection

```vue
<v-btn-toggle v-model="selection" mandatory>
  <v-btn flat value="left">
    <v-icon>format_align_left</v-icon>
  </v-btn>
  <v-btn flat value="center">
    <v-icon>format_align_center</v-icon>
  </v-btn>
</v-btn-toggle>
```

## Button Groups with v-toolbar

```vue
<v-toolbar>
  <v-toolbar-title>Editor</v-toolbar-title>
  <v-spacer />
  <v-btn-toggle v-model="format">
    <v-btn flat>
      <v-icon>format_bold</v-icon>
    </v-btn>
    <v-btn flat>
      <v-icon>format_italic</v-icon>
    </v-btn>
    <v-btn flat>
      <v-icon>format_underlined</v-icon>
    </v-btn>
  </v-btn-toggle>
</v-toolbar>
```

## v-speed-dial (FAB Menu)

Floating action button that reveals actions:

```vue
<v-speed-dial
  v-model="fab"
  direction="top"
  :open-on-hover="true"
>
  <v-btn
    slot="activator"
    color="primary"
    dark
    fab
    hover
    v-model="fab"
  >
    <v-icon>account_circle</v-icon>
    <v-icon>close</v-icon>
  </v-btn>
  <v-btn fab dark small color="secondary">
    <v-icon>edit</v-icon>
  </v-btn>
  <v-btn fab dark small color="accent">
    <v-icon>delete</v-icon>
  </v-btn>
</v-speed-dial>
```

## Common Button Patterns

### Form Submit

```vue
<v-form ref="form" v-model="valid">
  <!-- Form fields -->
  <v-btn
    :disabled="!valid"
    color="primary"
    @click="submit"
  >
    Submit
  </v-btn>
</v-form>
```

### Confirm/Delete Actions

```vue
<v-card-actions>
  <v-spacer />
  <v-btn flat @click="cancel">Cancel</v-btn>
  <v-btn color="error" @click="confirm">Delete</v-btn>
</v-card-actions>
```

### Toolbar Actions

```vue
<v-toolbar>
  <v-btn icon @click="refresh">
    <v-icon>refresh</v-icon>
  </v-btn>
  <v-btn icon @click="settings">
    <v-icon>settings</v-icon>
  </v-btn>
</v-toolbar>
```