# Theming Patterns

Comprehensive patterns for Vuetify V2 theming, colors, and styling.

## Theme Configuration

### Basic Setup

```javascript
// src/plugins/vuetify.js
import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    dark: false, // Default theme (false = light)
    themes: {
      light: {
        primary: '#1867C0',
        secondary: '#48A9A6',
        accent: '#82B1FF',
        error: '#B00020',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00'
      },
      dark: {
        primary: '#2196F3',
        secondary: '#54B6B2',
        accent: '#FFC107',
        error: '#B00020',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00'
      }
    },
    options: {
      customProperties: true // Enables CSS variables
    }
  },
  icons: {
    iconfont: 'mdi' // Material Design Icons
  }
})
```

### Custom Theme Colors

```javascript
export default new Vuetify({
  theme: {
    themes: {
      light: {
        // Standard colors
        primary: '#1867C0',
        secondary: '#48A9A6',
        accent: '#82B1FF',
        error: '#B00020',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00',
        // Custom colors
        background: '#F5F5F5',
        surface: '#FFFFFF',
        text: '#212121',
        textSecondary: '#757575',
        border: '#E0E0E0'
      }
    }
  }
})
```

### Theme Options

| Option | Description |
|--------|-------------|
| `dark` | Default theme mode |
| `themes.light` | Light theme colors |
| `themes.dark` | Dark theme colors |
| `options.customProperties` | Generate CSS variables |
| `options.themeCache` | Cache theme for performance |

## Using Colors

### In Component Props

```vue
<!-- Theme colors -->
<v-btn color="primary">Primary</v-btn>
<v-btn color="secondary">Secondary</v-btn>
<v-btn color="accent">Accent</v-btn>
<v-btn color="error">Error</v-btn>
<v-btn color="info">Info</v-btn>
<v-btn color="success">Success</v-btn>
<v-btn color="warning">Warning</v-btn>

<!-- Custom colors -->
<v-btn color="#FF5722">Custom Color</v-btn>
<v-btn color="indigo">Named Color</v-btn>

<!-- Color variations -->
<v-btn color="primary lighten-2">Lighter</v-btn>
<v-btn color="primary darken-2">Darker</v-btn>
```

### CSS Classes

```html
<!-- Background colors -->
<div class="primary">Primary background</div>
<div class="secondary">Secondary background</div>
<div class="error">Error background</div>

<!-- Text colors -->
<div class="primary--text">Primary text color</div>
<div class="secondary--text">Secondary text color</div>
<div class="error--text">Error text color</div>

<!-- Color variations -->
<div class="primary lighten-2">Lighter background</div>
<div class="primary--text text--lighten-2">Lighter text</div>
```

### CSS Variables (with `customProperties: true`)

```css
.my-component {
  color: var(--v-primary-base);
  background-color: var(--v-secondary-base);
  border-color: var(--v-primary-darken2);
}

/* Light/dark theme */
.my-component {
  background-color: var(--v-surface-base);
  color: var(--v-text-base);
}
```

### In JavaScript

```javascript
// Get theme color
const primaryColor = this.$vuetify.theme.currentTheme.primary

// Set theme color
this.$vuetify.theme.themes.light.primary = '#1976D2'

// Check if dark mode
if (this.$vuetify.theme.dark) {
  // Dark mode is active
}
```

## Dark Mode

### Toggle Dark Mode

```vue
<template>
  <v-btn icon @click="toggleDarkMode">
    <v-icon>{{ $vuetify.theme.dark ? 'mdi-brightness-7' : 'mdi-brightness-4' }}</v-icon>
  </v-btn>
</template>

<script>
export default {
  methods: {
    toggleDarkMode() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
      // Persist preference
      localStorage.setItem('darkMode', this.$vuetify.theme.dark)
    }
  },
  mounted() {
    // Restore preference
    const darkMode = localStorage.getItem('darkMode')
    if (darkMode !== null) {
      this.$vuetify.theme.dark = darkMode === 'true'
    }
  }
}
</script>
```

### System Preference

```javascript
// Use system preference for dark mode
export default new Vuetify({
  theme: {
    options: {
      customProperties: true
    }
  }
})

// In component
mounted() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  this.$vuetify.theme.dark = prefersDark

  // Listen for changes
  window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', e => {
      this.$vuetify.theme.dark = e.matches
    })
}
```

## Material Design Colors

Vuetify includes the full Material Design color palette.

### Available Colors

| Color | Variations |
|-------|------------|
| red | lighten-5 to darken-4, accent-1 to accent-4 |
| pink | lighten-5 to darken-4, accent-1 to accent-4 |
| purple | lighten-5 to darken-4, accent-1 to accent-4 |
| deep-purple | lighten-5 to darken-4, accent-1 to accent-4 |
| indigo | lighten-5 to darken-4, accent-1 to accent-4 |
| blue | lighten-5 to darken-4, accent-1 to accent-4 |
| light-blue | lighten-5 to darken-4, accent-1 to accent-4 |
| cyan | lighten-5 to darken-4, accent-1 to accent-4 |
| teal | lighten-5 to darken-4, accent-1 to accent-4 |
| green | lighten-5 to darken-4, accent-1 to accent-4 |
| light-green | lighten-5 to darken-4, accent-1 to accent-4 |
| lime | lighten-5 to darken-4, accent-1 to accent-4 |
| yellow | lighten-5 to darken-4, accent-1 to accent-4 |
| amber | lighten-5 to darken-4, accent-1 to accent-4 |
| orange | lighten-5 to darken-4, accent-1 to accent-4 |
| deep-orange | lighten-5 to darken-4, accent-1 to accent-4 |
| brown | lighten-5 to darken-4 |
| blue-grey | lighten-5 to darken-4 |
| grey | lighten-5 to darken-4 |
| white | - |
| black | - |

### Using Color Variations

```html
<!-- Background colors -->
<div class="red">Red</div>
<div class="red lighten-3">Light Red</div>
<div class="red darken-3">Dark Red</div>
<div class="red accent-3">Red Accent</div>

<!-- Text colors -->
<div class="red--text">Red Text</div>
<div class="red--text text--lighten-3">Light Red Text</div>
<div class="red--text text--darken-3">Dark Red Text</div>

<!-- In components -->
<v-btn color="indigo darken-3">Dark Indigo</v-btn>
<v-card color="blue-grey lighten-4">Light Blue Grey</v-card>
```

## Spacing

### Margin and Padding Classes

Format: `{property}{direction}-{size}`

- **Property**: `m` (margin), `p` (padding)
- **Direction**: `t` (top), `b` (bottom), `l` (left), `r` (right), `x` (left+right), `y` (top+bottom), `a` (all)
- **Size**: 0-12, n1-n12 for negative

| Size | Pixels |
|------|--------|
| 0 | 0px |
| 1 | 4px |
| 2 | 8px |
| 3 | 12px |
| 4 | 16px |
| 5 | 20px |
| 6 | 24px |
| 7 | 28px |
| 8 | 32px |
| 9 | 36px |
| 10 | 40px |
| 11 | 44px |
| 12 | 48px |

```html
<!-- Padding -->
<div class="pa-4">Padding all sides 16px</div>
<div class="px-2 py-4">Padding horizontal 8px, vertical 16px</div>
<div class="pt-2 pb-4">Padding top 8px, bottom 16px</div>

<!-- Margin -->
<div class="ma-2">Margin all sides 8px</div>
<div class="mx-auto">Center horizontally</div>
<div class="my-4">Margin vertical 16px</div>

<!-- Negative margin -->
<div class="ml-n2">Negative margin left -8px</div>
<div class="mt-n4">Negative margin top -16px</div>
```

## Typography

### Text Classes

```html
<!-- Headings -->
<h1 class="text-h1">Heading 1</h1>
<h2 class="text-h2">Heading 2</h2>
<h3 class="text-h3">Heading 3</h3>
<h4 class="text-h4">Heading 4</h4>
<h5 class="text-h5">Heading 5</h5>
<h6 class="text-h6">Heading 6</h6>

<!-- Subtitles -->
<div class="text-subtitle-1">Subtitle 1</div>
<div class="text-subtitle-2">Subtitle 2</div>

<!-- Body -->
<div class="text-body-1">Body 1</div>
<div class="text-body-2">Body 2</div>

<!-- Button text -->
<div class="text-button">Button Text</div>

<!-- Caption and overline -->
<div class="text-caption">Caption Text</div>
<div class="text-overline">Overline Text</div>
```

### Text Alignment

```html
<div class="text-left">Left aligned</div>
<div class="text-center">Center aligned</div>
<div class="text-right">Right aligned</div>
<div class="text-justify">Justified text</div>
```

### Text Transform

```html
<div class="text-lowercase">lowercase text</div>
<div class="text-uppercase">UPPERCASE TEXT</div>
<div class="text-capitalize">Capitalize Text</div>
```

### Text Weight

```html
<div class="font-weight-thin">Thin</div>
<div class="font-weight-light">Light</div>
<div class="font-weight-regular">Regular</div>
<div class="font-weight-medium">Medium</div>
<div class="font-weight-bold">Bold</div>
<div class="font-weight-black">Black</div>
```

### Text Truncation

```html
<div class="text-truncate">Long text that will be truncated...</div>
<div class="text-no-wrap">Text that won't wrap</div>
```

## Elevation

Shadow depth classes (0-24):

```html
<div class="elevation-0">No shadow</div>
<div class="elevation-1">Slight shadow</div>
<div class="elevation-2">Light shadow</div>
<div class="elevation-4">Medium shadow</div>
<div class="elevation-8">Strong shadow</div>
<div class="elevation-16">Very strong shadow</div>
<div class="elevation-24">Maximum shadow</div>
```

## Border Radius

```html
<div class="rounded-0">No border radius</div>
<div class="rounded-sm">Small border radius</div>
<div class="rounded">Default border radius</div>
<div class="rounded-lg">Large border radius</div>
<div class="rounded-xl">Extra large border radius</div>
<div class="rounded-circle">Circle</div>
<div class="rounded-pill">Pill shape</div>

<!-- Directional -->
<div class="rounded-t-lg">Top corners only</div>
<div class="rounded-b-lg">Bottom corners only</div>
<div class="rounded-l-lg">Left corners only</div>
<div class="rounded-r-lg">Right corners only</div>
```

## Display

```html
<!-- Display -->
<div class="d-none">Hidden</div>
<div class="d-inline">Inline</div>
<div class="d-inline-block">Inline block</div>
<div class="d-block">Block</div>
<div class="d-flex">Flex</div>
<div class="d-inline-flex">Inline flex</div>

<!-- Responsive display -->
<div class="d-none d-sm-block">Hidden on xs, visible on sm+</div>
<div class="d-md-none">Visible on xs and sm only</div>

<!-- Responsive examples -->
<div class="hidden-sm-and-down">Hidden on sm and smaller</div>
<div class="hidden-md-and-up">Hidden on md and larger</div>
<div class="hidden-sm-only">Hidden only on sm</div>
```

## Flexbox

```html
<!-- Justify -->
<div class="d-flex justify-start">Start</div>
<div class="d-flex justify-end">End</div>
<div class="d-flex justify-center">Center</div>
<div class="d-flex justify-space-between">Space between</div>
<div class="d-flex justify-space-around">Space around</div>

<!-- Align items -->
<div class="d-flex align-start">Start</div>
<div class="d-flex align-end">End</div>
<div class="d-flex align-center">Center</div>
<div class="d-flex align-baseline">Baseline</div>
<div class="d-flex align-stretch">Stretch</div>

<!-- Flex direction -->
<div class="d-flex flex-row">Row</div>
<div class="d-flex flex-column">Column</div>
<div class="d-flex flex-row-reverse">Row reverse</div>
<div class="d-flex flex-column-reverse">Column reverse</div>

<!-- Flex wrap -->
<div class="d-flex flex-wrap">Wrap</div>
<div class="d-flex flex-nowrap">No wrap</div>
```

## See Also

- [Vuetify Theming](https://vuetifyjs.com/en/features/theme/)
- [Vuetify Colors](https://vuetifyjs.com/en/features/theme/)
- [Vuetify Typography](https://vuetifyjs.com/en/styles/typography/)
- [Vuetify Spacing](https://vuetifyjs.com/en/framework/spacing/)