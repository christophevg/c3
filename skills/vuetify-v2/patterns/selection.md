# Selection Patterns

Comprehensive patterns for Vuetify V2 selection components.

## Content Panes & Transitions

### v-window
The baseline component for transitioning content between panes. It is the foundation for `v-carousel` and `v-stepper`.

**Key Props:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `v-model` | Any | - | Manages the visibility/active index |
| `vertical` | Boolean | false | Activates vertical transition |
| `reverse` | Boolean | false | Triggers reverse transition |
| `touchless` | Boolean | false | Disables touch support |
| `mandatory` | Boolean | false | Forces a selection to be active |

**Example:**
```vue
<v-window v-model="windowIndex">
  <v-window-item>
    <p>Pane 1 Content</p>
  </v-window-item>
  <v-window-item>
    <p>Pane 2 Content</p>
  </v-window-item>
</v-window>
```

### v-carousel
A slideshow component for cycling through images or content panes.

**Key Props:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `v-model` | Any | - | Controls the active slide index |
| `cycle` | Boolean | true | Automatically transitions to the next slide |
| `interval` | Number/String | 6000 | Milliseconds between automatic cycles |
| `height` | Number/String | 500 | Height of the carousel |
| `hide-controls` | Boolean | false | Hides navigation arrows |
| `hide-delimiters` | Boolean | false | Hides the bottom indicator dots |
| `vertical` | Boolean | false | Uses vertical transitions |

**Key Slots:**
| Slot | Description |
| :--- | :--- |
| `default` | Area for `v-carousel-item` components |
| `prev` | Customize the "previous" arrow button |
| `next` | Customize the "next" arrow button |

**Example:**
```vue
<v-carousel cycle interval="5000" height="400">
  <v-carousel-item>
    <v-img src="img1.jpg" alt="Slide 1"></v-img>
  </v-carousel-item>
  <v-carousel-item>
    <v-img src="img2.jpg" alt="Slide 2"></v-img>
  </v-carousel-item>
</v-carousel>
```

### v-stepper
Displays progress through a series of numbered steps, useful for multi-step forms.

**Key Props:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `v-model` | Number/String | - | Manages active step |
| `non-linear` | Boolean | false | Allows jumping between any steps |
| `vertical` | Boolean | false | Displays steps on the y-axis |
| `alt-labels` | Boolean | false | Places labels under the step |

**Example:**
```vue
<v-stepper vertical non-linear>
  <v-stepper-header>
    <v-stepper-step>Step 1</v-stepper-step>
    <v-stepper-step>Step 2</v-stepper-step>
  </v-stepper-header>
  <v-stepper-content>Content 1</v-stepper-content>
  <v-stepper-content>Content 2</v-stepper-content>
</v-stepper>
```

## Toggle Selection

### v-btn-group (V2 Alternative to v-btn-toggle)
Vuetify V2 does not have a standalone `v-btn-toggle`. Use `v-btn-group` or a set of buttons with a custom active state.

**Example:**
```vue
<v-btn-group v-model="selected">
  <v-btn value="left">Left</v-btn>
  <v-btn value="center">Center</v-btn>
  <v-btn value="right">Right</v-btn>
</v-btn-group>
```

## See Also
- [Vuetify V2 Carousels](https://v2.vuetifyjs.com/en/components/carousels/)
- [Vuetify V2 Windows](https://v15.vuetifyjs.com/en/components/windows/)
- [Vuetify V2 Steppers](https://v15.vuetifyjs.com/en/components/steppers/)
