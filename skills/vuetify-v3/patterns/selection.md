# Selection Patterns

Comprehensive patterns for Vuetify V3 selection and content pane components.

## Chip Groups

### v-chip-group

Interactive chip group for tag selection and filters.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Selected value(s) |
| `multiple` | boolean | Allow multiple selection |
| `column` | boolean | Stack chips vertically |
| `selected-class` | string | CSS class for selected chips |
| `mandatory` | boolean | Require at least one selection |

**V3 Changes:**
- Use `v-model` instead of `value`
- `active-class` → `selected-class`

```vue
<!-- Single selection -->
<v-chip-group v-model="selected">
  <v-chip filter value="vue">Vue.js</v-chip>
  <v-chip filter value="react">React</v-chip>
  <v-chip filter value="angular">Angular</v-chip>
</v-chip-group>

<!-- Multiple selection -->
<v-chip-group v-model="selected" multiple column>
  <v-chip filter value="frontend">Frontend</v-chip>
  <v-chip filter value="backend">Backend</v-chip>
  <v-chip filter value="devops">DevOps</v-chip>
  <v-chip filter value="mobile">Mobile</v-chip>
</v-chip-group>

<!-- With selected class -->
<v-chip-group v-model="selected" selected-class="text-primary">
  <v-chip filter value="option1">Option 1</v-chip>
  <v-chip filter value="option2">Option 2</v-chip>
</v-chip-group>

<!-- Mandatory selection (at least one) -->
<v-chip-group v-model="selected" mandatory>
  <v-chip filter value="option1">Option 1</v-chip>
  <v-chip filter value="option2">Option 2</v-chip>
</v-chip-group>

<script setup>
import { ref } from 'vue'

const selected = ref([])
</script>
```

## Button Groups

### v-btn-group

Button group for selection between options.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Selected value |
| `variant` | string | Style: `text`, `outlined`, `flat`, `elevated`, `tonal` |
| `divided` | boolean | Add dividers between buttons |
| `mandatory` | boolean | Require one button to be selected |
| `multiple` | boolean | Allow multiple selection |
| `color` | string | Active button color |

**V3 Changes:**
- Renamed from `v-btn-toggle` to `v-btn-group`
- Use `v-model` for selection

```vue
<!-- Single selection -->
<v-btn-group v-model="selected" variant="outlined" divided>
  <v-btn value="list">
    <v-icon icon="mdi-view-list" />
  </v-btn>
  <v-btn value="grid">
    <v-icon icon="mdi-view-grid" />
  </v-btn>
</v-btn-group>

<!-- Multiple selection -->
<v-btn-group v-model="selected" multiple variant="outlined">
  <v-btn value="bold">
    <v-icon icon="mdi-format-bold" />
  </v-btn>
  <v-btn value="italic">
    <v-icon icon="mdi-format-italic" />
  </v-btn>
  <v-btn value="underline">
    <v-icon icon="mdi-format-underline" />
  </v-btn>
</v-btn-group>

<!-- Text formatting toolbar -->
<v-btn-group v-model="format" multiple divided>
  <v-btn value="bold">
    <v-icon icon="mdi-format-bold" />
  </v-btn>
  <v-btn value="italic">
    <v-icon icon="mdi-format-italic" />
  </v-btn>
  <v-btn value="underline">
    <v-icon icon="mdi-format-underline" />
  </v-btn>
  <v-btn value="strike">
    <v-icon icon="mdi-format-strikethrough" />
  </v-btn>
</v-btn-group>

<!-- View switcher -->
<v-btn-group v-model="view" mandatory>
  <v-btn value="list">
    <v-icon icon="mdi-view-list" />
    <span class="ml-2">List</span>
  </v-btn>
  <v-btn value="grid">
    <v-icon icon="mdi-view-grid" />
    <span class="ml-2">Grid</span>
  </v-btn>
  <v-btn value="card">
    <v-icon icon="mdi-view-card" />
    <span class="ml-2">Card</span>
  </v-btn>
</v-btn-group>

<script setup>
import { ref } from 'vue'

const selected = ref([])
const format = ref([])
const view = ref('list')
</script>
```

## Carousels

### v-carousel

Display multiple visual content with slides.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | number | Current slide |
| `cycle` | boolean | Auto-cycle slides |
| `interval` | number | Cycle interval (ms) |
| `height` | number/string | Carousel height |
| `show-arrows` | boolean/string | Show navigation arrows: `true`, `false`, `hover` |
| `hide-delimiters` | boolean | Hide bottom delimiters |
| `progress` | boolean | Show progress bar |
| `progress-color` | string | Progress bar color |

**V3 Changes:**
- Use `v-model` instead of `value`
- `v-carousel-item` replaces `v-carousel-item`

```vue
<v-carousel v-model="slide" cycle height="400" hide-delimiters>
  <v-carousel-item
    v-for="(item, i) in items"
    :key="i"
    :src="item.src"
    cover
  >
    <v-card-title>{{ item.title }}</v-card-title>
  </v-carousel-item>
</v-carousel>

<!-- With controls -->
<v-carousel
  v-model="slide"
  height="400"
  show-arrows="hover"
  progress="primary"
>
  <v-carousel-item src="slide1.jpg" cover />
  <v-carousel-item src="slide2.jpg" cover />
  <v-carousel-item src="slide3.jpg" cover />
</v-carousel>

<!-- Custom content -->
<v-carousel v-model="slide" height="300">
  <v-carousel-item>
    <v-sheet height="100%" color="primary" class="d-flex align-center justify-center">
      <div class="text-h2">Slide 1</div>
    </v-sheet>
  </v-carousel-item>
  <v-carousel-item>
    <v-sheet height="100%" color="secondary" class="d-flex align-center justify-center">
      <div class="text-h2">Slide 2</div>
    </v-sheet>
  </v-carousel-item>
</v-carousel>

<script setup>
import { ref } from 'vue'

const slide = ref(0)

const items = [
  { src: 'image1.jpg', title: 'First Slide' },
  { src: 'image2.jpg', title: 'Second Slide' },
  { src: 'image3.jpg', title: 'Third Slide' },
]
</script>
```

## Windows

### v-window

Content panes controlled by model.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any | Current window |
| `prev-icon` | string | Previous button icon |
| `next-icon` | string | Next button icon |
| `show-arrows` | boolean/string | Show navigation arrows |
| `continuous` | boolean | Loop through items |

**V3 Changes:**
- Use `v-window` with `v-window-item` instead of `v-tabs-items` with `v-tab-item`

```vue
<v-window v-model="step">
  <v-window-item value="step1">
    <v-card>
      <v-card-title>Step 1</v-card-title>
      <v-card-text>First step content</v-card-text>
    </v-card>
  </v-window-item>

  <v-window-item value="step2">
    <v-card>
      <v-card-title>Step 2</v-card-title>
      <v-card-text>Second step content</v-card-text>
    </v-card>
  </v-window-item>

  <v-window-item value="step3">
    <v-card>
      <v-card-title>Step 3</v-card-title>
      <v-card-text>Third step content</v-card-text>
    </v-card>
  </v-window-item>
</v-window>

<v-btn @click="step = 'step1'">Step 1</v-btn>
<v-btn @click="step = 'step2'">Step 2</v-btn>
<v-btn @click="step = 'step3'">Step 3</v-btn>

<script setup>
import { ref } from 'vue'

const step = ref('step1')
</script>

<!-- Onboarding wizard -->
<v-window v-model="onboarding" show-arrows>
  <v-window-item value="welcome">
    <v-card height="300">
      <v-card-title>Welcome!</v-card-title>
      <v-card-text>Let's get started...</v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="onboarding = 'setup'">
          Get Started
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-window-item>

  <v-window-item value="setup">
    <v-card height="300">
      <v-card-title>Setup</v-card-title>
      <v-card-text>Configure your account...</v-card-text>
      <v-card-actions>
        <v-btn @click="onboarding = 'welcome'">Back</v-btn>
        <v-spacer />
        <v-btn color="primary" @click="onboarding = 'complete'">
          Complete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-window-item>

  <v-window-item value="complete">
    <v-card height="300">
      <v-card-title>All Done!</v-card-title>
      <v-card-text>You're all set up.</v-card-text>
    </v-card>
  </v-window-item>
</v-window>
```

## Steppers

### v-stepper

Linear progress for multi-step forms.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | number/string | Current step |
| `alt-labels` | boolean | Alternative label position |
| `editable` | boolean | Allow clicking steps |
| `non-linear` | boolean | Allow skipping steps |

**V3 Changes:**
- `v-stepper-step` → `v-stepper-item`
- `v-stepper-content` → `v-stepper-window` with `v-stepper-window-item`
- Use `v-stepper-actions` for action buttons

```vue
<v-stepper v-model="step">
  <v-stepper-header>
    <v-stepper-item :value="1" title="Step 1" complete />
    <v-divider />
    <v-stepper-item :value="2" title="Step 2" />
    <v-divider />
    <v-stepper-item :value="3" title="Step 3" />
  </v-stepper-header>

  <v-stepper-window>
    <v-stepper-window-item :value="1">
      <v-card>
        <v-card-title>Step 1</v-card-title>
        <v-card-text>First step content</v-card-text>
      </v-card>
    </v-stepper-window-item>

    <v-stepper-window-item :value="2">
      <v-card>
        <v-card-title>Step 2</v-card-title>
        <v-card-text>Second step content</v-card-text>
      </v-card>
    </v-stepper-window-item>

    <v-stepper-window-item :value="3">
      <v-card>
        <v-card-title>Step 3</v-card-title>
        <v-card-text>Third step content</v-card-text>
      </v-card>
    </v-stepper-window-item>
  </v-stepper-window>

  <v-stepper-actions>
    <v-btn @click="step--" :disabled="step === 1">Back</v-btn>
    <v-btn color="primary" @click="step++">
      {{ step === 3 ? 'Finish' : 'Next' }}
    </v-btn>
  </v-stepper-actions>
</v-stepper>

<!-- Editable stepper -->
<v-stepper v-model="step" alt-labels editable>
  <v-stepper-header>
    <v-stepper-item :value="1" title="Personal Info" />
    <v-divider />
    <v-stepper-item :value="2" title="Contact Info" />
    <v-divider />
    <v-stepper-item :value="3" title="Review" />
  </v-stepper-header>

  <v-stepper-window>
    <v-stepper-window-item :value="1">
      <v-form>
        <v-text-field label="Name" />
        <v-text-field label="Email" />
      </v-form>
    </v-stepper-window-item>

    <v-stepper-window-item :value="2">
      <v-form>
        <v-text-field label="Phone" />
        <v-text-field label="Address" />
      </v-form>
    </v-stepper-window-item>

    <v-stepper-window-item :value="3">
      <v-card>
        <v-card-title>Review Your Information</v-card-title>
        <v-card-text>
          <!-- Summary -->
        </v-card-text>
      </v-card>
    </v-stepper-window-item>
  </v-stepper-window>

  <v-stepper-actions>
    <v-btn @click="step--" :disabled="step === 1">Back</v-btn>
    <v-btn color="primary" @click="submit">
      {{ step === 3 ? 'Submit' : 'Next' }}
    </v-btn>
  </v-stepper-actions>
</v-stepper>

<script setup>
import { ref } from 'vue'

const step = ref(1)
</script>
```

## Expansion Panels

### v-expansion-panels

Reveal additional content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | any/array | Open panel(s) |
| `multiple` | boolean | Allow multiple open panels |
| `accordion` | boolean | Only one panel open at a time |
| `popout` | boolean | Popout style |
| `inset` | boolean | Inset style |
| `tile` | boolean | Tile style (no rounded corners) |

**V3 Changes:**
- `v-expansion-panel-content` removed, use `v-expansion-panel-text`
- Use `v-model` for controlled state

```vue
<!-- Basic expansion panels -->
<v-expansion-panels>
  <v-expansion-panel>
    <v-expansion-panel-title>Panel 1</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 1
    </v-expansion-panel-text>
  </v-expansion-panel>

  <v-expansion-panel>
    <v-expansion-panel-title>Panel 2</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 2
    </v-expansion-panel-text>
  </v-expansion-panel>
</v-expansion-panels>

<!-- Accordion (one open at a time) -->
<v-expansion-panels accordion>
  <v-expansion-panel value="panel1">
    <v-expansion-panel-title>Panel 1</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 1
    </v-expansion-panel-text>
  </v-expansion-panel>

  <v-expansion-panel value="panel2">
    <v-expansion-panel-title>Panel 2</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 2
    </v-expansion-panel-text>
  </v-expansion-panel>
</v-expansion-panels>

<!-- Multiple open panels -->
<v-expansion-panels v-model="openPanels" multiple>
  <v-expansion-panel value="panel1">
    <v-expansion-panel-title>Panel 1</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 1
    </v-expansion-panel-text>
  </v-expansion-panel>

  <v-expansion-panel value="panel2">
    <v-expansion-panel-title>Panel 2</v-expansion-panel-title>
    <v-expansion-panel-text>
      Content for panel 2
    </v-expansion-panel-text>
  </v-expansion-panel>
</v-expansion-panels>

<!-- FAQ style -->
<v-expansion-panels>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-icon icon="mdi-help-circle" start />
      Frequently Asked Question
    </v-expansion-panel-title>
    <v-expansion-panel-text>
      Answer to the frequently asked question.
    </v-expansion-panel-text>
  </v-expansion-panel>
</v-expansion-panels>

<script setup>
import { ref } from 'vue'

const openPanels = ref([])
</script>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Chip group not selecting | Use `v-model` and `value` on chips |
| Button group mandatory | Add `mandatory` prop to require selection |
| Carousel not cycling | Add `cycle` prop for auto-cycling |
| Window not switching | Check `v-model` value matches `value` on items |
| Stepper not showing content | Use `v-stepper-window` with `v-stepper-window-item` |
| Expansion panel not opening | Check `v-model` and `value` props |
| Multiple expansion panels | Add `multiple` prop to `v-expansion-panels` |
| Expansion panel style | Use `accordion`, `popout`, `inset`, or `tile` props |