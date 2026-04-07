# Vuetify 1.5 Images & Icons Patterns

## v-icon

**CRITICAL**: V1.5 uses slot syntax for icons, NOT a prop (different from V2).

```vue
<!-- Vuetify 1.5 (correct) -->
<v-icon>home</v-icon>
<v-icon>mdi-account</v-icon>

<!-- Vuetify 2 (different!) -->
<v-icon icon="home" />
```

### Icon Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | string | undefined | Theme color or CSS color |
| `dark` | boolean | false | Dark theme |
| `disabled` | boolean | false | Disabled state |
| `large` | boolean | false | 36px size |
| `left` | boolean | false | Left position in button |
| `light` | boolean | false | Light theme |
| `medium` | boolean | false | 28px size |
| `right` | boolean | false | Right position in button |
| `size` | number/string | undefined | Custom size |
| `small` | boolean | false | 16px size |
| `x-large` | boolean | false | 40px size |

### Icon Sizes

| Prop | Size |
|------|------|
| `small` | 16px |
| default | 24px |
| `medium` | 28px |
| `large` | 36px |
| `x-large` | 40px |

### Basic Icons

```vue
<!-- Material Icons (default) -->
<v-icon>home</v-icon>
<v-icon>favorite</v-icon>
<v-icon>settings</v-icon>

<!-- Material Design Icons (mdi) -->
<v-icon>mdi-account</v-icon>
<v-icon>mdi-facebook</v-icon>
<v-icon>mdi-twitter</v-icon>

<!-- Font Awesome (fa) -->
<v-icon>fa fa-user</v-icon>
<v-icon>fa fa-home</v-icon>
```

### Icon Colors

```vue
<v-icon color="primary">home</v-icon>
<v-icon color="success">check_circle</v-icon>
<v-icon color="error">error</v-icon>
<v-icon color="#FF5722">star</v-icon>
```

### Icons in Buttons

```vue
<v-btn color="primary">
  <v-icon left>add</v-icon>
  Add Item
</v-btn>

<v-btn color="primary">
  Continue
  <v-icon right>arrow_forward</v-icon>
</v-btn>

<v-btn icon color="primary">
  <v-icon>settings</v-icon>
</v-btn>
```

### Icon Sizes

```vue
<v-icon small>star</v-icon>
<v-icon>star</v-icon>
<v-icon medium>star</v-icon>
<v-icon large>star</v-icon>
<v-icon x-large>star</v-icon>

<!-- Custom size -->
<v-icon :size="48">star</v-icon>
```

### Clickable Icons

```vue
<v-icon @click="toggle">star</v-icon>

<v-icon
  large
  :color="liked ? 'error' : 'grey'"
  @click="liked = !liked"
>
  {{ liked ? 'favorite' : 'favorite_border' }}
</v-icon>
```

## v-img

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `alt` | string | - | Alt text |
| `aspect-ratio` | number/string | - | Aspect ratio |
| `contain` | boolean | false | Contain image |
| `gradient` | string | - | CSS gradient overlay |
| `height` | number/string | - | Height |
| `lazy-src` | string | - | Lazy load placeholder |
| `max-height` | number/string | - | Max height |
| `max-width` | number/string | - | Max width |
| `min-height` | number/string | - | Min height |
| `min-width` | number/string | - | Min width |
| `position` | string | 'center center' | Background position |
| `sizes` | string | - | Sizes for srcset |
| `src` | string | - | Image source (required) |
| `srcset` | string | - | Srcset attribute |
| `transition` | string | 'fade-transition' | Transition |
| `width` | number/string | - | Width |

### Basic Image

```vue
<v-img src="/images/photo.jpg" height="200" />
```

### Aspect Ratio

```vue
<v-img
  src="/images/photo.jpg"
  aspect-ratio="16/9"
/>
```

### Contain

```vue
<v-img
  src="/images/photo.jpg"
  height="300"
  contain
/>
```

### Lazy Loading

```vue
<v-img
  src="/images/high-res.jpg"
  lazy-src="/images/placeholder.jpg"
  height="300"
/>
```

### With Placeholder

```vue
<v-img
  src="/images/photo.jpg"
  height="300"
>
  <v-layout
    slot="placeholder"
    fill-height
    align-center
    justify-center
  >
    <v-progress-circular indeterminate color="grey" />
  </v-layout>
</v-img>
```

### Gradient Overlay

```vue
<v-img
  src="/images/photo.jpg"
  gradient="to top right, rgba(100,115,201,.33), rgba(25,32,72,.7)"
  height="300"
/>
```

### Responsive Grid

```vue
<v-layout row wrap>
  <v-flex xs6 md4 lg3 v-for="image in images" :key="image.id">
    <v-img :src="image.url" aspect-ratio="1" />
  </v-flex>
</v-layout>
```

## v-avatar

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | string | - | Background color |
| `size` | number/string | 48 | Avatar size |
| `tile` | boolean | false | Remove border radius |

### Image Avatar

```vue
<v-avatar size="36">
  <img src="/images/avatar.jpg" alt="Avatar">
</v-avatar>
```

### Text Avatar

```vue
<v-avatar color="primary">
  <span class="white--text headline">JD</span>
</v-avatar>

<v-avatar color="teal">
  <span class="white--text headline">AB</span>
</v-avatar>
```

### Icon Avatar

```vue
<v-avatar color="indigo">
  <v-icon dark>account_circle</v-icon>
</v-avatar>
```

### Sizes

```vue
<v-avatar size="24"><img src="/avatar.jpg"></v-avatar>
<v-avatar size="48"><img src="/avatar.jpg"></v-avatar>
<v-avatar size="64"><img src="/avatar.jpg"></v-avatar>
<v-avatar size="128"><img src="/avatar.jpg"></v-avatar>
```

### Avatar in List

```vue
<v-list>
  <v-list-tile avatar>
    <v-list-tile-avatar>
      <img src="/avatar.jpg">
    </v-list-tile-avatar>
    <v-list-tile-content>
      <v-list-tile-title>John Doe</v-list-tile-title>
      <v-list-tile-sub-title>johndoe@example.com</v-list-tile-sub-title>
    </v-list-tile-content>
  </v-list-tile>
</v-list>
```

## v-parallax

```vue
<v-parallax src="/images/hero.jpg" height="600">
  <v-layout column align-center justify-center>
    <h1 class="white--text">Welcome</h1>
  </v-layout>
</v-parallax>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `alt` | string | - | Alt text |
| `height` | number/string | - | Height |
| `src` | string | - | Image source |

## v-responsive

Maintains aspect ratio for any content:

```vue
<v-responsive :aspect-ratio="16/9">
  <iframe
    src="https://www.youtube.com/embed/..."
    frameborder="0"
    allowfullscreen
  ></iframe>
</v-responsive>
```

## Card Media

**Note**: V1.5 has `v-card-media`, V2 uses `v-img` instead.

```vue
<v-card>
  <v-card-media
    src="/images/photo.jpg"
    height="200px"
  >
    <v-layout fill-height align-center justify-center>
      <h3 class="white--text">Overlay Text</h3>
    </v-layout>
  </v-card-media>
  <v-card-title>Card Title</v-card-title>
</v-card>
```

### Card Media Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `height` | number/string | - | Height |
| `src` | string | - | Image source |
| `contain` | boolean | false | Contain image |