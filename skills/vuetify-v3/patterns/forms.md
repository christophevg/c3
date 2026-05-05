# Forms Patterns

Comprehensive patterns for Vuetify V3 form components and validation.

## Form Container

### v-form

Wraps form elements with validation support.

**Methods:**

| Method | Return | Description |
|--------|--------|-------------|
| `validate()` | boolean | Returns true if all fields valid |
| `reset()` | void | Clears fields and validation |
| `resetValidation()` | void | Clears validation only |

**V3 New Components:**
- `v-number-input` - Dedicated number input (V3.7.0+)
- `v-otp-input` - OTP/MFA input (V3.4.0+)

**Basic Usage:**

```vue
<v-form ref="form" v-model="valid">
  <v-text-field v-model="name" :rules="nameRules" label="Name" required />
  <v-text-field v-model="email" :rules="emailRules" label="Email" required />
  <v-btn :disabled="!valid" @click="submit">Submit</v-btn>
</v-form>

<script setup>
import { ref } from 'vue'

const form = ref(null)
const valid = ref(false)
const name = ref('')
const email = ref('')

const nameRules = [v => !!v || 'Name is required']
const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Invalid email format'
]

const submit = () => {
  if (form.value.validate()) {
    // Form is valid, proceed
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

// Usage with Composition API
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const nameRules = [rules.required, rules.min(3)]
const emailRules = [rules.required, rules.email]
const passwordRules = [rules.required, rules.password]
const confirmPasswordRules = [rules.required, rules.match(password.value, 'Password')]
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
| `prepend-icon` | string | Icon before input (V3: use `prepend-icon` prop) |
| `append-icon` | string | Icon after input (V3: use `append-icon` prop) |
| `counter` | boolean/number | Character counter |
| `variant` | string | Style variant: `filled`, `outlined`, `plain`, `solo`, `solo-inverted`, `solo-filled`, `underlined` |
| `density` | string | Density: `default`, `comfortable`, `compact` |

**V3 Changes:**
- `outlined`, `filled`, `solo`, `dense` props → use `variant` and `density` props
- `value` prop → `model-value`
- `@input` event → `@update:model-value`

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

<!-- Outlined style (V3) -->
<v-text-field v-model="name" label="Name" variant="outlined" />

<!-- Filled style (V3) -->
<v-text-field v-model="name" label="Name" variant="filled" />

<!-- Solo style (V3) -->
<v-text-field v-model="name" label="Name" variant="solo" />

<!-- Dense (V3) -->
<v-text-field v-model="name" label="Name" density="compact" />

<!-- Password field with toggle -->
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
  label="Error Field"
/>

<!-- Clearable -->
<v-text-field
  v-model="search"
  clearable
  label="Search"
  @click:clear="search = ''"
/>
```

### v-textarea

Multi-line text input.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `auto-grow` | boolean | Auto-grow height |
| `rows` | number | Initial rows (default: 2) |
| `max-rows` | number | Maximum rows when auto-grow |
| `counter` | boolean/number | Character counter |
| `no-resize` | boolean | Disable resize handle |

```vue
<v-textarea
  v-model="description"
  label="Description"
  auto-grow
  :rows="3"
  :max-rows="10"
  counter="500"
  :rules="[v => v.length <= 500 || 'Max 500 characters']"
/>
```

## Number Input (V3.7.0+)

### v-number-input

Dedicated number input with increment/decrement controls.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `min` | number | Minimum value |
| `max` | number | Maximum value |
| `step` | number | Increment step (default: 1) |
| `precision` | number | Decimal precision |
| `control-variant` | string | Control style: `default`, `stacked`, `split` |
| `hide-input` | boolean | Hide input, show only controls |
| `reverse` | boolean | Reverse control position |
| `inset` | boolean | Inset controls |
| `variant` | string | Field variant: `outlined`, `filled`, `solo`, `plain`, `underlined` |

```vue
<!-- Basic number input -->
<v-number-input v-model="quantity" label="Quantity" />

<!-- With min/max/step -->
<v-number-input
  v-model="age"
  :min="0"
  :max="120"
  :step="1"
  label="Age"
/>

<!-- Stacked controls -->
<v-number-input
  v-model="count"
  control-variant="stacked"
  label="Count"
/>

<!-- Split controls -->
<v-number-input
  v-model="price"
  control-variant="split"
  :step="0.01"
  :precision="2"
  label="Price"
/>

<!-- With variant -->
<v-number-input
  v-model="quantity"
  variant="outlined"
  density="compact"
  label="Quantity"
/>
```

## OTP Input (V3.4.0+)

### v-otp-input

One-time password input for MFA/authentication.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `length` | number | Number of OTP digits (default: 6) |
| `autofocus` | boolean | Auto-focus first input |
| `error` | boolean | Error state |
| `disabled` | boolean | Disable all inputs |
| `masked` | boolean | Mask input (password style) |
| `loader` | boolean | Show loading state |

```vue
<v-otp-input
  v-model="otp"
  :length="6"
  autofocus
/>

<!-- Masked OTP -->
<v-otp-input
  v-model="otp"
  :length="6"
  masked
  autofocus
/>

<!-- With validation -->
<v-otp-input
  v-model="otp"
  :length="6"
  :error="!!otpError"
  autofocus
/>

<script setup>
import { ref } from 'vue'

const otp = ref('')
const otpError = ref('')

const validateOtp = () => {
  if (otp.value.length !== 6) {
    otpError.value = 'OTP must be 6 digits'
  } else {
    otpError.value = ''
    // Submit OTP
  }
}
</script>
```

## Selection Inputs

### v-select

Dropdown selection with search capability.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `items` | array | Items to select from |
| `item-title` | string | Property for item label (default: 'title') |
| `item-value` | string | Property for item value (default: 'value') |
| `multiple` | boolean | Allow multiple selection |
| `chips` | boolean | Show selected items as chips |
| `clearable` | boolean | Allow clearing selection |
| `searchable` | boolean | Enable search |
| `hint` | string | Hint text |
| `persistent-hint` | boolean | Always show hint |

**V3 Changes:**
- `value` prop → `model-value`
- `item-text` prop → `item-title`
- `item-value` prop stays same
- `@input` event → `@update:model-value`

```vue
<!-- Basic select -->
<v-select
  v-model="selected"
  :items="items"
  label="Select Item"
/>

<!-- With custom item properties (V3) -->
<v-select
  v-model="selected"
  :items="items"
  item-title="name"
  item-value="id"
  label="Select User"
/>

<!-- Multiple select with chips -->
<v-select
  v-model="selected"
  :items="items"
  multiple
  chips
  label="Select Multiple"
/>

<!-- Searchable select -->
<v-select
  v-model="selected"
  :items="items"
  searchable
  label="Search and Select"
/>

<!-- With custom display -->
<v-select
  v-model="selected"
  :items="items"
  label="Select User"
>
  <template #selection="{ item }">
    <v-chip>
      <v-icon start icon="mdi-account" />
      {{ item.title }}
    </v-chip>
  </template>
  <template #item="{ item, props }">
    <v-list-item v-bind="props">
      <template #prepend>
        <v-avatar :image="item.raw.avatar" />
      </template>
      <v-list-item-title>{{ item.title }}</v-list-item-title>
      <v-list-item-subtitle>{{ item.raw.email }}</v-list-item-subtitle>
    </v-list-item>
  </template>
</v-select>
```

### v-autocomplete

Type-ahead selection with async support.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `items` | array | Items to select from |
| `search` | string | Search query (v-model:search) |
| `loading` | boolean | Show loading state |
| `no-filter` | boolean | Disable client-side filtering |
| `hide-no-data` | boolean | Hide "No data" message |

```vue
<!-- Basic autocomplete -->
<v-autocomplete
  v-model="selected"
  :items="items"
  label="Search and Select"
/>

<!-- Async autocomplete -->
<v-autocomplete
  v-model="selected"
  :items="items"
  :loading="loading"
  :search="search"
  label="Search Users"
  @update:search="searchUsers"
/>

<script setup>
import { ref } from 'vue'

const selected = ref(null)
const items = ref([])
const loading = ref(false)
const search = ref('')

const searchUsers = async (query) => {
  if (!query) return
  loading.value = true
  const response = await fetch(`/api/users?search=${query}`)
  items.value = response.data
  loading.value = false
}
</script>
```

### v-combobox

Select with custom entry capability.

```vue
<v-combobox
  v-model="selected"
  :items="items"
  label="Select or Create"
  multiple
  chips
  clearable
/>
```

### v-checkbox

Boolean or multi-select checkbox.

**V3 Changes:**
- `on-icon` / `off-icon` props → `true-icon` / `false-icon`
- `value` prop → `model-value`
- `@input` event → `@update:model-value`

```vue
<!-- Single checkbox -->
<v-checkbox
  v-model="agree"
  label="I agree to terms"
  :true-icon="mdiCheck"
  :false-icon="mdiCheckboxBlankOutline"
/>

<!-- Checkbox group -->
<v-checkbox
  v-for="item in items"
  :key="item.value"
  v-model="selected"
  :label="item.label"
  :value="item.value"
/>
```

### v-switch

Toggle switch for binary choices.

```vue
<v-switch
  v-model="enabled"
  label="Enable feature"
  color="primary"
  hide-details
/>
```

### v-radio-group

Single choice from multiple options.

```vue
<v-radio-group v-model="selected">
  <v-radio label="Option 1" value="opt1" />
  <v-radio label="Option 2" value="opt2" />
  <v-radio label="Option 3" value="opt3" />
</v-radio-group>
```

## File Input

### v-file-input

File upload with preview support.

```vue
<v-file-input
  v-model="files"
  label="Upload Files"
  multiple
  show-size
  counter
  prepend-icon="mdi-paperclip"
/>

<!-- With file type restriction -->
<v-file-input
  v-model="image"
  label="Upload Image"
  accept="image/*"
  prepend-icon="mdi-camera"
/>

<!-- With chips -->
<v-file-input
  v-model="files"
  label="Upload Files"
  multiple
  chips
  show-size
/>
```

## Range Inputs

### v-slider

Range input for numeric selection.

```vue
<!-- Basic slider -->
<v-slider
  v-model="volume"
  label="Volume"
  :max="100"
  :min="0"
  :step="1"
/>

<!-- With thumb label -->
<v-slider
  v-model="brightness"
  label="Brightness"
  thumb-label
  :max="100"
/>

<!-- Range slider -->
<v-range-slider
  v-model="range"
  label="Price Range"
  :max="1000"
  :min="0"
/>
```

## Form Validation Patterns

### Real-time Validation

```vue
<v-form ref="form" v-model="valid">
  <v-text-field
    v-model="email"
    :rules="emailRules"
    label="Email"
    @update:model-value="validateEmail"
  />
</v-form>

<script setup>
import { ref } from 'vue'

const form = ref(null)
const valid = ref(false)
const email = ref('')

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Invalid email format'
]

const validateEmail = () => {
  // Real-time validation logic
  if (email.value && !/.+@.+\..+/.test(email.value)) {
    // Handle invalid email
  }
}
</script>
```

### Dynamic Form with Conditional Fields

```vue
<v-form>
  <v-select
    v-model="formType"
    :items="['personal', 'business']"
    label="Account Type"
  />

  <v-text-field
    v-if="formType === 'personal'"
    v-model="firstName"
    label="First Name"
  />

  <v-text-field
    v-if="formType === 'business'"
    v-model="companyName"
    label="Company Name"
  />
</v-form>
```

### Multi-Step Form

```vue
<v-stepper v-model="step">
  <v-stepper-header>
    <v-stepper-item :value="1">Personal Info</v-stepper-item>
    <v-divider />
    <v-stepper-item :value="2">Contact Info</v-stepper-item>
    <v-divider />
    <v-stepper-item :value="3">Review</v-stepper-item>
  </v-stepper-header>

  <v-stepper-window>
    <v-stepper-window-item :value="1">
      <v-form ref="form1" v-model="valid1">
        <v-text-field v-model="name" label="Name" :rules="[v => !!v || 'Required']" />
      </v-form>
    </v-stepper-window-item>

    <v-stepper-window-item :value="2">
      <v-form ref="form2" v-model="valid2">
        <v-text-field v-model="email" label="Email" :rules="[v => !!v || 'Required']" />
      </v-form>
    </v-stepper-window-item>

    <v-stepper-window-item :value="3">
      <v-card>
        <v-card-title>Review Your Information</v-card-title>
        <v-card-text>
          <p><strong>Name:</strong> {{ name }}</p>
          <p><strong>Email:</strong> {{ email }}</p>
        </v-card-text>
      </v-card>
    </v-stepper-window-item>
  </v-stepper-window>

  <v-stepper-actions>
    <v-btn @click="step--" :disabled="step === 1">Back</v-btn>
    <v-btn @click="nextStep" color="primary">
      {{ step === 3 ? 'Submit' : 'Next' }}
    </v-btn>
  </v-stepper-actions>
</v-stepper>

<script setup>
import { ref } from 'vue'

const step = ref(1)
const form1 = ref(null)
const form2 = ref(null)
const valid1 = ref(false)
const valid2 = ref(false)

const nextStep = () => {
  if (step.value === 1 && !valid1.value) return
  if (step.value === 2 && !valid2.value) return
  if (step.value < 3) {
    step.value++
  } else {
    // Submit form
  }
}
</script>
```

### Form Reset Pattern

```vue
<v-form ref="form">
  <v-text-field v-model="name" label="Name" />
  <v-text-field v-model="email" label="Email" />
  <v-btn @click="resetForm">Reset</v-btn>
  <v-btn @click="clearValidation">Clear Validation</v-btn>
</v-form>

<script setup>
import { ref } from 'vue'

const form = ref(null)
const name = ref('')
const email = ref('')

const resetForm = () => {
  form.value.reset()
}

const clearValidation = () => {
  form.value.resetValidation()
}
</script>
```

## Form Layout Patterns

### Horizontal Form

```vue
<v-form>
  <v-row>
    <v-col cols="12" md="6">
      <v-text-field v-model="firstName" label="First Name" />
    </v-col>
    <v-col cols="12" md="6">
      <v-text-field v-model="lastName" label="Last Name" />
    </v-col>
  </v-row>
</v-form>
```

### Inline Form

```vue
<v-form class="d-flex align-center">
  <v-text-field v-model="search" label="Search" density="compact" class="mr-2" />
  <v-btn color="primary" type="submit">Search</v-btn>
</v-form>
```

### Form with Validation Summary

```vue
<v-form ref="form" v-model="valid">
  <v-alert v-if="!valid && showErrors" type="error" class="mb-4">
    Please fix the errors below before submitting.
  </v-alert>

  <v-text-field v-model="name" :rules="nameRules" label="Name" />
  <v-text-field v-model="email" :rules="emailRules" label="Email" />

  <v-btn @click="submit" :disabled="!valid">Submit</v-btn>
</v-form>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `v-model` not working | Use `model-value` and `@update:model-value` in V3 |
| Validation not triggering | Check that `v-model` is bound to `<v-form>` |
| Form reset clears values | Use `resetValidation()` to clear only errors |
| Select not showing items | Check `item-title` and `item-value` props (V3 renamed) |
| Checkbox icons incorrect | Use `true-icon` / `false-icon` instead of `on-icon` / `off-icon` |
| Dense text field | Use `density="compact"` instead of `dense` prop |
| Outlined text field | Use `variant="outlined"` instead of `outlined` prop |