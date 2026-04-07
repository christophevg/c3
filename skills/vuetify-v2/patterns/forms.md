# Forms Patterns

Comprehensive patterns for Vuetify V2 form components and validation.

## Form Container

### v-form

Wraps form elements with validation support.

**Methods:**

| Method | Return | Description |
|--------|--------|-------------|
| `validate()` | boolean | Returns true if all fields valid |
| `reset()` | void | Clears fields and validation |
| `resetValidation()` | void | Clears validation only |

**V2 Compatibility Note:**
Vuetify V2 does not have standalone components for `v-input`, `v-number-input`, or `v-otp-input`.
- For **Numeric Input**: Use `<v-text-field type="number">`.
- For **OTP Input**: Implement a custom group of `v-text-field` components.
- `v-input` is an internal base class and not for direct use.

**Basic Usage:**

```vue
<v-form ref="form" v-model="valid">
  <v-text-field v-model="name" :rules="nameRules" label="Name" required />
  <v-text-field v-model="email" :rules="emailRules" label="Email" required />
  <v-btn :disabled="!valid" @click="submit">Submit</v-btn>
</v-form>

<script>
export default {
  data: () => ({
    valid: false,
    name: '',
    email: '',
    nameRules: [v => !!v || 'Name is required'],
    emailRules: [
      v => !!v || 'Email is required',
      v => /.+@.+\..+/.test(v) || 'Invalid email format'
    ]
  }),
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        // Form is valid, proceed
      }
    }
  }
}
</script>
```

### Validation Rules

Common validation patterns:

```javascript
const rules = {
  required: v => !!v || 'This field is required',
  min: min => v => (v && v.length >= min) || `Minimum ${min} characters`,
  max: max => v => (v && v.length <= max) || `Maximum ${max} characters`,
  email: v => /.+@.+\..+/.test(v) || 'Invalid email format',
  url: v => /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/.test(v) || 'Invalid URL',
  numeric: v => /^[0-9]+$/.test(v) || 'Numbers only',
  alpha: v => /^[a-zA-Z]+$/.test(v) || 'Letters only',
  alphanumeric: v => /^[a-zA-Z0-9]+$/.test(v) || 'Letters and numbers only',
  phone: v => /^\+?[\d\s-]+$/.test(v) || 'Invalid phone number',
  password: v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(v) || 'Password must be 8+ chars with uppercase, lowercase, and number',
  match: (field, fieldName) => v => v === field || `${fieldName} does not match`
}

// Usage
data: () => ({
  rules: {
    name: [rules.required, rules.min(3)],
    email: [rules.required, rules.email],
    password: [rules.required, rules.password],
    confirmPassword: [rules.required, rules.match(this.password, 'Password')]
  }
})
```

## Text Inputs

### v-text-field

Single-line text input with validation.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Field label |
| `placeholder` | string | Placeholder text |
| `hint` | string | Hint text below field |
| `persistent-hint` | boolean | Always show hint |
| `rules` | array | Validation rules |
| `error` | boolean | Force error state |
| `error-messages` | array | Custom error messages |
| `disabled` | boolean | Disable input |
| `readonly` | boolean | Read-only mode |
| `clearable` | boolean | Add clear button |
| `prepend-icon` | string | Icon before input |
| `append-icon` | string | Icon after input |
| `counter` | boolean/number | Character counter |
| `outlined` | boolean | Outlined style |
| `filled` | boolean | Filled style |
| `solo` | boolean | Solo style |
| `dense` | boolean | Dense style |

```vue
<!-- Basic text field -->
<v-text-field v-model="name" label="Name" />

<!-- With validation -->
<v-text-field
  v-model="name"
  :rules="[v => !!v || 'Required']"
  label="Name"
  required
/>

<!-- With icon and counter -->
<v-text-field
  v-model="email"
  prepend-icon="mdi-email"
  counter="100"
  label="Email"
/>

<!-- Outlined style -->
<v-text-field v-model="name" label="Name" outlined />

<!-- Password field -->
<v-text-field
  v-model="password"
  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
  :type="showPassword ? 'text' : 'password'"
  label="Password"
  @click:append="showPassword = !showPassword"
/>

<!-- With error state -->
<v-text-field
  v-model="field"
  error
  error-messages="This field has an error"
  label="Field with Error"
/>
```

### v-textarea

Multi-line text input.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `rows` | number | Number of rows (default: 5) |
| `auto-grow` | boolean | Auto-grow height |
| `row-height` | number | Height per row |
| `no-resize` | boolean | Disable resize |

```vue
<!-- Basic textarea -->
<v-textarea v-model="description" label="Description" />

<!-- Auto-growing -->
<v-textarea v-model="description" label="Description" auto-grow />

<!-- Fixed rows -->
<v-textarea v-model="notes" label="Notes" rows="3" no-resize />

<!-- With counter -->
<v-textarea v-model="bio" counter="500" label="Bio" />
```

## Selection Inputs

### v-select

Dropdown selection from list.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `items` | array | Options array |
| `item-text` | string | Property for display text |
| `item-value` | string | Property for value |
| `multiple` | boolean | Enable multi-select |
| `chips` | boolean | Display as chips (multiple) |
| `small-chips` | boolean | Small chips |
| `deletable-chips` | boolean | Removable chips |
| `clearable` | boolean | Add clear button |
| `menu-props` | object | Props for v-menu |

```vue
<!-- Basic select -->
<v-select
  v-model="selected"
  :items="['Option 1', 'Option 2', 'Option 3']"
  label="Options"
/>

<!-- With objects -->
<v-select
  v-model="selected"
  :items="users"
  item-text="name"
  item-value="id"
  label="User"
/>

<!-- Multiple select with chips -->
<v-select
  v-model="selected"
  :items="tags"
  multiple
  chips
  small-chips
  label="Tags"
/>

<!-- With custom slot -->
<v-select v-model="selected" :items="items" label="Items">
  <template v-slot:selection="{ item, index }">
    <v-chip v-if="index < 3">
      {{ item }}
    </v-chip>
    <span v-else-if="index === 3" class="grey--text">
      (+{{ selected.length - 3 }} more)
    </span>
  </template>
</v-select>
```

### v-autocomplete

Type-ahead selection with search.

**Additional Props:**

| Prop | Type | Description |
|------|------|-------------|
| `search` | string | Search query |
| `filter` | function | Custom filter function |
| `no-filter` | boolean | Disable filtering |
| `cache-items` | boolean | Cache search results |

```vue
<!-- Basic autocomplete -->
<v-autocomplete
  v-model="selected"
  :items="items"
  label="Search"
/>

<!-- With async search -->
<v-autocomplete
  v-model="selected"
  :items="items"
  :search-input.sync="search"
  label="Search users"
  @update:search="searchUsers"
/>

<!-- Custom item slot -->
<v-autocomplete
  v-model="selected"
  :items="users"
  item-text="name"
  item-value="id"
  label="User"
>
  <template v-slot:item="{ item }">
    <v-list-item-avatar>
      <v-img :src="item.avatar" />
    </v-list-item-avatar>
    <v-list-item-content>
      <v-list-item-title>{{ item.name }}</v-list-item-title>
      <v-list-item-subtitle>{{ item.email }}</v-list-item-subtitle>
    </v-list-item-content>
  </template>
</v-autocomplete>
```

### v-combobox

Select from list with custom entry.

```vue
<!-- Allow custom entries -->
<v-combobox
  v-model="tags"
  :items="suggestedTags"
  multiple
  chips
  label="Tags"
/>
```

## Chip Selection

### v-chip-group

Makes chips interactive for tag selection and filters. Wraps `v-chip` components and provides selection behavior.

**Key Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | any | - | Selected value(s) |
| `multiple` | boolean | false | Enable multi-select |
| `mandatory` | boolean | false | Require at least one selection |
| `active-class` | string | - | CSS class for selected chips |
| `column` | boolean | false | Display chips in column layout |
| `center-active` | boolean | false | Center the active chip |

**Key Events:**

| Event | Description |
|-------|-------------|
| `change` | Emitted when selection changes |

**Single Selection:**

```vue
<template>
  <v-chip-group v-model="selected" mandatory>
    <v-chip>Option 1</v-chip>
    <v-chip>Option 2</v-chip>
    <v-chip>Option 3</v-chip>
  </v-chip-group>
</template>

<script>
export default {
  data: () => ({
    selected: 0 // Index of selected chip
  })
}
</script>
```

**Multiple Selection:**

```vue
<template>
  <v-chip-group v-model="selected" multiple column>
    <v-chip filter>Tag 1</v-chip>
    <v-chip filter>Tag 2</v-chip>
    <v-chip filter>Tag 3</v-chip>
  </v-chip-group>
</template>

<script>
export default {
  data: () => ({
    selected: [0, 2] // Array of selected indices
  })
}
</script>
```

**Filter Chips with Active Class:**

```vue
<v-chip-group v-model="filter" active-class="primary--text" mandatory>
  <v-chip filter outlined>All</v-chip>
  <v-chip filter outlined>Active</v-chip>
  <v-chip filter outlined>Inactive</v-chip>
  <v-chip filter outlined>Pending</v-chip>
</v-chip-group>
```

**With Custom Colors:**

```vue
<v-chip-group v-model="category" mandatory>
  <v-chip color="primary" filter>Electronics</v-chip>
  <v-chip color="success" filter>Books</v-chip>
  <v-chip color="warning" filter>Clothing</v-chip>
  <v-chip color="error" filter>Sports</v-chip>
</v-chip-group>
```

**Dynamic Items:**

```vue
<template>
  <v-chip-group v-model="selected" multiple column>
    <v-chip
      v-for="tag in tags"
      :key="tag.id"
      :value="tag.id"
      filter
    >
      {{ tag.name }}
    </v-chip>
  </v-chip-group>
</template>

<script>
export default {
  data: () => ({
    selected: [],
    tags: [
      { id: 1, name: 'Vue.js' },
      { id: 2, name: 'React' },
      { id: 3, name: 'Angular' }
    ]
  })
}
</script>
```

**Combined with v-chip Props:**

```vue
<v-chip-group v-model="selected" multiple>
  <v-chip filter outlined>Outlined</v-chip>
  <v-chip filter large>Large</v-chip>
  <v-chip filter small>Small</v-chip>
  <v-chip filter label>Label</v-chip>
</v-chip-group>
```

**Usage in Form:**

```vue
<v-form ref="form" v-model="valid">
  <v-label>Filter by status:</v-label>
  <v-chip-group v-model="status" column active-class="primary--text">
    <v-chip filter>All</v-chip>
    <v-chip filter>Active</v-chip>
    <v-chip filter>Pending</v-chip>
    <v-chip filter>Archived</v-chip>
  </v-chip-group>

  <v-label>Select tags:</v-label>
  <v-chip-group v-model="tags" multiple column>
    <v-chip
      v-for="tag in availableTags"
      :key="tag"
      :value="tag"
      filter
    >
      {{ tag }}
    </v-chip>
  </v-chip-group>
</v-form>
```

**Use Cases:**

| Use Case | Configuration |
|----------|---------------|
| Filter categories | `mandatory` + single selection |
| Multi-select tags | `multiple` + `column` |
| Tab alternative | `mandatory` + `active-class` |
| Toggle buttons | With `filter` chips |
| Status filter | `mandatory` + styled chips |

## Boolean Inputs

### v-checkbox

Checkbox for boolean/multi-select.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Label text |
| `value` | any | Value when checked |
| `true-value` | any | Value when true |
| `false-value` | any | Value when false |
| `indeterminate` | boolean | Indeterminate state |
| `hide-details` | boolean | Hide validation details |

```vue
<!-- Single checkbox -->
<v-checkbox v-model="agree" label="I agree to terms" />

<!-- Multiple checkboxes -->
<v-checkbox
  v-model="selected"
  v-for="option in options"
  :key="option.value"
  :label="option.label"
  :value="option.value"
/>

<!-- With custom true/false values -->
<v-checkbox
  v-model="status"
  label="Active"
  true-value="active"
  false-value="inactive"
/>
```

### v-switch

Toggle switch for on/off.

```vue
<!-- Basic switch -->
<v-switch v-model="enabled" label="Enable feature" />

<!-- With color -->
<v-switch v-model="dark" label="Dark mode" color="primary" />

<!-- With inset style -->
<v-switch v-model="notifications" label="Notifications" inset />
```

### v-radio

Radio button for single choice.

```vue
<!-- Radio group -->
<v-radio-group v-model="selected" label="Choose option">
  <v-radio label="Option 1" value="opt1" />
  <v-radio label="Option 2" value="opt2" />
  <v-radio label="Option 3" value="opt3" />
</v-radio-group>

<!-- With color -->
<v-radio-group v-model="color">
  <v-radio label="Red" value="red" color="red" />
  <v-radio label="Green" value="green" color="green" />
  <v-radio label="Blue" value="blue" color="blue" />
</v-radio-group>
```

## Range Inputs

### v-slider

Single value slider.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `min` | number | Minimum value |
| `max` | number | Maximum value |
| `step` | number | Step increment |
| `thumb-label` | boolean | Show thumb label |
| `ticks` | boolean | Show tick marks |
| `thumb-color` | string | Thumb color |

```vue
<!-- Basic slider -->
<v-slider v-model="volume" label="Volume" />

<!-- With thumb label -->
<v-slider v-model="price" label="Price" thumb-label />

<!-- With ticks -->
<v-slider v-model="rating" :max="5" :step="1" ticks label="Rating" />
```

### v-range-slider

Range selection slider.

```vue
<!-- Price range -->
<v-range-slider
  v-model="priceRange"
  :min="0"
  :max="1000"
  label="Price Range"
  thumb-label
/>
```

## File Upload

### v-file-input

File selection and upload.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `accept` | string | Accepted file types |
| `multiple` | boolean | Multiple files |
| `show-size` | boolean | Show file size |
| `prepend-icon` | string | Icon before input |
| `truncate-length` | number | Truncate file name |

```vue
<!-- Basic file input -->
<v-file-input v-model="file" label="Upload file" />

<!-- With type restriction -->
<v-file-input
  v-model="image"
  accept="image/*"
  label="Upload image"
  prepend-icon="mdi-camera"
/>

<!-- Multiple files with size -->
<v-file-input
  v-model="files"
  multiple
  show-size
  label="Upload files"
/>

<!-- With preview -->
<v-file-input
  v-model="file"
  accept="image/*"
  label="Upload image"
  @change="previewImage"
/>
<img v-if="preview" :src="preview" />
```

## Complete Form Pattern

### Login Form

```vue
<v-form ref="form" v-model="valid" @submit.prevent="submit">
  <v-text-field
    v-model="email"
    :rules="emailRules"
    label="Email"
    prepend-icon="mdi-email"
    required
  />
  <v-text-field
    v-model="password"
    :rules="passwordRules"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :type="showPassword ? 'text' : 'password'"
    label="Password"
    prepend-icon="mdi-lock"
    @click:append="showPassword = !showPassword"
    required
  />
  <v-checkbox v-model="remember" label="Remember me" />
  <v-btn type="submit" color="primary" block :disabled="!valid">
    Login
  </v-btn>
</v-form>
```

### Registration Form

```vue
<v-form ref="form" v-model="valid" lazy-validation>
  <v-row>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="firstName"
        :rules="nameRules"
        label="First Name"
        required
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="lastName"
        :rules="nameRules"
        label="Last Name"
        required
      />
    </v-col>
  </v-row>

  <v-text-field
    v-model="email"
    :rules="emailRules"
    label="Email"
    prepend-icon="mdi-email"
    required
  />

  <v-text-field
    v-model="password"
    :rules="passwordRules"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :type="showPassword ? 'text' : 'password'"
    label="Password"
    prepend-icon="mdi-lock"
    counter
    @click:append="showPassword = !showPassword"
    required
  />

  <v-text-field
    v-model="confirmPassword"
    :rules="[v => v === password || 'Passwords do not match']"
    :type="showPassword ? 'text' : 'password'"
    label="Confirm Password"
    prepend-icon="mdi-lock"
    required
  />

  <v-checkbox
    v-model="agree"
    :rules="[v => v || 'You must agree to continue']"
    label="I agree to the terms and conditions"
    required
  />

  <v-btn
    :disabled="!valid"
    color="primary"
    class="mr-4"
    @click="submit"
  >
    Register
  </v-btn>
  <v-btn @click="reset">Reset</v-btn>
</v-form>
```

### Dynamic Form Fields

```vue
<v-form ref="form" v-model="valid">
  <v-text-field
    v-for="(field, index) in fields"
    :key="index"
    v-model="field.value"
    :label="field.label"
    :rules="field.rules"
    :type="field.type"
  />

  <v-btn @click="addField">Add Field</v-btn>
</v-form>

<script>
export default {
  data: () => ({
    valid: false,
    fields: [
      { label: 'Name', value: '', type: 'text', rules: [v => !!v || 'Required'] }
    ]
  }),
  methods: {
    addField() {
      this.fields.push({
        label: `Field ${this.fields.length + 1}`,
        value: '',
        type: 'text',
        rules: []
      })
    }
  }
}
</script>
```

## Form Validation Pattern

```vue
<template>
  <v-form ref="form" v-model="valid">
    <!-- Fields -->
    <v-btn :disabled="!valid" @click="validateAndSubmit">Submit</v-btn>
  </v-form>
</template>

<script>
export default {
  data: () => ({
    valid: false,
    // fields and rules
  }),
  methods: {
    validateAndSubmit() {
      // Force validation
      if (this.$refs.form.validate()) {
        // All fields valid, submit
        this.submitForm()
      }
    },
    resetForm() {
      this.$refs.form.reset()
    },
    clearValidation() {
      this.$refs.form.resetValidation()
    }
  }
}
</script>
```

## See Also

- [Vuetify Forms](https://vuetifyjs.com/en/components/forms/)
- [Vuetify Text Fields](https://vuetifyjs.com/en/components/text-fields/)
- [Vuetify Selects](https://vuetifyjs.com/en/components/selects/)
- [Vuetify Autocompletes](https://vuetifyjs.com/en/components/autocompletes/)