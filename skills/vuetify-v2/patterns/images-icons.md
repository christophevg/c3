# Images & Icons Patterns

Comprehensive patterns for Vuetify V2 image and icon components.

## Aspect Ratios & Responsiveness

Vuetify V2 does not have a standalone `v-aspect-ratio` component. Instead, aspect ratio is managed via the `aspect-ratio` prop in `v-responsive` and `v-img`.

### v-responsive
A container used to maintain a specific aspect ratio for layout sections.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `aspect-ratio` | string \| number | The ratio of width to height (e.g., `1.7778` for 16:9) |
| `width` | string \| number | Sets the width of the container |
| `height` | string \| number | Sets the height of the container |

**Example:**
```vue
<v-responsive aspect-ratio="1.7778">
  <!-- Content will maintain 16:9 ratio -->
  <div class="fill-height">
    16:9 Content Area
  </div>
</v-responsive>
```

### v-img
High-performance image component with built-in lazy loading and ratio handling.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `src` | string | **Mandatory**. Image URL |
| `aspect-ratio` | string | Forces a specific ratio (e.g., `"16/9"`), preventing layout shift |
| `contain` | boolean | Prevents cropping by adding space if the image doesn't fit |
| `lazy-src` | string | Low-res placeholder shown during load |
| `gradient` | string | CSS linear-gradient overlay |

**Key Events:**
| Event | Description |
| :--- | :--- |
| `@load` | Triggered when image loads successfully |
| `@error` | Triggered on load failure |

**Key Slots:**
| Slot | Description |
| :--- | :--- |
| `default` | Overlays content (text/buttons) on top of the image |
| `placeholder` | Custom loading UI (e.g., `v-progress-circular`) |
| `error` | Fallback UI for broken images |

**Example:**
```vue
<v-img
  src="https://picsum.photos/500/300"
  aspect-ratio="16/9"
  lazy-src="https://picsum.photos/10/6"
>
  <template v-slot:placeholder>
    <v-row class="fill-height" justify="center" align="center">
      <v-progress-circular indeterminate color="primary" />
    </v-row>
  </template>
  
  <!-- Overlay content -->
  <div class="white--text px-4 py-2">Image Caption</div>
</v-img>
```

### v-parallax
Creates a 3D scrolling effect where the background image moves slower than the foreground.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `src` | string | Background image URL |
| `height` | number | Height of the parallax area (default: `500`) |
| `alt` | string | Alternative text |

**Example:**
```vue
<v-parallax src="hero-bg.jpg" height="600">
  <div class="text-center white--text fill-height align-center justify-center">
    <h1 class="headline">Welcome to the Site</h1>
    <p>Experience the depth of Vuetify V2</p>
  </div>
</v-parallax>
```

## See Also
- [Vuetify V2 Images](https://v15.vuetifyjs.com/en/components/images/)
- [Vuetify V2 Aspect Ratios](https://v2.vuetifyjs.com/en/components/aspect-ratios/)
- [Vuetify V2 Parallax](https://v15.vuetifyjs.com/en/components/parallax/)
