---
name: vuetify-v1
description: Use this skill when creating or modifying Vuetify 1.5 UI components in legacy Baseweb projects
triggers:
  - when creating Vuetify 1.5 components
  - when asked about Vuetify 1.5 component options
  - when maintaining legacy Baseweb projects using Vuetify 1.x
  - when migrating from Vuetify 1.x to Vuetify 2.x
---

# Vuetify V1.5 Skill

Comprehensive skill for creating and maintaining UIs with Vuetify 1.5 components. Designed for legacy Baseweb projects that haven't migrated to Vuetify 2.

## Overview

This skill provides:

| Capability | Description |
|------------|-------------|
| Component Selection | Guidance on choosing the right component for each use case |
| Component Props | Detailed props documentation for all Vuetify 1.5 components |
| Styling Patterns | Best practices for theming, colors, spacing, and responsive design |
| Layout Options | Grid system with v-layout/v-flex, containers |
| Accessibility | A11y guidelines for Vuetify components |
| Common Patterns | Ready-to-use code templates for frequent UI patterns |

## V1.5 vs V2 Key Differences

**CRITICAL**: Vuetify 1.5 and V2 are NOT compatible. Know these differences:

### Grid System

| Vuetify 1.5 | Vuetify 2 |
|-------------|-----------|
| `v-layout` | `v-row` |
| `v-flex` | `v-col` |
| `grid-list-md` prop | `dense` prop on row |

### Activator Slots

| Vuetify 1.5 | Vuetify 2 |
|-------------|-----------|
| `slot="activator"` | `v-slot:activator="{ on }"` |
| `<v-btn slot="activator">` | `<template v-slot:activator="{ on }"><v-btn v-on="on">` |

### Button Props

| Vuetify 1.5 | Vuetify 2 |
|-------------|-----------|
| `flat` | `text` |
| `outline` | `outlined` |
| `small`, `large` | `x-small`, `small`, `large`, `x-large` |

### Spacing Scale

| Vuetify 1.5 | Vuetify 2 | Pixels |
|-------------|-----------|--------|
| `ma-3`, `pa-3` | `ma-4`, `pa-4` | 16px |
| `ma-4`, `pa-4` | `ma-6`, `pa-6` | 24px |
| `ma-5`, `pa-5` | `ma-12`, `pa-12` | 48px |

### Text Alignment

| Vuetify 1.5 | Vuetify 2 |
|-------------|-----------|
| `text-xs-center` | `text-center` |
| `text-xs-right` | `text-right` |

### Other Differences

| Vuetify 1.5 | Vuetify 2 |
|-------------|-----------|
| `v-card-media` | `v-img` (deprecated) |
| `v-btn-toggle` | `v-btn-group` |
| `v-list-tile` | `v-list-item` |

## Component Categories

### Containment

- `v-btn` - Button for actions and navigation
- `v-card` - Versatile container for content
- `v-card-title`, `v-card-text`, `v-card-actions`, `v-card-media` - Card sub-components
- `v-list`, `v-list-tile` - Display interface for items
- `v-chip` - Small pieces of information (tags, filters)
- `v-divider` - Separate content into sections
- `v-expansion-panel` - Reveal additional content
- `v-menu` - Display a list of actions (dropdowns)
- `v-dialog` - Modal dialogs
- `v-bottom-sheet` - Content from bottom
- `v-toolbar` - Label content areas
- `v-tooltip` - Additional information on hover
- `v-sheet` - Simple styled container

### Selection

- `v-btn-toggle` - Button group for selection (V1 alternative to V2's `v-btn-group`)
- `v-chip-group` - NOT available in V1 (use `v-btn-toggle` or custom implementation)
- `v-carousel` - Display multiple visual content
- `v-window` / `v-item-group` - Display content based on model
- `v-stepper` - Linear progress for forms (multi-step forms)

### Navigation

- `v-toolbar` - Top-level navigation (V1 uses `v-toolbar`, V2 uses `v-app-bar`)
- `v-fab` - Floating Action Button
- `v-navigation-drawer` - Side navigation
- `v-pagination` - Paginate long sets of data
- `v-bottom-nav` - Mobile navigation (V2 renamed to `v-bottom-navigation`)
- `v-breadcrumbs`, `v-breadcrumbs-item`, `v-breadcrumbs-divider` - Path indication
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
- `v-radio`, `v-radio-group` - Single choice from options
- `v-file-input` - NOT available in V1 (use native input with `v-text-field`)
- `v-slider` - Range input
- `v-range-slider` - Range selection
- `v-form` - Form container with validation
- `v-overflow-btn` - V1-specific overflow dropdown

### Layout

- `v-container` - Center and pad content
- `v-layout` - Wrapper for flex items (V1)
- `v-flex` - Content holder (V1)
- `v-spacer` - Flexible spacing

### Data Display

- `v-data-table` - Tables with sorting, filtering, pagination
- `v-data-iterator` - Grid views with pagination
- `v-virtual-scroll` - NOT available in V1
- `v-infinite-scroll` - NOT available in V1
- `v-timeline` - Chronological events
- `v-sparkline` - Simple charts

### Feedback

- `v-alert` - Important messages (warnings, errors, success)
- `v-snackbar` - Toast notifications
- `v-badge` - Notifications, counts
- `v-banner` - NOT available in V1
- `v-skeleton-loader` - NOT available in V1
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
- `v-color-picker` - NOT available in V1

### Other

- `v-calendar`, `v-calendar-daily`, `v-calendar-monthly`, `v-calendar-weekly` - Calendar views
- `v-treeview` - Tree structure display
- `v-hover` - Hover state detection

## When to Use This Skill

Use this skill when:
- Creating or modifying Vuetify 1.5 components in legacy projects
- Maintaining Baseweb projects that haven't migrated to V2
- Understanding V1 syntax for migration planning
- Need component prop/event/slot documentation for V1.5

## Integration with Baseweb Skill

| Baseweb Skill Handles | Vuetify V1 Skill Handles |
|-----------------------|--------------------------|
| Page structure | Component selection |
| Navigation registration | Component props |
| API integration | Styling patterns |
| Vuex store modules | Layout options |
| Socket.IO events | Accessibility |

## Quick Reference

### Grid Layout (V1.5)

```vue
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12 sm6 md4 lg3>
      <!-- Responsive: full on xs, half on sm, third on md, quarter on lg -->
    </v-flex>
  </v-layout>
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

### Dialog (V1.5 Activator Syntax)

```vue
<v-dialog v-model="dialog" max-width="500">
  <v-btn slot="activator" color="primary">Open Dialog</v-btn>
  <v-card>
    <v-card-title>Title</v-card-title>
    <v-card-text>Content</v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn flat @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="save">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Menu (V1.5 Activator Syntax)

```vue
<v-menu offset-y>
  <v-btn slot="activator">
    <span>Options</span>
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

### Button Group (V1.5)

```vue
<!-- V1.5 uses v-btn-toggle instead of v-btn-group -->
<v-btn-toggle v-model="selected">
  <v-btn flat>
    <v-icon>format_align_left</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_center</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_right</v-icon>
  </v-btn>
</v-btn-toggle>
```

### Data Table

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :search="search"
>
  <template slot="items" slot-scope="props">
    <td>{{ props.item.name }}</td>
    <td>{{ props.item.status }}</td>
  </template>
</v-data-table>
```

### Card with Actions

```vue
<v-card>
  <v-card-title>Title</v-card-title>
  <v-card-text>Content here</v-card-text>
  <v-card-actions>
    <v-btn flat color="primary">Action</v-btn>
    <v-spacer />
    <v-btn flat @click="cancel">Cancel</v-btn>
  </v-card-actions>
</v-card>
```

### Navigation Drawer

```vue
<v-navigation-drawer
  v-model="drawer"
  app
  :clipped="$vuetify.breakpoint.lgAndUp"
>
  <v-list>
    <v-list-tile to="/home">
      <v-list-tile-action>
        <v-icon>home</v-icon>
      </v-list-tile-action>
      <v-list-tile-content>
        <v-list-tile-title>Home</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
  </v-list>
</v-navigation-drawer>
```

## Pattern Files

This skill includes detailed patterns in separate files:

- `patterns/selection.md` - Selection components and content panes
- `patterns/forms.md` - Form components and validation
- `patterns/navigation.md` - Navigation components
- `patterns/data-display.md` - Tables, cards, lists
- `patterns/feedback.md` - Alerts, snackbars, dialogs
- `patterns/theming.md` - Colors and theming
- `patterns/images-icons.md` - Images, avatars, icons
- `patterns/pickers.md` - Date and time pickers
- `patterns/layout.md` - Grid system and responsive design
- `patterns/buttons.md` - Button variants and patterns

## Theming Quick Reference

### Theme Configuration

```javascript
// main.js or vuetify config
Vue.use(Vuetify, {
  theme: {
    primary: '#3f51b5',
    secondary: '#b0bec5',
    accent: '#8c9eff',
    error: '#b71c1c'
  }
})
```

### Using Pre-defined Material Colors

```javascript
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
  theme: {
    primary: colors.purple.base
  }
})
```

### Dynamic Theme Access

```javascript
// Change theme color at runtime
this.$vuetify.theme.primary = '#4caf50'

// Toggle dark mode
this.$vuetify.theme.dark = true
```

### Theme Colors

| Color | Usage |
|-------|-------|
| `primary` | Primary brand color |
| `secondary` | Secondary brand color |
| `accent` | Accent color |
| `error` | Error states |
| `info` | Informational |
| `success` | Success states |
| `warning` | Warning states |

## Breakpoints

| Device | Code | Range |
|--------|------|-------|
| Extra small | `xs` | < 600px |
| Small | `sm` | 600px - 959px |
| Medium | `md` | 960px - 1263px |
| Large | `lg` | 1264px - 1903px |
| Extra large | `xl` | 1904px+ |

### Responsive Props

```html
<v-flex xs12 sm6 md4 lg3>
  <!-- 12 columns on xs, 6 on sm, 4 on md, 3 on lg -->
</v-flex>
```

### Programmatic Breakpoint Access

```javascript
// Available at $vuetify.breakpoint
if (this.$vuetify.breakpoint.smAndDown) {
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

## See Also

- [Vuetify 1.5 Documentation](https://v15.vuetifyjs.com/)
- [Material Design Icons](https://materialdesignicons.com/)
- [Vuetify V2 Skill](/.claude/skills/vuetify/SKILL.md) - For V2 projects
- [Baseweb Skill](/.claude/skills/baseweb/SKILL.md)