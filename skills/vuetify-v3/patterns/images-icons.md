# Images and Icons Patterns

Comprehensive patterns for Vuetify V3 image and icon components.

## Images

### v-img

Flexible image display with lazy loading and placeholder support.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `src` | string | Image source URL |
| `alt` | string | Alt text |
| `width` | number/string | Width |
| `height` | number/string | Height |
| `max-width` | number/string | Maximum width |
| `max-height` | number/string | Maximum height |
| `cover` | boolean | Cover container |
| `contain` | boolean | Contain within container |
| `lazy-src` | string | Placeholder image |
| `gradient` | string | CSS gradient overlay |
| `aspect-ratio` | number/string | Aspect ratio |

**V3 Changes:**
- Same props as V2

```vue
<!-- Basic image -->
<v-img src="image.jpg" alt="Description" />

<!-- Fixed dimensions -->
<v-img src="image.jpg" width="300" height="200" />

<!-- Cover mode -->
<v-img src="image.jpg" height="300" cover />

<!-- Contain mode -->
<v-img src="image.jpg" width="300" height="300" contain />

<!-- Aspect ratio -->
<v-img src="image.jpg" aspect-ratio="16/9" />

<!-- With gradient overlay -->
<v-img src="image.jpg" height="300" gradient="to top right, rgba(0,0,0,.7), rgba(0,0,0,.3)">
  <v-card-title class="text-white">Title</v-card-title>
</v-img>

<!-- Lazy loading -->
<v-img src="image.jpg" lazy-src="placeholder.jpg" />

<!-- With placeholder -->
<v-img src="image.jpg" height="300">
  <template #placeholder>
    <v-skeleton-loader type="image" height="300" />
  </template>
</v-img>

<!-- Card with image -->
<v-card max-width="400">
  <v-img src="image.jpg" height="200" cover />
  <v-card-title>Card Title</v-card-title>
</v-card>

<!-- Gallery -->
<v-container>
  <v-row>
    <v-col
      v-for="image in images"
      :key="image.id"
      cols="12"
      sm="6"
      md="4"
    >
      <v-img :src="image.url" :alt="image.title" height="200" cover />
    </v-col>
  </v-row>
</v-container>
```

### v-avatar

User avatars with image or icon.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `image` | string | Avatar image URL |
| `icon` | string | Icon name |
| `color` | string | Background color |
| `size` | number/string | Size: `x-small`, `small`, `default`, `large`, `x-large` or number |
| `rounded` | string/boolean | Border radius |

```vue
<!-- Image avatar -->
<v-avatar image="user.jpg" />

<!-- Icon avatar -->
<v-avatar color="primary">
  <v-icon icon="mdi-account" />
</v-avatar>

<!-- Text avatar -->
<v-avatar color="primary">
  <span class="text-white">JD</span>
</v-avatar>

<!-- Sizes -->
<v-avatar image="user.jpg" size="x-small" />
<v-avatar image="user.jpg" size="small" />
<v-avatar image="user.jpg" size="default" />
<v-avatar image="user.jpg" size="large" />
<v-avatar image="user.jpg" size="x-large" />
<v-avatar image="user.jpg" :size="48" />

<!-- Rounded -->
<v-avatar image="user.jpg" rounded="0" />
<v-avatar image="user.jpg" rounded="sm" />
<v-avatar image="user.jpg" rounded="lg" />
<v-avatar image="user.jpg" rounded="xl" />

<!-- Avatar group -->
<v-avatar-group>
  <v-avatar image="user1.jpg" />
  <v-avatar image="user2.jpg" />
  <v-avatar image="user3.jpg" />
</v-avatar-group>

<!-- Avatar with badge -->
<v-badge dot color="success" location="bottom end">
  <v-avatar image="user.jpg" />
</v-badge>

<!-- Avatar in list -->
<v-list>
  <v-list-item>
    <template #prepend>
      <v-avatar image="user.jpg" />
    </template>
    <v-list-item-title>John Doe</v-list-item-title>
    <v-list-item-subtitle>john@example.com</v-list-item-subtitle>
  </v-list-item>
</v-list>
```

### v-parallax

3D scrolling effect for hero sections.

```vue
<v-parallax src="hero.jpg" height="400">
  <v-row class="fill-height" align="center" justify="center">
    <v-col class="text-center">
      <h1 class="text-h2 text-white">Hero Title</h1>
      <p class="text-white">Hero subtitle</p>
    </v-col>
  </v-row>
</v-parallax>

<!-- With content overlay -->
<v-parallax src="background.jpg" height="600">
  <v-container fill-height>
    <v-row align="center" justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="text-h3 text-white mb-4">Welcome</h1>
        <v-btn color="primary" size="large">Get Started</v-btn>
      </v-col>
    </v-row>
  </v-container>
</v-parallax>
```

## Icons

### v-icon

Material Design Icons and custom icons.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `icon` | string | Icon name (MDI: `mdi-*`) |
| `color` | string | Icon color |
| `size` | string/number | Size: `x-small`, `small`, `default`, `large`, `x-large` or number |
| `start` | boolean | Margin start |
| `end` | boolean | Margin end |
| `left` | boolean | Left position (deprecated, use `start`) |
| `right` | boolean | Right position (deprecated, use `end`) |

**V3 Changes:**
- Use `icon` prop instead of default slot content
- `left`/`right` props → `start`/`end` props

```vue
<!-- Basic icon (V3 syntax) -->
<v-icon icon="mdi-home" />

<!-- Colored icon -->
<v-icon icon="mdi-home" color="primary" />

<!-- Icon sizes -->
<v-icon icon="mdi-home" size="x-small" />
<v-icon icon="mdi-home" size="small" />
<v-icon icon="mdi-home" size="default" />
<v-icon icon="mdi-home" size="large" />
<v-icon icon="mdi-home" size="x-large" />
<v-icon icon="mdi-home" :size="48" />

<!-- Icon in button -->
<v-btn prepend-icon="mdi-home">Home</v-btn>
<v-btn append-icon="mdi-arrow-right">Next</v-btn>
<v-btn icon="mdi-home" />

<!-- Icon in text field -->
<v-text-field prepend-icon="mdi-account" label="Name" />
<v-text-field append-icon="mdi-search" label="Search" />

<!-- Icon in list item -->
<v-list-item prepend-icon="mdi-home">
  <v-list-item-title>Home</v-list-item-title>
</v-list-item>

<!-- Icon in card -->
<v-card-title>
  <v-icon icon="mdi-account" start />
  User Profile
</v-card-title>

<!-- Icon colors -->
<v-icon icon="mdi-home" color="primary" />
<v-icon icon="mdi-home" color="success" />
<v-icon icon="mdi-home" color="warning" />
<v-icon icon="mdi-home" color="error" />
<v-icon icon="mdi-home" color="info" />
<v-icon icon="mdi-home" color="#FF5722" />
```

### Icon Setup

**MDI Font (CSS) - Easiest:**

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

**MDI SVG (Recommended for Production):**

```javascript
// src/plugins/vuetify.js
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { mdiHome, mdiAccount, mdiSettings } from '@mdi/js'

export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases: {
      ...aliases,
      home: mdiHome,
      account: mdiAccount,
      settings: mdiSettings,
    },
    sets: {
      mdi,
    },
  },
})
```

**Using Custom Aliases:**

```vue
<!-- Use custom alias -->
<v-icon icon="$home" />
<v-icon icon="$account" />
<v-icon icon="$settings" />
```

### Other Icon Sets

**Material Icons:**

```javascript
import { aliases, md } from 'vuetify/iconsets/md'

export default createVuetify({
  icons: {
    defaultSet: 'md',
    aliases,
    sets: {
      md,
    },
  },
})
```

```vue
<v-icon icon="home" />
```

**FontAwesome:**

```javascript
import { aliases, fa } from 'vuetify/iconsets/fa-svg'

export default createVuetify({
  icons: {
    defaultSet: 'fa',
    aliases,
    sets: {
      fa,
    },
  },
})
```

```vue
<v-icon icon="fas fa-home" />
```

### Common Icon Patterns

```vue
<!-- Icon button -->
<v-btn icon="mdi-magnify" />

<!-- Icon with text -->
<v-btn prepend-icon="mdi-home">Home</v-btn>

<!-- Icon in chip -->
<v-chip>
  <v-icon icon="mdi-account" start />
  John Doe
</v-chip>

<!-- Icon in alert -->
<v-alert type="info" icon="mdi-bell">
  New notification
</v-alert>

<!-- Icon in badge -->
<v-badge content="5" color="error">
  <v-icon icon="mdi-bell" />
</v-badge>

<!-- Icon in tooltip -->
<v-tooltip text="Edit">
  <template #activator="{ props }">
    <v-icon icon="mdi-pencil" v-bind="props" />
  </template>
</v-tooltip>

<!-- Icon in expansion panel -->
<v-expansion-panel>
  <v-expansion-panel-title>
    <v-icon icon="mdi-help-circle" start />
    FAQ
  </v-expansion-panel-title>
  <v-expansion-panel-text>
    Answer to the question.
  </v-expansion-panel-text>
</v-expansion-panel>

<!-- Icon in card actions -->
<v-card>
  <v-card-actions>
    <v-btn icon="mdi-heart" color="error" />
    <v-btn icon="mdi-share" />
    <v-spacer />
    <v-btn icon="mdi-bookmark" />
  </v-card-actions>
</v-card>
```

## Aspect Ratio

### v-responsive

Maintain aspect ratios for layout.

```vue
<!-- 16:9 aspect ratio -->
<v-responsive aspect-ratio="16/9">
  <v-img src="video-thumbnail.jpg" />
</v-responsive>

<!-- 4:3 aspect ratio -->
<v-responsive aspect-ratio="4/3">
  <v-img src="image.jpg" />
</v-responsive>

<!-- 1:1 (square) -->
<v-responsive aspect-ratio="1">
  <v-img src="square.jpg" />
</v-responsive>

<!-- Custom aspect ratio -->
<v-responsive aspect-ratio="21/9">
  <v-img src="ultrawide.jpg" />
</v-responsive>

<!-- With content -->
<v-responsive aspect-ratio="16/9">
  <v-card>
    <v-card-title>Video Player</v-card-title>
  </v-card>
</v-responsive>

<!-- Flexible height -->
<v-responsive :aspect-ratio="aspectRatio">
  <v-img src="image.jpg" />
</v-responsive>

<script setup>
import { ref } from 'vue'

const aspectRatio = ref(16/9)
</script>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Image not loading | Check `src` URL and CORS settings |
| Icon not showing | Install MDI font or configure SVG icons |
| Avatar size not changing | Use `size` prop with number or size string |
| Parallax not scrolling | Check height and container |
| Image not covering | Use `cover` prop |
| Image not containing | Use `contain` prop |
| Icon color not applying | Use `color` prop |
| Icon size not working | Use `size` prop with number or size string |
| Aspect ratio not working | Check aspect-ratio format (`16/9` or decimal) |
| Icon alias not working | Register aliases in Vuetify config |
| MDI icons not showing | Import MDI CSS or configure SVG iconset |