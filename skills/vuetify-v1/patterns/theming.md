# Vuetify 1.5 Theming Patterns

## Theme Configuration

### Basic Setup

```javascript
// main.js
import Vue from 'vue'
import Vuetify from 'vuetify'

Vue.use(Vuetify, {
  theme: {
    primary: '#1976D2',
    secondary: '#424242',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107'
  }
})
```

### Using Material Color Palette

```javascript
import Vue from 'vue'
import Vuetify from 'vuetify'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
  theme: {
    primary: colors.purple.base,
    secondary: colors.grey.darken1,
    accent: colors.pink.accent2,
    error: colors.red.base,
    warning: colors.amber.base,
    info: colors.blue.base,
    success: colors.green.base
  }
})
```

### Color Object Structure

```javascript
// Each color has these variants
colors.purple = {
  base: '#9C27B0',
  lighten5: '#F3E5F5',
  lighten4: '#E1BEE7',
  lighten3: '#CE93D8',
  lighten2: '#BA68C8',
  lighten1: '#AB47BC',
  darken1: '#8E24AA',
  darken2: '#7B1FA2',
  darken3: '#6A1B9A',
  darken4: '#4A148C',
  accent1: '#EA80FC',
  accent2: '#E040FB',
  accent3: '#D500F9',
  accent4: '#AA00FF'
}
```

### Dark Mode

```javascript
// Enable dark mode globally
Vue.use(Vuetify, {
  theme: {
    dark: true,
    themes: {
      dark: {
        primary: '#21CFF3',
        secondary: '#424242',
        accent: '#FF4081',
        error: '#FF5252'
      },
      light: {
        primary: '#1976D2',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252'
      }
    }
  }
})
```

## Runtime Theme Changes

### Toggle Dark Mode

```vue
<template>
  <v-btn @click="toggleDark">
    <v-icon>{{ dark ? 'brightness_3' : 'brightness_5' }}</v-icon>
  </v-btn>
</template>

<script>
export default {
  computed: {
    dark() {
      return this.$vuetify.theme.dark
    }
  },
  methods: {
    toggleDark() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
    }
  }
}
</script>
```

### Change Theme Color

```javascript
// Change a theme color at runtime
this.$vuetify.theme.primary = '#4CAF50'

// Change with theme object
this.$vuetify.theme.themes.light.primary = '#4CAF50'
this.$vuetify.theme.themes.dark.primary = '#81C784'
```

## CSS Custom Properties

### Enable Custom Properties

```javascript
Vue.use(Vuetify, {
  options: {
    customProperties: true
  },
  theme: {
    primary: '#1976D2'
  }
})
```

### Use in Styles

```vue
<style>
.my-component {
  color: var(--v-primary-base);
  background: var(--v-secondary-darken2);
}

.custom-button {
  background: var(--v-accent-lighten1);
}
</style>
```

## Available Theme Variables

When `customProperties: true` is enabled:

```css
/* Base colors */
--v-primary-base
--v-secondary-base
--v-accent-base
--v-error-base
--v-info-base
--v-success-base
--v-warning-base

/* Light variants */
--v-primary-lighten1
--v-primary-lighten2
--v-primary-lighten3
--v-primary-lighten4
--v-primary-lighten5

/* Dark variants */
--v-primary-darken1
--v-primary-darken2
--v-primary-darken3
--v-primary-darken4
```

## Color Usage

### Component Colors

```vue
<!-- Theme colors -->
<v-btn color="primary">Primary</v-btn>
<v-btn color="secondary">Secondary</v-btn>
<v-btn color="accent">Accent</v-btn>

<!-- Semantic colors -->
<v-btn color="error">Error</v-btn>
<v-btn color="info">Info</v-btn>
<v-btn color="success">Success</v-btn>
<v-btn color="warning">Warning</v-btn>

<!-- Material colors -->
<v-btn color="blue darken-2">Blue Darken</v-btn>
<v-btn color="pink accent-1">Pink Accent</v-btn>
<v-chip color="teal">Teal</v-chip>

<!-- Custom colors -->
<v-btn color="#FF5722">Custom Hex</v-btn>
<v-btn color="rgb(255, 87, 34)">Custom RGB</v-btn>
```

### Text Colors

```vue
<v-card>
  <v-card-title class="primary--text">Primary Text</v-card-title>
  <v-card-text class="secondary--text">Secondary Text</v-card-text>
  <p class="error--text">Error Text</p>
</v-card>
```

### Background Colors

```vue
<v-card color="primary">
  <v-card-text class="white--text">
    Primary background with white text
  </v-card-text>
</v-card>

<div class="grey lighten-2 pa-4">
  Grey lighten-2 background
</div>
```

## Component Theming

### Dark Components

```vue
<v-card dark>
  <v-card-title>Dark Card</v-card-title>
</v-card>

<v-list dark>
  <v-list-tile>Dark List Item</v-list-tile>
</v-list>

<v-toolbar dark color="primary">
  <v-toolbar-title>Dark Toolbar</v-toolbar-title>
</v-toolbar>
```

### Light Components (in Dark Mode)

```vue
<v-card light>
  <v-card-title>Light Card in Dark Mode</v-card-title>
</v-card>
```

## Elevation (Shadows)

Vuetify 1.5 uses elevation classes (0-24):

```vue
<v-card :elevation="0">No shadow</v-card>
<v-card :elevation="2">Default shadow</v-card>
<v-card :elevation="4">Light shadow</v-card>
<v-card :elevation="8">Medium shadow</v-card>
<v-card :elevation="16">Heavy shadow</v-card>
<v-card :elevation="24">Maximum shadow</v-card>
```

### Elevation Classes

```html
<div class="elevation-2">Light shadow</div>
<div class="elevation-8">Medium shadow</div>
<div class="elevation-16">Heavy shadow</div>
```

## Pre-built Themes

### Light Theme

```javascript
theme: {
  primary: '#1976D2',
  secondary: '#424242',
  accent: '#82B1FF',
  error: '#FF5252',
  info: '#2196F3',
  success: '#4CAF50',
  warning: '#FFC107'
}
```

### Dark Theme

```javascript
theme: {
  dark: true,
  themes: {
    dark: {
      primary: '#2196F3',
      secondary: '#424242',
      accent: '#FF4081',
      error: '#FF5252',
      info: '#2196F3',
      success: '#4CAF50',
      warning: '#FB8C00'
    }
  }
}
```

## Best Practices

### 1. Use Semantic Color Names

```vue
<!-- Good: Use semantic colors -->
<v-btn color="primary">Submit</v-btn>
<v-alert type="error">Error message</v-alert>

<!-- Avoid: Hardcoded colors in templates -->
<v-btn color="#1976D2">Submit</v-btn>
```

### 2. Consistent Dark Mode Support

```javascript
// Define both light and dark themes
Vue.use(Vuetify, {
  theme: {
    themes: {
      light: { primary: '#1976D2' },
      dark: { primary: '#2196F3' }
    }
  }
})
```

### 3. Use CSS Variables for Custom Styles

```vue
<style scoped>
.custom-element {
  background: var(--v-primary-base);
  color: var(--v-primary-on-primary);
}
</style>
```

### 4. Theme Persistence

```javascript
// Store theme preference
const theme = localStorage.getItem('theme')
if (theme) {
  this.$vuetify.theme.dark = theme === 'dark'
}

// Watch for changes
watch: {
  '$vuetify.theme.dark'(val) {
    localStorage.setItem('theme', val ? 'dark' : 'light')
  }
}
```