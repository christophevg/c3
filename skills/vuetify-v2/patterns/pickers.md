# Pickers Patterns

Comprehensive patterns for Vuetify V2 picker components.

## Color Selection

### v-color-picker
Visual color selection with support for multiple color modes.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | string \| object | Selected color (Hex string or color object) |
| `mode` | string | Current mode (`rgba`, `rgb`, `hsla`, `hsl`, `hexa`, `hex`) |
| `modes` | array | Array of available modes to switch between |
| `show-swatches` | boolean | Enables predefined color swatches |
| `swatches` | array | 2D array of color strings |
| `hide-canvas` | boolean | Hide the main color canvas |
| `hide-sliders` | boolean | Hide the adjustment sliders |
| `hide-inputs` | boolean | Hide the text inputs |

**Key Events:**
| Event | Description |
| :--- | :--- |
| `@input` | Emitted on every color change (High frequency) |
| `@update:mode` | Emitted when the color mode is changed |

**Example:**
```vue
<v-color-picker 
  v-model="color" 
  mode="hexa" 
  show-swatches 
  :swatches="[['#FF0000', '#00FF00'], ['#0000FF', '#FFFFFF']]" 
/>
```
*Performance Tip: Use debouncing for API calls triggered by `@input`.*

## Date & Time Selection

### v-date-picker
Visual calendar for selecting dates or months.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | string | Date in ISO 8601 format (`YYYY-MM-DD` or `YYYY-MM`) |
| `type` | string | `'date'` (default) or `'month'` |
| `multiple` | boolean | Allows selecting multiple dates (model must be an array) |
| `allowed-dates` | function | Function to disable specific dates |
| `reactive` | boolean | Automatically updates model when changing month/year |
| `landscape` | boolean | Switches to horizontal orientation |

**Example:**
```vue
<v-date-picker 
  v-model="date" 
  color="primary" 
  reactive 
  @input="onDateSelected"
/>
```

### v-time-picker
Visual clock for selecting time.

**Key Props:**
| Prop | Type | Description |
| :--- | :--- | :--- |
| `v-model` | string | Time in 24hr format (`HH:mm`) |
| `format` | string | `'ampm'` (default) or `'24hr'` (Controls display only) |
| `use-seconds` | boolean | Includes seconds in the picker |
| `allowed-hours` | function | Function to restrict hour selection |
| `allowed-minutes` | function | Function to restrict minute selection |
| `landscape` | boolean | Switches to horizontal orientation |

**Example:**
```vue
<v-time-picker 
  v-model="time" 
  format="24hr" 
  color="primary" 
/>
```

## See Also
- [Vuetify V2 Color Pickers](https://www.mintlify.com/vuetifyjs/vuetify/components/color-picker)
- [Vuetify V2 Date Pickers](https://v15.vuetifyjs.com/en/components/date-pickers/)
- [Vuetify V2 Time Pickers](https://v15.vuetifyjs.com/en/components/time-pickers/)
