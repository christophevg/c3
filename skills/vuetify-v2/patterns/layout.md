# Layout Patterns

Comprehensive patterns for Vuetify V2 grid system and responsive layout.

## Containment Components

### v-sheet
Basic generic container ("piece of paper") with background color and elevation.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `color` | string | Material or CSS color |
| `elevation` | number | Shadow depth (0-24) |
| `dark` / `light` | boolean | Theme variants |
| `tile` | boolean | Removes border-radius |
| `tag` | string | Changes root element (default `div`) |

**Example:**
```vue
<v-sheet color="primary" elevation="4" width="300" height="200">
  Custom styled sheet content
</v-sheet>
```

### v-overlay
Backdrop layer (scrim) to emphasize content or create popups.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | boolean | Visibility control |
| `color` | string | Scrim color |
| `opacity` | number | Transparency |
| `contained` | boolean | Overlay contained within parent instead of screen |

**Example:**
```vue
<v-overlay v-model="showOverlay" color="black" opacity="0.7">
  <v-sheet class="pa-4">Custom Overlay Content</v-sheet>
</v-overlay>
```

### v-bottom-sheet
Specialized overlay sliding up from the bottom (mobile-first).

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | boolean | Visibility control |
| `inset` | boolean | Reduces max width on desktop |
| `persistent` | boolean | Don't close on outside click |

**Example:**
```vue
<v-bottom-sheet v-model="sheet">
  <v-sheet class="text-center" height="50vh" tile>
    Bottom Sheet Content
  </v-sheet>
</v-bottom-sheet>
```

## Grid System
Vuetify uses a 12-column grid system with responsive breakpoints.

### Basic Structure
```vue
<v-container>
  <v-row>
    <v-col cols="12">
      <!-- Full width -->
    </v-col>
  </v-row>
</v-container>
```

### v-container
Wraps content and centers it horizontally.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `fluid` | boolean | Full-width container |
| `tag` | string | HTML tag (default: `div`) |

**Example:**
```vue
<!-- Centered container (max-width: 1200px) -->
<v-container>
  <!-- Content -->
</v-container>

<!-- Full-width container -->
<v-container fluid>
  <!-- Content -->
</v-container>
```

### v-row
Wrapper for columns with alignment options.

**Key Props:**
| Prop | Values | Description |
| :--- | :--- | :--- |
| `align` | `start`, `center`, `end`, `baseline`, `stretch` | Vertical alignment |
| `justify` | `start`, `center`, `end`, `space-between`, `space-around` | Horizontal alignment |
| `no-gutters` | boolean | Remove column gutters |
| `dense` | boolean | Reduce column spacing |

**Example:**
```vue
<!-- Centered content -->
<v-row align="center" justify="center">
  <v-col cols="6">Centered</v-col>
</v-row>

<!-- Space between columns -->
<v-row justify="space-between">
  <v-col cols="3">Left</v-col>
  <v-col cols="3">Right</v-col>
</v-row>
```

### v-col
Content holder with responsive column spans.

**Key Props:**
| Prop | Values | Description |
| :--- | :--- | :--- |
| `cols` | 1-12, "auto" | Default columns (xs breakpoint) |
| `sm` | 1-12, "auto" | Small screens (≥600px) |
| `md` | 1-12, "auto" | Medium screens (≥960px) |
| `lg` | 1-12, "auto" | Large screens (≥1264px) |
| `xl` | 1-12, "auto" | Extra large screens (≥1904px) |
| `offset` | 0-12 | Column offset |
| `order` | 1-12 | Order within row |

**Example:**
```vue
<!-- Responsive columns -->
<v-row>
  <v-col cols="12" sm="6" md="4" lg="3">
    <!-- Full width on mobile
         Half on small screens
         1/3 on medium screens
         1/4 on large screens -->
  </v-col>
</v-row>
```

### v-spacer
Flexible spacing between elements.

**Example:**
```vue
<v-row>
  <v-col cols="auto">Left</v-col>
  <v-spacer />
  <v-col cols="auto">Right</v-col>
</v-row>
```

## Breakpoints
| Breakpoint | Code | Range | Devices |
|------------|------|-------|---------|
| Extra small | `xs` | < 600px | Phones |
| Small | `sm` | ≥ 600px | Tablets |
| Medium | `md` | ≥ 960px | Small laptops |
| Large | `lg` | ≥ 1264px | Laptops/desktops |
| Extra large | `xl` | ≥ 1904px | Large desktops |

### Key Behaviors
1. **No `xs` prop** - Use `cols` for smallest screens
2. **"And up" behavior** - Props apply to that size and larger
3. **12-column system** - Total columns per row = 12

## Common Layout Patterns
### Two-Column Layout
```vue
<v-container>
  <v-row>
    <v-col cols="12" md="8">
      <h2>Main Content</h2>
    </v-col>
    <v-col cols="12" md="4">
      <h3>Sidebar</h3>
    </v-col>
  </v-row>
</v-container>
```

### Dashboard Grid
```vue
<v-container fluid>
  <v-row dense>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 1</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 2</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 3</v-card>
    </v-col>
    <v-col cols="12" sm="6" lg="3">
      <v-card>Stat Card 4</v-card>
    </v-col>
  </v-row>
</v-container>
```

### Centered Content
```vue
<v-container fill-height>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card>
        <v-card-title>Centered Card</v-card-title>
      </v-card>
    </v-col>
  </v-row>
</v-container>
```

## Application Layout
### Full App Layout
```vue
<v-app>
  <v-navigation-drawer app v-model="drawer" clipped>
    <v-list>
      <v-list-item to="/" exact>
        <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-app-bar app clipped-left color="primary" dark>
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-toolbar-title>App Title</v-toolbar-title>
    <v-spacer />
    <v-btn icon><v-icon>mdi-cog</v-icon></v-btn>
  </v-app-bar>

  <v-main>
    <v-container fluid>
      <router-view />
    </v-container>
  </v-main>

  <v-footer app>
    <span>&copy; 2024</span>
  </v-footer>
</v-app>
```

## Responsive Visibility
### Display Helpers
```vue
<div class="hidden-sm-and-down">Hidden on sm and smaller</div>
<div class="hidden-md-and-up">Hidden on md and larger</div>
```

### Conditional Rendering
```vue
<div v-if="$vuetify.breakpoint.mobile">
  Mobile view
</div>
```

## Spacing
Vuetify uses spacing classes: `{property}{direction}-{size}`
- **Property**: `m` (margin), `p` (padding)
- **Direction**: `t`, `b`, `l`, `r`, `x`, `y`, `a`
- **Size**: 0-12 (4px increments)

```vue
<div class="pa-4">Padding all sides 16px</div>
<div class="mt-4 mb-2">Margin top 16px, bottom 8px</div>
```
