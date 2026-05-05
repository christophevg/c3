# Pickers Patterns

Comprehensive patterns for Vuetify V3 picker components.

## Date Picker

### v-date-picker

Date and month selection.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | string/array | Selected date(s) |
| `min` | string | Minimum date |
| `max` | string | Maximum date |
| `allowed-dates` | function | Function to filter allowed dates |
| `disabled` | boolean | Disable picker |
| `readonly` | boolean | Read-only mode |
| `multiple` | boolean | Allow multiple selection |
| `range` | boolean | Allow range selection |
| `show-adjacent-months` | boolean | Show prev/next month days |
| `hide-header` | boolean | Hide header |
| `title` | string | Picker title |
| `header` | string | Header text (deprecated) |
| `color` | string | Selected date color |
| `elevation` | number | Shadow elevation |

**V3 Changes:**
- Use `v-model` instead of `value`
- `@input` event → `@update:model-value`

```vue
<!-- Basic date picker -->
<v-date-picker v-model="date" />

<!-- With title -->
<v-date-picker v-model="date" title="Select Date" />

<!-- With min/max -->
<v-date-picker
  v-model="date"
  min="2024-01-01"
  max="2024-12-31"
/>

<!-- Allowed dates -->
<v-date-picker
  v-model="date"
  :allowed-dates="allowedDates"
/>

<script setup>
import { ref } from 'vue'

const date = ref(new Date().toISOString().substr(0, 10))

const allowedDates = (date) => {
  // Only allow weekdays
  const day = new Date(date).getDay()
  return day !== 0 && day !== 6
}
</script>

<!-- Multiple selection -->
<v-date-picker v-model="dates" multiple />

<!-- Range selection -->
<v-date-picker v-model="dates" range />

<!-- Show adjacent months -->
<v-date-picker v-model="date" show-adjacent-months />

<!-- Custom colors -->
<v-date-picker v-model="date" color="primary" />
<v-date-picker v-model="date" color="success" />

<!-- In dialog -->
<v-dialog v-model="dialog" max-width="400">
  <template #activator="{ props }">
    <v-btn v-bind="props">
      {{ date || 'Select Date' }}
    </v-btn>
  </template>
  <v-card>
    <v-date-picker v-model="date" />
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="saveDate">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<!-- Date picker with text field -->
<v-text-field
  v-model="formattedDate"
  label="Select Date"
  prepend-icon="mdi-calendar"
  readonly
  @click="dialog = true"
/>

<v-dialog v-model="dialog" max-width="400">
  <v-card>
    <v-date-picker v-model="date" @update:model-value="dialog = false" />
  </v-card>
</v-dialog>

<script setup>
import { ref, computed } from 'vue'

const date = ref(null)
const dialog = ref(false)

const formattedDate = computed(() => {
  if (!date.value) return ''
  return new Date(date.value).toLocaleDateString()
})
</script>
```

## Time Picker

### v-time-picker

Time selection.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | string | Selected time |
| `min` | string | Minimum time |
| `max` | string | Maximum time |
| `allowed-hours` | function/array | Filter allowed hours |
| `allowed-minutes` | function/array | Filter allowed minutes |
| `allowed-seconds` | function/array | Filter allowed seconds |
| `format` | string | Time format: `ampm`, `24hr` |
| `use-seconds` | boolean | Show seconds |
| `disabled` | boolean | Disable picker |
| `readonly` | boolean | Read-only mode |
| `color` | string | Selected time color |
| `elevation` | number | Shadow elevation |

```vue
<!-- Basic time picker -->
<v-time-picker v-model="time" />

<!-- 24-hour format -->
<v-time-picker v-model="time" format="24hr" />

<!-- With seconds -->
<v-time-picker v-model="time" use-seconds />

<!-- With min/max -->
<v-time-picker
  v-model="time"
  min="09:00"
  max="17:00"
/>

<!-- Allowed hours/minutes -->
<v-time-picker
  v-model="time"
  :allowed-hours="allowedHours"
  :allowed-minutes="allowedMinutes"
/>

<script setup>
import { ref } from 'vue'

const time = ref('12:00')

const allowedHours = (hour) => {
  // Only allow 9 AM to 5 PM
  return hour >= 9 && hour <= 17
}

const allowedMinutes = (minute) => {
  // Only allow 15-minute intervals
  return minute % 15 === 0
}
</script>

<!-- In dialog -->
<v-dialog v-model="dialog" max-width="400">
  <template #activator="{ props }">
    <v-btn v-bind="props">
      {{ time || 'Select Time' }}
    </v-btn>
  </template>
  <v-card>
    <v-time-picker v-model="time" format="24hr" />
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="saveTime">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<!-- Time picker with text field -->
<v-text-field
  v-model="formattedTime"
  label="Select Time"
  prepend-icon="mdi-clock"
  readonly
  @click="dialog = true"
/>

<v-dialog v-model="dialog" max-width="400">
  <v-card>
    <v-time-picker v-model="time" @update:model-value="dialog = false" />
  </v-card>
</v-dialog>

<script setup>
import { ref, computed } from 'vue'

const time = ref(null)
const dialog = ref(false)

const formattedTime = computed(() => {
  if (!time.value) return ''
  return time.value
})
</script>
```

## Color Picker

### v-color-picker

Visual color selection.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `v-model` | string | Selected color (hex, rgb, hsl) |
| `mode` | string | Color mode: `rgba`, `hsla`, `hexa` |
| `hide-inputs` | boolean | Hide input fields |
| `hide-canvas` | boolean | Hide color canvas |
| `hide-sliders` | boolean | Hide sliders |
| `disabled` | boolean | Disable picker |
| `dot-size` | number | Size of selection dot |
| `swatches` | array | Preset color swatches |
| `swatches-max-height` | number | Max height of swatches |
| `show-swatches` | boolean | Show color swatches |
| `elevation` | number | Shadow elevation |

```vue
<!-- Basic color picker -->
<v-color-picker v-model="color" />

<!-- With swatches -->
<v-color-picker
  v-model="color"
  :swatches="swatches"
  show-swatches
/>

<script setup>
import { ref } from 'vue'

const color = ref('#FF0000')

const swatches = [
  ['#FF0000', '#AA0000', '#550000'],
  ['#00FF00', '#00AA00', '#005500'],
  ['#0000FF', '#0000AA', '#000055'],
  ['#FFFF00', '#AAAA00', '#555500'],
]
</script>

<!-- Hide inputs -->
<v-color-picker v-model="color" hide-inputs />

<!-- Hide canvas -->
<v-color-picker v-model="color" hide-canvas />

<!-- Hide sliders -->
<v-color-picker v-model="color" hide-sliders />

<!-- Color mode -->
<v-color-picker v-model="color" mode="rgba" />
<v-color-picker v-model="color" mode="hsla" />
<v-color-picker v-model="color" mode="hexa" />

<!-- In dialog -->
<v-dialog v-model="dialog" max-width="400">
  <template #activator="{ props }">
    <v-btn v-bind="props">
      <v-icon icon="mdi-palette" start />
      Choose Color
    </v-btn>
  </template>
  <v-card>
    <v-card-title>Select Color</v-card-title>
    <v-card-text>
      <v-color-picker v-model="color" />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="saveColor">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<!-- Color picker with preview -->
<v-row align="center">
  <v-col cols="auto">
    <v-sheet
      :color="color"
      width="100"
      height="100"
      rounded
    />
  </v-col>
  <v-col>
    <v-color-picker v-model="color" hide-inputs />
  </v-col>
</v-row>
```

## Labs Components

### VDateInput (Labs)

Date input field (experimental).

```vue
<!-- Must import from labs -->
<script setup>
import { VDateInput } from 'vuetify/labs/VDateInput'
</script>

<template>
  <v-date-input
    v-model="date"
    label="Select Date"
    prepend-icon="mdi-calendar"
  />
</template>
```

### VColorInput (Labs)

Color input field (experimental).

```vue
<!-- Must import from labs -->
<script setup>
import { VColorInput } from 'vuetify/labs/VColorInput'
</script>

<template>
  <v-color-input
    v-model="color"
    label="Select Color"
    prepend-icon="mdi-palette"
  />
</template>
```

### VMaskInput (Labs)

Masked input field (experimental).

```vue
<!-- Must import from labs -->
<script setup>
import { VMaskInput } from 'vuetify/labs/VMaskInput'
</script>

<template>
  <v-mask-input
    v-model="phone"
    label="Phone Number"
    mask="(###) ###-####"
  />
</template>
```

## Common Picker Patterns

### Date Range Picker

```vue
<v-date-picker v-model="dateRange" range />

<script setup>
import { ref } from 'vue'

const dateRange = ref([])
</script>
```

### DateTime Picker (Combined)

```vue
<v-dialog v-model="dialog" max-width="600">
  <template #activator="{ props }">
    <v-text-field
      v-bind="props"
      :model-value="formattedDateTime"
      label="Select Date & Time"
      prepend-icon="mdi-calendar-clock"
      readonly
    />
  </template>

  <v-card>
    <v-tabs v-model="tab">
      <v-tab value="date">Date</v-tab>
      <v-tab value="time">Time</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="date">
        <v-date-picker v-model="date" />
      </v-window-item>
      <v-window-item value="time">
        <v-time-picker v-model="time" format="24hr" />
      </v-window-item>
    </v-window>

    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="saveDateTime">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

<script setup>
import { ref, computed } from 'vue'

const dialog = ref(false)
const tab = ref('date')
const date = ref(null)
const time = ref(null)

const formattedDateTime = computed(() => {
  if (!date.value || !time.value) return ''
  return `${date.value} ${time.value}`
})

const saveDateTime = () => {
  dialog.value = false
}
</script>
```

### Date Picker Form

```vue
<v-form ref="form" v-model="valid">
  <v-text-field
    v-model="event.title"
    label="Event Title"
    required
  />

  <v-menu>
    <template #activator="{ props }">
      <v-text-field
        v-bind="props"
        v-model="event.date"
        label="Event Date"
        prepend-icon="mdi-calendar"
        readonly
      />
    </template>
    <v-date-picker v-model="event.date" />
  </v-menu>

  <v-menu>
    <template #activator="{ props }">
      <v-text-field
        v-bind="props"
        v-model="event.time"
        label="Event Time"
        prepend-icon="mdi-clock"
        readonly
      />
    </template>
    <v-time-picker v-model="event.time" format="24hr" />
  </v-menu>

  <v-btn :disabled="!valid" color="primary" @click="submit">
    Create Event
  </v-btn>
</v-form>

<script setup>
import { ref } from 'vue'

const valid = ref(false)
const event = ref({
  title: '',
  date: null,
  time: null,
})

const submit = () => {
  // Submit event
}
</script>
```

### Birthday Picker

```vue
<v-date-picker
  v-model="birthday"
  :max="maxDate"
  title="Select Birthday"
  color="primary"
/>

<script setup>
import { ref, computed } from 'vue'

const birthday = ref(null)

const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().substr(0, 10)
})
</script>
```

### Event Calendar Picker

```vue
<v-date-picker
  v-model="selectedDate"
  :events="eventDates"
  event-color="primary"
/>

<script setup>
import { ref } from 'vue'

const selectedDate = ref(null)

const eventDates = ref([
  '2024-01-15',
  '2024-01-20',
  '2024-02-14',
  '2024-03-17',
])
</script>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Date format incorrect | Use ISO format `YYYY-MM-DD` for v-model |
| Time format incorrect | Use `HH:MM` format (24-hour) or `HH:MM AM/PM` |
| Color picker value wrong | Use hex `#RRGGBB` or `rgba(r,g,b,a)` format |
| Picker not updating | Use `v-model` and listen to `@update:model-value` |
| Allowed dates not working | Return `true`/`false` from `allowed-dates` function |
| Time picker AM/PM | Use `format="ampm"` for 12-hour format |
| Date picker range | Use `range` prop and `v-model` array |
| Multiple date selection | Use `multiple` prop and `v-model` array |
| Labs components not found | Import from `vuetify/labs/VComponentName` |
| Color swatches not showing | Add `show-swatches` prop and `swatches` array |