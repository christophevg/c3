---
name: vuetify-v3
description: Use this skill when creating or modifying Vuetify V3 UI components in Baseweb projects. Examples: "create Vuetify 3 component", "Vuetify V3 form patterns", "Vuetify 3 data table", "migrate Vuetify 2 to 3"
triggers:
  - when creating Vuetify V3 components
  - when asked about Vuetify V3 component options
  - when designing UI layouts with Vuetify 3
  - when implementing forms, tables, or navigation with Vuetify 3
  - when working with Vuetify 3 themes or styling
  - when migrating from Vuetify V2 to V3
---

# Vuetify V3 Skill

Comprehensive skill for creating beautiful UIs with Vuetify V3 components. Works as a companion to the baseweb skill, handling pure Vuetify V3 specifics while baseweb handles project structure, navigation registration, API integration, and state management.

## Overview

This skill provides:

| Capability | Description |
|------------|-------------|
| Component Selection | Guidance on choosing the right component for each use case |
| Component Props | Detailed props documentation for all Vuetify V3 components |
| Styling Patterns | Best practices for theming, colors, spacing, and responsive design |
| Layout Options | Grid system, containers, and layout components |
| Accessibility | A11y guidelines for Vuetify components |
| Common Patterns | Ready-to-use code templates for frequent UI patterns |
| Migration Guide | Breaking changes and migration patterns from V2 to V3 |

## V3 Focus

**IMPORTANT:** This skill focuses exclusively on Vuetify V3 because Baseweb projects are migrating to V3. Vuetify V3 has breaking changes from V2.

### Key Breaking Changes from V2 to V3

| Vuetify V2 | Vuetify V3 |
|------------|------------|
| `value` prop | `model-value` |
| `@input` event | `@update:model-value` |
| `background-color` | `bg-color` |
| `v-simple-table` | `v-table` |
| `v-tab-item` | `v-window-item` |
| `v-list-item-content` | **removed** (lists use CSS grid) |
| `v-list-item-group` | **removed** (use `value` on items + `v-model:selected` on list) |
| `active-class` (v-btn) | `selected-class` |
| `depressed` (v-btn) | `variant="flat"` |
| `on-icon/off-icon` | `true-icon/false-icon` |
| `retain-focus-on-click` | **removed** (use `:focus-visible`) |

### Activator Slot Syntax Change

**Vuetify V2 (Old):**
```vue
<template v-slot:activator="{ on, attrs }">
  <v-btn v-bind="attrs" v-on="on">Click me</v-btn>
</template>
```

**Vuetify V3 (New):**
```vue
<template v-slot:activator="{ props }">
  <v-btn v-bind="props">Click me</v-btn>
</template>
```

The `on` (event handlers) and `attrs` (attributes) objects are merged into a single `props` object.

### Icon Usage Change

**Vuetify V2 (Old):**
```vue
<v-icon>mdi-home</v-icon>
```

**Vuetify V3 (Recommended):**
```vue
<v-icon icon="mdi-home" />
```

Use the `icon` prop instead of default slot content for icons.

## Component Categories

### Containment

- `v-btn` - Button for actions and navigation
- `v-card` - Versatile container for content
- `v-list` - Display interface for items
- `v-chip` - Small pieces of information (tags, filters)
- `v-divider` - Separate content into sections
- `v-expansion-panel` - Reveal additional content
- `v-menu` - Display a list of actions (dropdowns)
- `v-dialog` - Modal dialogs
- `v-bottom-sheet` - Content from bottom
- `v-overlay` - Custom scrim/overlay
- `v-toolbar` - Label content areas
- `v-tooltip` - Additional information on hover
- `v-sheet` - Simple styled container

### Selection

- `v-chip-group` - Makes chips interactive for tag selection and filters
- `v-btn-group` - Select between options
- `v-carousel` - Display multiple visual content
- `v-window` - Display content based on model (tabs alternative)
- `v-stepper` - Linear progress for forms (multi-step forms)

### Navigation

- `v-app-bar` - Top-level navigation
- `v-fab` - Floating Action Button
- `v-navigation-drawer` - Side navigation
- `v-pagination` - Paginate long sets of data
- `v-bottom-navigation` - Mobile navigation
- `v-breadcrumbs` - Path indication
- `v-footer` - Footer area
- `v-speed-dial` - FAB that reveals actions
- `v-system-bar` - Status bar
- `v-tabs` - Organize content in sections

### Form Inputs

- `v-text-field` - Text input
- `v-textarea` - Multi-line text input
- `v-select` - Dropdown selection
- `v-autocomplete` - Type-ahead selection
- `v-combobox` - Select with custom entry
- `v-checkbox` - Boolean/multi-select
- `v-switch` - Toggle switch
- `v-radio` - Single choice from options
- `v-file-input` - File upload
- `v-slider` - Range input
- `v-range-slider` - Range selection
- `v-form` - Form container with validation
- `v-number-input` - Number input (V3.7.0+)
- `v-otp-input` - OTP/MFA input (V3.4.0+)

### Layout

- `v-container` - Center and pad content
- `v-row` - Wrapper for columns
- `v-col` - Content holder
- `v-spacer` - Flexible spacing
- `v-responsive` - Maintain aspect ratios for layout

### Data Display

- `v-data-table` - Tables with sorting, filtering, pagination
- `v-data-table-server` - Server-side data tables
- `v-data-iterator` - Grid views with pagination
- `v-virtual-scroll` - Efficient long lists
- `v-infinite-scroll` - Load on scroll
- `v-timeline` - Chronological events
- `v-sparkline` - Simple charts
- `v-table` - Simple table (renamed from `v-simple-table`)

### Feedback

- `v-alert` - Important messages (warnings, errors, success)
- `v-snackbar` - Toast notifications
- `v-badge` - Notifications, counts
- `v-banner` - Announcements
- `v-skeleton-loader` - Loading states
- `v-progress-circular` - Circular loading
- `v-progress-linear` - Linear progress
- `v-rating` - User feedback

### Images & Icons

- `v-img` - Flexible image display with lazy loading
- `v-responsive` - Maintain aspect ratios for layout
- `v-parallax` - 3D scrolling effect for hero sections
- `v-icon` - Material Design Icons
- `v-avatar` - User avatars

### Pickers

- `v-date-picker` - Date and month selection
- `v-time-picker` - Time selection
- `v-color-picker` - Visual color selection

### Providers (V3 New)

- `v-default-provider` - Set default prop values
- `v-locale-provider` - Locale configuration
- `v-theme-provider` - Scoped theme configuration

### Labs Components (Experimental)

Must be imported from `vuetify/labs/components`:

- `VColorInput` - Color input field
- `VDateInput` - Date input field
- `VMaskInput` - Masked input field
- `VCommandPalette` - Command palette
- `VFileUpload` - File upload component
- `VAvatarGroup` - Avatar group
- `VIconBtn` - Icon button
- `VPicker` - Generic picker
- `VPie` - Pie chart
- `VPullToRefresh` - Pull to refresh
- `VStepperVertical` - Vertical stepper
- `VVideo` - Video player

## When to Use This Skill

Use this skill when:
- Creating or modifying Vuetify V3 components
- Designing UI layouts and responsive designs
- Implementing forms with validation
- Working with data tables
- Styling with themes and colors
- Migrating from Vuetify V2 to V3
- Need component prop/event/slot documentation for V3

## Integration with Baseweb Skill

| Baseweb Skill Handles | Vuetify V3 Skill Handles |
|-----------------------|--------------------------|
| Page structure | Component selection |
| Navigation registration | Component props |
| API integration | Styling patterns |
| State management | Layout options |
| Socket.IO events | Accessibility |

## Quick Reference

### Layout Pattern

```vue
<v-container>
  <v-row>
    <v-col cols="12" sm="6" md="4" lg="3">
      <!-- Responsive: full on mobile, half on sm, third on md, quarter on lg -->
    </v-col>
  </v-row>
</v-container>
```

### Form with Validation

```vue
<v-form ref="form" v-model="valid">
  <v-text-field
    v-model="name"
    :rules="[v => !!v || 'Name is required']"
    label="Name"
    required
  />
  <v-btn :disabled="!valid" @click="submit">Submit</v-btn>
</v-form>
```

### Chip Group (Tag Selection)

```vue
<v-chip-group v-model="selected" multiple column active-class="primary--text">
  <v-chip filter>Vue.js</v-chip>
  <v-chip filter>React</v-chip>
  <v-chip filter>Angular</v-chip>
</v-chip-group>
```

### Data Table (Client-Side)

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :search="search"
>
  <template #item.status="{ item }">
    <v-chip :color="item.status === 'active' ? 'success' : 'error'">
      {{ item.status }}
    </v-chip>
  </template>
</v-data-table>
```

### Data Table (Server-Side)

```vue
<v-data-table-server
  :items="serverItems"
  :items-length="totalItems"
  :headers="headers"
  :loading="loading"
  :items-per-page="itemsPerPage"
  @update:options="loadItems"
/>

<script setup>
const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  loading.value = true
  const response = await fetch(`/api/data?page=${page}&perPage=${itemsPerPage}`)
  serverItems.value = response.data
  totalItems.value = response.total
  loading.value = false
}
</script>
```

### Dialog (V3 Activator Syntax)

```vue
<v-dialog v-model="dialog" max-width="500">
  <template v-slot:activator="{ props }">
    <v-btn color="primary" v-bind="props">Open Dialog</v-btn>
  </template>
  <v-card>
    <v-card-title>Title</v-card-title>
    <v-card-text>Content</v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="save">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Menu (V3 Activator Syntax)

```vue
<v-menu>
  <template v-slot:activator="{ props }">
    <v-btn v-bind="props">
      <span>Options</span>
      <v-icon icon="mdi-chevron-down" />
    </v-btn>
  </template>
  <v-list>
    <v-list-item @click="action1">
      <v-list-item-title>Action 1</v-list-item-title>
    </v-list-item>
    <v-list-item @click="action2">
      <v-list-item-title>Action 2</v-list-item-title>
    </v-list-item>
  </v-list>
</v-menu>
```

### Card with Actions

```vue
<v-card>
  <v-card-title>Title</v-card-title>
  <v-card-text>Content here</v-card-text>
  <v-card-actions>
    <v-btn text color="primary">Action</v-btn>
    <v-spacer />
    <v-btn text @click="cancel">Cancel</v-btn>
  </v-card-actions>
</v-card>
```

### Number Input (V3.7.0+)

```vue
<v-number-input
  v-model="quantity"
  :max="100"
  :min="0"
  :step="1"
  control-variant="stacked"
  label="Quantity"
/>
```

### OTP Input (V3.4.0+)

```vue
<v-otp-input
  v-model="otp"
  :length="6"
  autofocus
/>
```

## Pattern Files

This skill includes detailed patterns in separate files:

- `patterns/buttons.md` - Button variants and patterns
- `patterns/forms.md` - Form components and validation
- `patterns/navigation.md` - Navigation components
- `patterns/data-display.md` - Tables, cards, lists, and iterators
- `patterns/feedback.md` - Alerts, snackbars, dialogs
- `patterns/theming.md` - Colors and theming system
- `patterns/images-icons.md` - Images, aspect ratios, and parallax
- `patterns/pickers.md` - Color, date, and time pickers
- `patterns/selection.md` - Selection components and content panes
- `patterns/layout.md` - Grid system and responsive design

## VueFormGenerator Integration

For larger, complex forms, use **VueFormGenerator** instead of native Vuetify forms. VueFormGenerator provides:

- Schema-based form definitions
- Dynamic/conditional fields
- API-driven form schemas
- Multi-step wizard forms

See the `vue-form-generator` skill for detailed patterns.

**When to use:**
- VueFormGenerator: Complex forms, multi-step forms, dynamic fields, API-driven schemas
- Vuetify native: Simple forms (1-5 fields), quick CRUD, static forms, prototypes

## Theming Quick Reference

### Theme Configuration

```javascript
// src/plugins/vuetify.js
import { createVuetify } from 'vuetify'

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
        },
      },
    },
  },
})
```

### Base Colors Required

| Color | Usage |
|-------|-------|
| `background` | Page background |
| `surface` | Card/component background |
| `primary` | Primary brand color |
| `secondary` | Secondary brand color |
| `success` | Success states |
| `warning` | Warning states |
| `error` | Error states |
| `info` | Informational |

### On-colors Auto-generation

Colors like `on-primary`, `on-surface` are auto-generated based on luminance for proper text contrast.

```css
/* Generated CSS variables */
:root {
  --v-theme-primary: 24, 103, 192;
}

/* Usage in custom CSS */
.my-component {
  background: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-on-primary));
}
```

### Dynamic Theme Switching

```typescript
import { useTheme } from 'vuetify'

const theme = useTheme()
theme.change('dark')            // Switch to specific theme
theme.cycle()                   // Cycle through all themes
theme.toggle(['light', 'dark']) // Toggle between specific themes
theme.current.value.dark        // Check if dark theme
```

### Using Colors

```html
<v-btn color="primary">Primary</v-btn>
<v-card color="secondary">Secondary</v-card>
<v-chip color="success">Active</v-chip>
<v-alert type="error">Error message</v-alert>
```

### Dark Mode

```javascript
// Toggle dark mode
this.$vuetify.theme.dark = !this.$vuetify.theme.dark

// Or with Composition API
const theme = useTheme()
theme.toggle(['light', 'dark'])
```

## Icon System

### MDI Font (CSS) - Easiest

```bash
npm install @mdi/font -D
```

```javascript
// src/plugins/vuetify.js
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

export default createVuetify({
  icons: {
    defaultSet: 'mdi',
  },
})
```

### MDI SVG (Recommended for Production)

```javascript
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { mdiAccount } from '@mdi/js'

export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases: {
      ...aliases,
      account: mdiAccount,
    },
    sets: {
      mdi,
    },
  },
})
```

### Usage

```vue
<!-- MDI icon -->
<v-icon icon="mdi-account" />

<!-- Custom icon alias -->
<v-icon icon="$account" />

<!-- In component props -->
<v-btn prepend-icon="mdi-home">Home</v-btn>
<v-card append-icon="mdi-close">Card</v-card>
```

### Other Icon Sets Available

- Material Icons: `vuetify/iconsets/md`
- FontAwesome 5 CSS: `vuetify/iconsets/fa`
- FontAwesome 5 SVG: `vuetify/iconsets/fa-svg`
- FontAwesome 4: `vuetify/iconsets/fa4`
- UnoCSS: Phosphor, Lucide, Tabler, Remix, BoxIcons, Carbon via Iconify

## Breakpoints

| Device | Code | Min | Max |
|--------|------|-----|-----|
| Extra small | `xs` | 0px | 599px |
| Small | `sm` | 600px | 959px |
| Medium | `md` | 960px | 1279px |
| Large | `lg` | 1280px | 1919px |
| Extra large | `xl` | 1920px | 2559px |
| Extra extra large | `xxl` | 2560px+ | - |

### Responsive Props

```html
<v-col cols="12" sm="6" md="4" lg="3">
  <!-- 12 columns on xs, 6 on sm, 4 on md, 3 on lg -->
</v-col>
```

### Programmatic Breakpoint Access

```javascript
import { useDisplay } from 'vuetify'

const { xs, sm, md, lg, xl, xxl, smAndDown, mdAndUp } = useDisplay()

if (smAndDown.value) {
  // Mobile-specific logic
}
```

## Agent Collaboration

This skill collaborates with:

| Agent | Collaboration Point |
|-------|---------------------|
| UI/UX Designer | Component selection, layout, styling |
| Python Developer | Frontend patterns for Baseweb pages |
| Functional Analyst | Understanding component capabilities |

## Migration from V2 to V3

When migrating Baseweb projects from Vuetify V2 to V3:

### Step 1: Update Dependencies

```bash
npm uninstall vuetify
npm install vuetify@^3.0.0
```

### Step 2: Update Plugin Initialization

```javascript
// V2 (Old)
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

// V3 (New)
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

const vuetify = createVuetify()
app.use(vuetify)
```

### Step 3: Update Component Syntax

| Change | V2 | V3 |
|--------|----|----|
| Props with v-model | `value` | `model-value` |
| Events | `@input` | `@update:model-value` |
| Activator slots | `{ on, attrs }` | `{ props }` |
| Icons | `<v-icon>mdi-home</v-icon>` | `<v-icon icon="mdi-home" />` |
| Button variant | `depressed` | `variant="flat"` |
| Table | `v-simple-table` | `v-table` |
| Tab content | `v-tab-item` | `v-window-item` |

### Step 4: Remove Deprecated Components

- `v-list-item-content` - Remove wrapper, use `v-list-item-title` directly
- `v-list-item-group` - Use `value` prop on items + `v-model:selected` on list
- `retain-focus-on-click` - Remove, use `:focus-visible` CSS

### Step 5: Update Theme System

```javascript
// V2 (Old)
theme: {
  primary: '#3f51b5',
  secondary: '#b0bec5',
}

// V3 (New)
theme: {
  themes: {
    light: {
      colors: {
        primary: '#3f51b5',
        secondary: '#b0bec5',
      },
    },
  },
}
```

## See Also

- [Vuetify V3 Documentation](https://vuetifyjs.com/)
- [Vuetify V3 Upgrade Guide](https://vuetifyjs.com/getting-started/upgrade-guide/)
- [Material Design Icons](https://materialdesignicons.com/)
- [Baseweb Skill](/.claude/skills/baseweb/SKILL.md)
- [Vuetify V2 Skill](/.claude/skills/vuetify-v2/SKILL.md) - For legacy V2 projects