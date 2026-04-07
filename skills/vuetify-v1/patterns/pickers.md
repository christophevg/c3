# Vuetify 1.5 Pickers Patterns

## v-date-picker

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `allowed-dates` | function | - | Allowed dates function |
| `color` | string | 'primary' | Picker color |
| `dark` | boolean | false | Dark theme |
| `day-format` | function | - | Day format function |
| `disabled` | boolean | false | Disabled state |
| `events` | array/function | - | Event dates |
| `event-color` | string/function | - | Event color |
| `first-day-of-week` | number/string | 0 | First day (0 = Sunday) |
| `header-color` | string | - | Header color |
| `landscape` | boolean | false | Landscape mode |
| `light` | boolean | false | Light theme |
| `locale` | string | 'en-us' | Locale |
| `max` | string | - | Maximum date |
| `min` | string | - | Minimum date |
| `month-format` | function | - | Month format |
| `next-icon` | string | '$vuetify.icons.next' | Next icon |
| `no-title` | boolean | false | Hide title |
| `picker-date` | string | - | Picker date |
| `prev-icon` | string | '$vuetify.icons.prev' | Previous icon |
| `reactive` | boolean | false | Reactive month change |
| `readonly` | boolean | false | Read-only mode |
| `scrollable` | boolean | false | Enable scroll |
| `show-current` | boolean/string | - | Show current date |
| `show-week` | boolean | false | Show week numbers |
| `type` | string | 'date' | Type: 'date' or 'month' |
| `value` | string/array | - | Selected date |
| `weekday-format` | function | - | Weekday format |
| `width` | number/string | 290 | Picker width |
| `year-format` | function | - | Year format |
| `year-icon` | string | - | Year icon |

### Basic Date Picker

```vue
<template>
  <v-date-picker v-model="date"></v-date-picker>
</template>

<script>
export default {
  data() {
    return {
      date: new Date().toISOString().substr(0, 10)
    }
  }
}
</script>
```

### Date Picker with Menu

```vue
<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    full-width
    min-width="290"
  >
    <v-text-field
      slot="activator"
      v-model="date"
      label="Select Date"
      prepend-icon="event"
      readonly
    />
    <v-date-picker v-model="date" @input="menu = false" />
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      date: new Date().toISOString().substr(0, 10),
      menu: false
    }
  }
}
</script>
```

### Date Range

```vue
<v-date-picker v-model="dates" multiple></v-date-picker>

<!-- Or range with allowed-dates -->
<v-date-picker
  v-model="range"
  :allowed-dates="allowedDates"
></v-date-picker>

<script>
export default {
  data() {
    return {
      range: null,
      startDate: '2024-01-01',
      endDate: '2024-12-31'
    }
  },
  methods: {
    allowedDates(date) {
      const d = new Date(date)
      return d >= new Date(this.startDate) && d <= new Date(this.endDate)
    }
  }
}
</script>
```

### Min/Max Dates

```vue
<v-date-picker
  v-model="date"
  :min="minDate"
  :max="maxDate"
/>
```

### Allowed Dates Function

```vue
<v-date-picker
  v-model="date"
  :allowed-dates="allowedDates"
/>

<script>
export default {
  methods: {
    allowedDates(date) {
      // Only allow weekdays
      const d = new Date(date)
      const day = d.getDay()
      return day !== 0 && day !== 6 // No weekends
    }
  }
}
</script>
```

### Events

```vue
<v-date-picker
  v-model="date"
  :events="events"
  event-color="green lighten-1"
/>

<script>
export default {
  data() {
    return {
      date: null,
      events: ['2024-01-15', '2024-01-20', '2024-02-14']
    }
  }
}
</script>
```

### Landscape Mode

```vue
<v-date-picker v-model="date" landscape></v-date-picker>
```

### Month Picker

```vue
<v-date-picker v-model="month" type="month"></v-date-picker>
```

### Localization

```vue
<v-date-picker
  v-model="date"
  locale="fr-fr"
  first-day-of-week="1"
></v-date-picker>
```

## v-time-picker

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `allowed-hours` | function/array | - | Allowed hours |
| `allowed-minutes` | function/array | - | Allowed minutes |
| `allowed-seconds` | function/array | - | Allowed seconds |
| `color` | string | 'primary' | Picker color |
| `dark` | boolean | false | Dark theme |
| `disabled` | boolean | false | Disabled state |
| `format` | string | - | 'ampm' or '24hr' |
| `header-color` | string | - | Header color |
| `landscape` | boolean | false | Landscape mode |
| `light` | boolean | false | Light theme |
| `min` | string | - | Minimum time |
| `max` | string | - | Maximum time |
| `no-title` | boolean | false | Hide title |
| `readonly` | boolean | false | Read-only mode |
| `scrollable` | boolean | false | Enable scroll |
| `use-seconds` | boolean | false | Show seconds |
| `value` | string | - | Selected time |
| `width` | number/string | 290 | Picker width |

### Basic Time Picker

```vue
<template>
  <v-time-picker v-model="time"></v-time-picker>
</template>

<script>
export default {
  data() {
    return {
      time: null
    }
  }
}
</script>
```

### Time Picker with Menu

```vue
<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    full-width
    min-width="290"
  >
    <v-text-field
      slot="activator"
      v-model="time"
      label="Select Time"
      prepend-icon="access_time"
      readonly
    />
    <v-time-picker v-model="time" @input="menu = false" />
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      time: null,
      menu: false
    }
  }
}
</script>
```

### 24-Hour Format

```vue
<v-time-picker v-model="time" format="24hr"></v-time-picker>
```

### With Seconds

```vue
<v-time-picker v-model="time" use-seconds></v-time-picker>
```

### Allowed Times

```vue
<v-time-picker
  v-model="time"
  :allowed-hours="[9, 10, 11, 12, 13, 14, 15, 16, 17]"
  :allowed-minutes="[0, 15, 30, 45]"
></v-time-picker>
```

### Min/Max Time

```vue
<v-time-picker
  v-model="time"
  min="09:00"
  max="17:00"
></v-time-picker>
```

## Combined Date/Time Picker

```vue
<template>
  <v-layout row>
    <v-flex xs6 mr-2>
      <v-menu
        v-model="dateMenu"
        :close-on-content-click="false"
        full-width
        min-width="290"
      >
        <v-text-field
          slot="activator"
          v-model="date"
          label="Date"
          prepend-icon="event"
          readonly
        />
        <v-date-picker v-model="date" @input="dateMenu = false" />
      </v-menu>
    </v-flex>
    <v-flex xs6>
      <v-menu
        v-model="timeMenu"
        :close-on-content-click="false"
        full-width
        min-width="290"
      >
        <v-text-field
          slot="activator"
          v-model="time"
          label="Time"
          prepend-icon="access_time"
          readonly
        />
        <v-time-picker v-model="time" @input="timeMenu = false" />
      </v-menu>
    </v-flex>
  </v-layout>
</template>
```