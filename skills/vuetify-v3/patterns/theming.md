# Theming Patterns

Comprehensive patterns for Vuetify V3 theming and colors.

## Theme Configuration

### Basic Theme Setup

```javascript
// src/plugins/vuetify.js
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

export default createVuetify({
  theme: {
    defaultTheme: 'light', // or 'dark', 'system', or custom theme name
    themes: {
      light: {
        dark: false,
        colors: {
          background: '#FFFFFF',
          surface: '#F2F5F8',
          primary: '#1867C0',
          secondary: '#48A9A6',
          error: '#B00020',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
      dark: {
        dark: true,
        colors: {
          background: '#121212',
          surface: '#212121',
          primary: '#2196F3',
          secondary: '#48A9A6',
          error: '#CF6679',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
})
```

### Required Base Colors

| Color | Usage |
|-------|-------|
| `background` | Page background color |
| `surface` | Card/component background |
| `primary` | Primary brand color |
| `secondary` | Secondary brand color |
| `success` | Success states |
| `warning` | Warning states |
| `error` | Error states |
| `info` | Informational states |

### On-Colors Auto-generation

Vuetify automatically generates `on-*` colors for text contrast:

| Auto-generated | Usage |
|----------------|-------|
| `on-background` | Text on background |
| `on-surface` | Text on surface |
| `on-primary` | Text on primary color |
| `on-secondary` | Text on secondary color |
| `on-error` | Text on error color |
| `on-success` | Text on success color |

```css
/* Generated CSS variables */
:root {
  --v-theme-primary: 24, 103, 192;
  --v-theme-on-primary: 255, 255, 255;
}

/* Usage in custom CSS */
.my-component {
  background: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-on-primary));
}
```

## Theme Variations

### Color Variations

```javascript
createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
        },
        // Generate lighten/darken variations
        variations: {
          colors: ['primary', 'secondary'],
          lighten: 5, // Generate 5 lighten steps
          darken: 5,  // Generate 5 darken steps
        },
      },
    },
  },
})
```

Generated variations:
- `primary-lighten-5` to `primary-lighten-1`
- `primary-darken-1` to `primary-darken-5`

### Custom Themes

```javascript
createVuetify({
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme: {
        dark: false,
        colors: {
          primary: '#6200EA',
          secondary: '#03DAC6',
          accent: '#FF4081',
          background: '#FAFAFA',
          surface: '#FFFFFF',
        },
      },
    },
  },
})
```

## Dynamic Theme Switching

### useTheme Composable

```typescript
import { useTheme } from 'vuetify'

const theme = useTheme()

// Switch to specific theme
theme.change('dark')

// Cycle through themes
theme.cycle()

// Toggle between specific themes
theme.toggle(['light', 'dark'])

// Check current theme
if (theme.current.value.dark) {
  // Dark theme is active
}

// Access theme colors
const primaryColor = theme.current.value.colors.primary
```

### Theme Toggle Component

```vue
<template>
  <v-btn
    :prepend-icon="theme.current.value.dark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
    @click="toggleTheme"
  >
    {{ theme.current.value.dark ? 'Light Mode' : 'Dark Mode' }}
  </v-btn>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

const toggleTheme = () => {
  theme.toggle(['light', 'dark'])
}
</script>
```

### Persist Theme Preference

```vue
<script setup>
import { useTheme } from 'vuetify'
import { onMounted } from 'vue'

const theme = useTheme()

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    theme.change(savedTheme)
  }
})

const toggleTheme = () => {
  theme.toggle(['light', 'dark'])
  localStorage.setItem('theme', theme.current.value.dark ? 'dark' : 'light')
}
</script>
```

## Using Colors

### Component Colors

```vue
<!-- Primary color -->
<v-btn color="primary">Primary Button</v-btn>
<v-card color="primary">Primary Card</v-card>
<v-chip color="primary">Primary Chip</v-chip>

<!-- Secondary color -->
<v-btn color="secondary">Secondary Button</v-btn>

<!-- Status colors -->
<v-alert type="success">Success Alert</v-alert>
<v-alert type="warning">Warning Alert</v-alert>
<v-alert type="error">Error Alert</v-alert>
<v-alert type="info">Info Alert</v-alert>

<!-- Custom colors -->
<v-btn color="#FF5722">Custom Color</v-btn>
<v-card color="teal">Named Color</v-card>
<v-chip color="orange-darken-2">Darkened Orange</v-chip>
```

### Color Utility Classes

When enabled, Vuetify generates utility classes for theme colors:

```html
<!-- Background colors -->
<div class="bg-primary">Primary Background</div>
<div class="bg-secondary">Secondary Background</div>
<div class="bg-success">Success Background</div>

<!-- Text colors -->
<span class="text-primary">Primary Text</span>
<span class="text-secondary">Secondary Text</span>
<span class="text-error">Error Text</span>

<!-- Border colors -->
<div class="border-primary">Primary Border</div>
<div class="border-secondary">Secondary Border</div>
```

Enable in config:

```javascript
createVuetify({
  theme: {
    variations: false, // Disable variations
  },
})
```

## Material Design Colors

### Color Palettes

Vuetify includes Material Design color palettes:

```javascript
import colors from 'vuetify/util/colors'

createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: colors.purple.base,
          secondary: colors.indigo.base,
          accent: colors.pink.accent2,
        },
      },
    },
  },
})
```

### Available Color Palettes

- `red`, `pink`, `purple`, `deep-purple`, `indigo`, `blue`, `light-blue`, `cyan`
- `teal`, `green`, `light-green`, `lime`, `yellow`, `amber`, `orange`, `deep-orange`
- `brown`, `blue-grey`, `grey`
- `white`, `black`, `transparent`

### Color Shades

Each color has multiple shades:

```javascript
colors.red.lighten-5
colors.red.lighten-4
colors.red.lighten-3
colors.red.lighten-2
colors.red.lighten-1
colors.red.base
colors.red.darken-1
colors.red.darken-2
colors.red.darken-3
colors.red.darken-4

colors.red.accent-1
colors.red.accent-2
colors.red.accent-3
colors.red.accent-4
```

## Theme Provider

### Scoped Themes

```vue
<v-theme-provider theme="dark">
  <v-card>
    <v-card-title>Dark Card</v-card-title>
    <v-card-text>This card uses the dark theme.</v-card-text>
  </v-card>
</v-theme-provider>

<v-theme-provider theme="light">
  <v-card>
    <v-card-title>Light Card</v-card-title>
    <v-card-text>This card uses the light theme.</v-card-text>
  </v-card>
</v-theme-provider>
```

## Defaults Provider

### Set Component Defaults

```vue
<v-default-provider>
  <v-card>
    <!-- All v-btn inside will have color="primary" -->
    <v-btn>Primary Button</v-btn>
    <v-btn>Another Primary Button</v-btn>
  </v-card>
</v-default-provider>

<!-- With specific defaults -->
<v-default-provider :defaults="{ VBtn: { color: 'secondary', variant: 'outlined' } }">
  <v-btn>Secondary Outlined</v-btn>
</v-default-provider>
```

## Breakpoints

### Default Breakpoints

| Name | Min | Max |
|------|-----|-----|
| `xs` | 0px | 599px |
| `sm` | 600px | 959px |
| `md` | 960px | 1279px |
| `lg` | 1280px | 1919px |
| `xl` | 1920px | 2559px |
| `xxl` | 2560px | - |

### useDisplay Composable

```typescript
import { useDisplay } from 'vuetify'

const { xs, sm, md, lg, xl, xxl } = useDisplay()

// Boolean checks
if (xs.value) {
  // Extra small screen
}

// Ranges
const { smAndDown, mdAndUp, lgOnly } = useDisplay()

if (smAndDown.value) {
  // Mobile (xs or sm)
}

if (mdAndUp.value) {
  // Tablet and desktop (md, lg, xl, xxl)
}

// Current breakpoint name
const { name } = useDisplay()
console.log(name.value) // 'xs', 'sm', 'md', 'lg', 'xl', 'xxl'

// Current width
const { width, height } = useDisplay()
console.log(width.value, height.value)
```

### Responsive Props

```vue
<!-- Column responsive -->
<v-col cols="12" sm="6" md="4" lg="3">
  <!-- 12 columns on xs, 6 on sm, 4 on md, 3 on lg -->
</v-col>

<!-- Hide on mobile -->
<div class="d-none d-md-block">Hidden on mobile</div>

<!-- Show only on mobile -->
<div class="d-md-none">Only visible on mobile</div>

<!-- Conditional rendering -->
<v-card v-if="smAndDown">
  Mobile Card
</v-card>
<v-card v-else>
  Desktop Card
</v-card>
```

## Custom CSS Variables

### Access Theme Variables

```css
/* In your CSS */
:root {
  --my-custom-color: rgb(var(--v-theme-primary));
}

.my-component {
  background-color: var(--my-custom-color);
  color: rgb(var(--v-theme-on-primary));
}

/* With opacity */
.overlay {
  background-color: rgba(var(--v-theme-primary), 0.5);
}
```

### Vue Component Styles

```vue
<template>
  <v-card class="custom-card">
    <v-card-title>Custom Styled Card</v-card-title>
  </v-card>
</template>

<style scoped>
.custom-card {
  background-color: rgb(var(--v-theme-surface));
  border: 2px solid rgb(var(--v-theme-primary));
}

.custom-card:hover {
  background-color: rgba(var(--v-theme-primary), 0.1);
}
</style>
```

## Dark Mode Patterns

### System Preference Detection

```javascript
import { createVuetify } from 'vuetify'

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'system', // Automatically detect system preference
    themes: {
      light: { /* ... */ },
      dark: { /* ... */ },
    },
  },
})
```

### Custom Dark Mode Toggle

```vue
<template>
  <v-switch
    v-model="isDark"
    :prepend-icon="isDark ? 'mdi-weather-night' : 'mdi-weather-sunny'"
    label="Dark Mode"
    @update:model-value="toggleDark"
  />
</template>

<script setup>
import { useTheme } from 'vuetify'
import { computed } from 'vue'

const theme = useTheme()

const isDark = computed(() => theme.current.value.dark)

const toggleDark = () => {
  theme.toggle(['light', 'dark'])
}
</script>
```

### Custom Light/Dark Colors

```javascript
createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          background: '#FAFAFA',
          surface: '#FFFFFF',
          primary: '#1867C0',
        },
      },
      dark: {
        colors: {
          background: '#121212', // Material Design dark background
          surface: '#212121',     // Surface color
          primary: '#2196F3',     // Lighter primary for dark mode
        },
      },
    },
  },
})
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Colors not updating | Check theme configuration and use `useTheme()` composable |
| Dark mode not working | Use `defaultTheme: 'dark'` or `theme.change('dark')` |
| Custom color not applied | Use hex (`#FF5722`) or named color (`teal`) format |
| Theme not persisting | Save to `localStorage` and restore on mount |
| Breakpoints not working | Import and use `useDisplay()` composable |
| On-colors not generated | Ensure `primary`/`secondary` colors are defined |
| CSS variables not working | Use `rgb(var(--v-theme-primary))` format |
| Theme provider not working | Ensure nested components use theme values |