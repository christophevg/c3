# Vuetify 1.5 Layout Patterns

## Grid System

Vuetify 1.5 uses a **v-container » v-layout » v-flex** hierarchy (different from V2's v-row/v-col).

### Basic Structure

```vue
<v-container>
  <v-layout row wrap>
    <v-flex xs12 sm6 md4>
      <!-- Content -->
    </v-flex>
  </v-layout>
</v-container>
```

### Container Types

| Prop | Description |
|------|-------------|
| `fluid` | Extends full width, removes max-width |
| `fill-height` | Fills parent/child height (important for Safari/Firefox) |
| `grid-list-{xs-xl}` | Sets gutter spacing |

### Grid List Spacing

| Prop | Gutter |
|------|--------|
| `grid-list-xs` | 2px |
| `grid-list-sm` | 4px |
| `grid-list-md` | 8px |
| `grid-list-lg` | 16px |
| `grid-list-xl` | 24px |

## Flex System

### v-layout Props

| Prop | Description |
|------|-------------|
| `row` | Horizontal layout (default) |
| `column` | Vertical layout |
| `wrap` | Allow wrapping |
| `reverse` | Reverse direction |
| `align-center` | Center align items |
| `align-start` | Start align items |
| `align-end` | End align items |
| `justify-center` | Center justify content |
| `justify-space-between` | Space between items |
| `justify-space-around` | Space around items |

### v-flex Props

| Prop | Description |
|------|-------------|
| `xs{n}`, `sm{n}`, `md{n}`, `lg{n}`, `xl{n}` | Column width (1-12) |
| `offset-{n}` | Offset columns |
| `order-{n}` | Order within flex container |
| `grow` | Flex-grow: 1 |
| `shrink` | Flex-shrink: 1 |

## Responsive Layouts

### Mobile-First Columns

```vue
<v-layout row wrap>
  <!-- Full width on mobile, half on tablet, third on desktop -->
  <v-flex xs12 sm6 md4>
    <v-card>Card 1</v-card>
  </v-flex>
  <v-flex xs12 sm6 md4>
    <v-card>Card 2</v-card>
  </v-flex>
  <v-flex xs12 sm6 md4>
    <v-card>Card 3</v-card>
  </v-flex>
</v-layout>
```

### Offset Columns

```vue
<v-layout row>
  <v-flex xs6 offset-xs3>
    <!-- Centered column, 6 wide with 3 offset -->
  </v-flex>
</v-layout>
```

### Column Direction

```vue
<v-layout column>
  <v-flex>Top content</v-flex>
  <v-flex>Middle content</v-flex>
  <v-flex>Bottom content</v-flex>
</v-layout>
```

### Reversed Order

```vue
<v-layout row reverse>
  <v-flex>First in DOM, last visually</v-flex>
  <v-flex>Last in DOM, first visually</v-flex>
</v-layout>
```

## Alignment Patterns

### Centered Content

```vue
<v-container fill-height>
  <v-layout align-center justify-center>
    <v-flex xs6>
      <v-card>Centered content</v-card>
    </v-flex>
  </v-layout>
</v-container>
```

### Space Between

```vue
<v-layout justify-space-between>
  <v-flex>Left</v-flex>
  <v-flex>Right</v-flex>
</v-layout>
```

### Vertical Alignment

```vue
<v-layout align-center>
  <v-flex>
    <v-card>Vertically centered</v-card>
  </v-flex>
</v-layout>
```

## Nested Layouts

```vue
<v-container>
  <v-layout row wrap>
    <v-flex xs12 md6>
      <v-card>
        <v-container grid-list-sm>
          <v-layout row wrap>
            <v-flex xs6>
              <v-card>Nested 1</v-card>
            </v-flex>
            <v-flex xs6>
              <v-card>Nested 2</v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
```

## v-spacer

Creates flexible space between elements:

```vue
<v-layout>
  <v-flex>Left content</v-flex>
  <v-spacer />
  <v-flex>Right content</v-flex>
</v-layout>

<!-- Or in toolbar -->
<v-toolbar>
  <v-toolbar-title>Title</v-toolbar-title>
  <v-spacer />
  <v-btn icon><v-icon>more_vert</v-icon></v-btn>
</v-toolbar>
```

## v-sheet

Basic container for layout and styling:

```vue
<v-sheet
  :max-width="300"
  class="mx-auto"
>
  <v-card>Content in sheet</v-card>
</v-sheet>
```

## Display Helpers

Vuetify 1.5 supports display classes:

```html
<!-- Display types -->
<div class="d-none">Hidden</div>
<div class="d-flex">Flex container</div>
<div class="d-inline-flex">Inline flex</div>
<div class="d-block">Block</div>
<div class="d-inline-block">Inline block</div>

<!-- Responsive display -->
<div class="hidden-sm-and-down">Hidden on sm and up</div>
<div class="hidden-md-and-up">Hidden on md and up</div>
<div class="hidden-xs-only">Hidden only on xs</div>
```

## Common Layout Patterns

### App Layout with Navigation

```vue
<v-app>
  <v-navigation-drawer v-model="drawer" app>
    <!-- Navigation content -->
  </v-navigation-drawer>

  <v-toolbar app>
    <v-toolbar-side-icon @click="drawer = !drawer" />
    <v-toolbar-title>App Title</v-toolbar-title>
  </v-toolbar>

  <v-content>
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs12>
          <!-- Page content -->
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>

  <v-footer app>
    <span>&copy; 2024</span>
  </v-footer>
</v-app>
```

### Dashboard Grid

```vue
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12 md6 lg4>
      <v-card>Widget 1</v-card>
    </v-flex>
    <v-flex xs12 md6 lg4>
      <v-card>Widget 2</v-card>
    </v-flex>
    <v-flex xs12 md6 lg4>
      <v-card>Widget 3</v-card>
    </v-flex>
  </v-layout>
</v-container>
```

### Two-Column Form

```vue
<v-container>
  <v-layout row wrap>
    <v-flex xs12 md6>
      <v-text-field label="First Name" />
    </v-flex>
    <v-flex xs12 md6>
      <v-text-field label="Last Name" />
    </v-flex>
    <v-flex xs12>
      <v-text-field label="Email" />
    </v-flex>
  </v-layout>
</v-container>
```

## Spacing Classes

Vuetify 1.5 uses a 0-5 scale (different from V2's 0-12):

| Class | Pixels |
|-------|--------|
| `ma-0`, `pa-0` | 0 |
| `ma-1`, `pa-1` | 4px |
| `ma-2`, `pa-2` | 8px |
| `ma-3`, `pa-3` | 16px |
| `ma-4`, `pa-4` | 24px |
| `ma-5`, `pa-5` | 48px |

### Directional Spacing

```html
<div class="mt-3">Margin top 16px</div>
<div class="mb-4">Margin bottom 24px</div>
<div class="mx-2">Margin left/right 8px</div>
<div class="my-3">Margin top/bottom 16px</div>
<div class="pt-2">Padding top 8px</div>
```