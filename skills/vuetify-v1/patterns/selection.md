# Vuetify 1.5 Selection Patterns

## v-btn-toggle (V1 Button Groups)

**Note**: V1.5 uses `v-btn-toggle`, V2 uses `v-btn-group`.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `dark` | boolean | false | Dark theme |
| `light` | boolean | false | Light theme |
| `mandatory` | boolean | false | Require selection |
| `max` | number | - | Max selections (multiple) |
| `multiple` | boolean | false | Allow multiple |
| `value` | any | - | Selected value(s) |

### Single Selection

```vue
<v-btn-toggle v-model="alignment">
  <v-btn flat>
    <v-icon>format_align_left</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_center</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_right</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_align_justify</v-icon>
  </v-btn>
</v-btn-toggle>
```

### Multiple Selection

```vue
<v-btn-toggle v-model="format" multiple>
  <v-btn flat>
    <v-icon>format_bold</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_italic</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_underlined</v-icon>
  </v-btn>
  <v-btn flat>
    <v-icon>format_strikethrough</v-icon>
  </v-btn>
</v-btn-toggle>
```

### Mandatory Selection

```vue
<v-btn-toggle v-model="selection" mandatory>
  <v-btn flat value="option1">Option 1</v-btn>
  <v-btn flat value="option2">Option 2</v-btn>
</v-btn-toggle>
```

### With Values

```vue
<v-btn-toggle v-model="selected">
  <v-btn flat value="list">
    <v-icon>view_list</v-icon>
  </v-btn>
  <v-btn flat value="grid">
    <v-icon>view_grid</v-icon>
  </v-btn>
  <v-btn flat value="table">
    <v-icon>table_chart</v-icon>
  </v-btn>
</v-btn-toggle>

<!-- selected will be 'list', 'grid', or 'table' -->
```

## v-carousel

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `active-class` | string | - | Active item class |
| `cycle` | boolean | true | Auto-cycle |
| `dark` | boolean | false | Dark theme |
| `delimiter-icon` | string | '$vuetify.icons.delimiter' | Delimiter icon |
| `height` | number/string | 500 | Height |
| `hide-controls` | boolean | false | Hide controls |
| `hide-delimiters` | boolean | false | Hide delimiters |
| `interval` | number | 6000 | Cycle interval (ms) |
| `light` | boolean | false | Light theme |
| `mandatory` | boolean | true | Require selection |
| `max` | number | - | Max selections |
| `next-icon` | string | '$vuetify.icons.next' | Next icon |
| `prev-icon` | string | '$vuetify.icons.prev' | Previous icon |
| `reverse` | boolean | false | Reverse cycle |
| `touch` | object | - | Touch options |
| `value` | number | - | Active slide |

### Basic Carousel

```vue
<v-carousel>
  <v-carousel-item
    v-for="(item, i) in items"
    :key="i"
    :src="item.src"
  />
</v-carousel>
```

### Carousel with Custom Content

```vue
<v-carousel cycle interval="5000">
  <v-carousel-item
    v-for="(slide, i) in slides"
    :key="i"
  >
    <v-layout fill-height align-center justify-center>
      <v-flex text-xs-center>
        <h1>{{ slide.title }}</h1>
        <p>{{ slide.description }}</p>
      </v-flex>
    </v-layout>
  </v-carousel-item>
</v-carousel>
```

### Hide Controls/Delimiters

```vue
<v-carousel hide-controls hide-delimiters>
  <v-carousel-item v-for="item in items" :src="item.src" :key="item.id" />
</v-carousel>
```

### Controlled Carousel

```vue
<template>
  <v-carousel v-model="slide">
    <v-carousel-item v-for="item in items" :src="item.src" :key="item.id" />
  </v-carousel>
  <v-btn @click="slide = (slide + 1) % items.length">Next</v-btn>
</template>

<script>
export default {
  data() {
    return {
      slide: 0,
      items: [...]
    }
  }
}
</script>
```

## v-stepper (Multi-Step Selection)

### Horizontal Stepper

```vue
<v-stepper v-model="step">
  <v-stepper-header>
    <v-stepper-step :complete="step > 1" step="1">
      Step 1
    </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 2" step="2">
      Step 2
    </v-stepper-step>
    <v-divider />
    <v-stepper-step step="3">Step 3</v-stepper-step>
  </v-stepper-header>

  <v-stepper-items>
    <v-stepper-content step="1">
      <v-card>
        <v-card-text>Step 1 content</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="step = 2">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>

    <v-stepper-content step="2">
      <v-card>
        <v-card-text>Step 2 content</v-card-text>
        <v-card-actions>
          <v-btn flat @click="step = 1">Back</v-btn>
          <v-btn color="primary" @click="step = 3">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>

    <v-stepper-content step="3">
      <v-card>
        <v-card-text>Step 3 content</v-card-text>
        <v-card-actions>
          <v-btn flat @click="step = 2">Back</v-btn>
          <v-btn color="primary" @click="submit">Finish</v-btn>
        </v-card-actions>
      </v-card>
    </v-stepper-content>
  </v-stepper-items>
</v-stepper>
```

### Vertical Stepper

```vue
<v-stepper v-model="step" vertical>
  <v-stepper-step :complete="step > 1" step="1">
    Select campaign
    <small>Choose your campaign settings</small>
  </v-stepper-step>
  <v-stepper-content step="1">
    <v-card>
      <v-card-text>Campaign selection content</v-card-text>
    </v-card>
    <v-btn color="primary" @click="step = 2">Continue</v-btn>
  </v-stepper-content>

  <v-stepper-step :complete="step > 2" step="2">
    Create ad group
    <small>Define your ad group</small>
  </v-stepper-step>
  <v-stepper-content step="2">
    <v-card>
      <v-card-text>Ad group content</v-card-text>
    </v-card>
    <v-btn flat @click="step = 1">Back</v-btn>
    <v-btn color="primary" @click="step = 3">Continue</v-btn>
  </v-stepper-content>

  <v-stepper-step step="3">
    Create ad
  </v-stepper-step>
  <v-stepper-content step="3">
    <v-card>
      <v-card-text>Ad creation content</v-card-text>
    </v-card>
    <v-btn flat @click="step = 2">Back</v-btn>
    <v-btn color="primary" @click="submit">Finish</v-btn>
  </v-stepper-content>
</v-stepper>
```

### Stepper with Errors

```vue
<v-stepper-step :complete="step > 2" step="2" :rules="[() => valid]">
  Ad Group
  <small>Error message shown here</small>
</v-stepper-step>

<script>
export default {
  computed: {
    valid() {
      // Return false to show error state
      return this.formDataIsValid
    }
  }
}
</script>
```

## v-window

Tab-like selection without tabs:

```vue
<v-window v-model="window">
  <v-window-item v-for="n in 3" :key="`window-${n}`">
    <v-card>
      <v-card-text>
        Window {{ n }} content
      </v-card-text>
    </v-card>
  </v-window-item>
</v-window>

<v-btn @click="window = (window + 1) % 3">Next</v-btn>
```

### Vertical Window

```vue
<v-window v-model="window" vertical>
  <v-window-item v-for="n in 3" :key="n">
    <v-card height="200">
      <v-card-text>Window {{ n }}</v-card-text>
    </v-card>
  </v-window-item>
</v-window>
```

## v-expansion-panel

### Basic Accordion

```vue
<v-expansion-panel>
  <v-expansion-panel-content>
    <div slot="header">Panel 1</div>
    <v-card>
      <v-card-text>Panel 1 content</v-card-text>
    </v-card>
  </v-expansion-panel-content>

  <v-expansion-panel-content>
    <div slot="header">Panel 2</div>
    <v-card>
      <v-card-text>Panel 2 content</v-card-text>
    </v-card>
  </v-expansion-panel-content>

  <v-expansion-panel-content>
    <div slot="header">Panel 3</div>
    <v-card>
      <v-card-text>Panel 3 content</v-card-text>
    </v-card>
  </v-expansion-panel-content>
</v-expansion-panel>
```

### Controlled Accordion

```vue
<template>
  <v-expansion-panel v-model="panel" expand>
    <v-expansion-panel-content>
      <div slot="header">Panel 1</div>
      <v-card><v-card-text>Content 1</v-card-text></v-card>
    </v-expansion-panel-content>
    <v-expansion-panel-content>
      <div slot="header">Panel 2</div>
      <v-card><v-card-text>Content 2</v-card-text></v-card>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  data() {
    return {
      panel: [true, false] // First panel open, second closed
    }
  }
}
</script>
```

### Expand Multiple

```vue
<v-expansion-panel expand>
  <v-expansion-panel-content>
    <div slot="header">Panel 1</div>
    <v-card><v-card-text>Content 1</v-card-text></v-card>
  </v-expansion-panel-content>
  <v-expansion-panel-content>
    <div slot="header">Panel 2</div>
    <v-card><v-card-text>Content 2</v-card-text></v-card>
  </v-expansion-panel-content>
</v-expansion-panel>
```

### With Icons

```vue
<v-expansion-panel>
  <v-expansion-panel-content>
    <div slot="header">
      <v-icon left>settings</v-icon>
      Settings
    </div>
    <v-card><v-card-text>Settings content</v-card-text></v-card>
  </v-expansion-panel-content>
</v-expansion-panel>
```