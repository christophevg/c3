---
name: vuetify-v2
description: Use this skill when creating or modifying Vuetify V2 UI components in Baseweb projects
triggers:
  - when creating Vuetify components
  - when asked about Vuetify component options
  - when designing UI layouts
  - when implementing forms, tables, or navigation
  - when working with themes or styling
---

# Vuetify V2 Skill

Comprehensive skill for creating beautiful UIs with Vuetify V2 components. Works as a companion to the baseweb skill, handling pure Vuetify specifics while baseweb handles project structure, navigation registration, API integration, and Vuex store modules.

## Overview

This skill provides:

| Capability | Description |
|------------|-------------|
| Component Selection | Guidance on choosing the right component for each use case |
| Component Props | Detailed props documentation for all Vuetify V2 components |
| Styling Patterns | Best practices for theming, colors, spacing, and responsive design |
| Layout Options | Grid system, containers, and layout components |
| Accessibility | A11y guidelines for Vuetify components |
| Common Patterns | Ready-to-use code templates for frequent UI patterns |

## V2 Focus

**IMPORTANT:** This skill focuses exclusively on Vuetify V2 because Baseweb projects use V2. Vuetify V3 has breaking changes and is not compatible.

Key V2 vs V3 differences to remember:
- Icon syntax: `<v-icon>mdi-home</v-icon>` (not `<v-icon icon="mdi-home" />`)
- Button sizes: `x-small`, `small`, `large`, `x-large` as boolean props (not `size="small"`)
- Activator slots: `v-slot:activator="{ on }"` + `v-on="on"` (not `v-bind="props"`)

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
- `v-btn-group` - Select between options (V2 alternative to v-btn-toggle)
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

### Layout
- `v-container` - Center and pad content
- `v-row` - Wrapper for columns
- `v-col` - Content holder
- `v-spacer` - Flexible spacing

### Data Display
- `v-data-table` - Tables with sorting, filtering, pagination
- `v-data-iterator` - Grid views with pagination
- `v-virtual-scroll` - Efficient long lists
- `v-infinite-scroll` - Load on scroll
- `v-timeline` - Chronological events
- `v-sparkline` - Simple charts

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

### Pickers
- `v-date-picker` - Date and month selection
- `v-time-picker` - Time selection
- `v-color-picker` - Visual color selection

## When to Use This Skill

Use this skill when:
- Creating or modifying Vuetify V2 components
- Designing UI layouts and layouts
- Implementing forms with validation
- Working with data tables
- Styling with themes and colors
- Need component prop/event/slot documentation

## Integration with Baseweb Skill

| Baseweb Skill Handles | Vuetify Skill Handles |
|-----------------------|----------------------|
| Page structure | Component selection |
| Navigation registration | Component props |
| API integration | Styling patterns |
| Vuex store modules | Layout options |
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

### Data Table

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

### Dialog

```vue
<v-dialog v-model="dialog" max-width="500">
  <template v-slot:activator="{ on }">
    <v-btn color="primary" v-on="on">Open Dialog</v-btn>
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

## Pattern Files

This skill includes detailed patterns in separate files:

- `patterns/selection.md` - Selection components and content panes
- `patterns/forms.md` - Form components and validation
- `patterns/navigation.md` - Navigation components
- `patterns/data-display.md` - Tables, cards, lists, and iterators
- `patterns/feedback.md` - Alerts, snackbars, dialogs
- `patterns/theming.md` - Colors and theming
- `patterns/images-icons.md` - Images, aspect ratios, and parallax
- `patterns/pickers.md` - Color, date, and time pickers
- `patterns/vue-form-generator-integration.md` - Using VueFormGenerator with Vuetify

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
```

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
<v-col cols="12" sm="6" md="4" lg="3">
  <!-- 12 columns on xs, 6 on sm, 4 on md, 3 on lg -->
</v-col>
```

## Agent Collaboration

This skill collaborates with:

| Agent | Collaboration Point |
|-------|---------------------|
| UI/UX Designer | Component selection, layout, styling |
| Python Developer | Frontend patterns for Baseweb pages |
| Functional Analyst | Understanding component capabilities |

## See Also

- [Vuetify V2 Documentation](https://v2.vuetifyjs.com/)
- [Material Design Icons](https://materialdesignicons.com/)
- [Baseweb Skill](/.claude/skills/baseweb/SKILL.md)