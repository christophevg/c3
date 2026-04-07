# Vuetify 1.5 Form Patterns

## v-form

### Basic Form with Validation

```vue
<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <v-text-field
      v-model="name"
      :rules="nameRules"
      label="Name"
      required
    />
    <v-text-field
      v-model="email"
      :rules="emailRules"
      label="Email"
      required
    />
    <v-btn :disabled="!valid" @click="submit">Submit</v-btn>
    <v-btn @click="reset">Reset</v-btn>
  </v-form>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length >= 3 || 'Name must be at least 3 characters'
      ],
      email: '',
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+/.test(v) || 'Email must be valid'
      ]
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        // Submit form
      }
    },
    reset() {
      this.$refs.form.reset()
    }
  }
}
</script>
```

### v-form Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `lazy-validation` | boolean | false | Only validate when user interacts |
| `value` | boolean | false | Form validity state |

### v-form Methods

| Method | Description |
|--------|-------------|
| `validate()` | Validate all inputs, returns boolean |
| `reset()` | Clear all inputs and reset validation |
| `resetValidation()` | Reset validation state without clearing values |

## v-text-field

### Basic Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `append-icon` | string | - | Icon after input |
| `append-outer-icon` | string | - | Icon outside input |
| `box` | boolean | false | Box style input |
| `clearable` | boolean | false | Show clear button |
| `color` | string | 'primary' | Input color |
| `counter` | boolean/number | - | Character counter |
| `disabled` | boolean | false | Disable input |
| `error` | boolean | false | Manual error state |
| `error-messages` | string/array | [] | Error messages |
| `flat` | boolean | false | Remove elevation (with solo) |
| `full-width` | boolean | false | Full width |
| `hint` | string | - | Hint text below input |
| `label` | string | - | Input label |
| `loading` | boolean | false | Show loading |
| `mask` | string/object | - | Input mask |
| `outline` | boolean | false | Outlined style |
| `persistent-hint` | boolean | false | Always show hint |
| `placeholder` | string | - | Placeholder text |
| `prepend-icon` | string | - | Icon before input |
| `prepend-inner-icon` | string | - | Icon inside, before text |
| `readonly` | boolean | false | Read-only state |
| `reverse` | boolean | false | Reverse input direction |
| `rules` | array | [] | Validation rules |
| `solo` | boolean | false | Solo style |
| `solo-inverted` | boolean | false | Inverted solo style |
| `type` | string | 'text' | Input type |
| `validate-on-blur` | boolean | false | Validate on blur only |

### Input Styles

```vue
<!-- Default -->
<v-text-field label="Default" />

<!-- Box -->
<v-text-field label="Box" box />

<!-- Outline -->
<v-text-field label="Outline" outline />

<!-- Solo -->
<v-text-field label="Solo" solo />

<!-- Solo Inverted -->
<v-text-field label="Solo Inverted" solo-inverted />
```

### With Icons

```vue
<!-- Prepend Icon -->
<v-text-field
  v-model="search"
  prepend-icon="search"
  label="Search"
/>

<!-- Append Icon -->
<v-text-field
  v-model="password"
  :append-icon="showPassword ? 'visibility' : 'visibility_off'"
  :type="showPassword ? 'text' : 'password'"
  label="Password"
  @click:append="showPassword = !showPassword"
/>

<!-- Clearable -->
<v-text-field
  v-model="value"
  clearable
  label="Clearable"
/>
```

### Character Counter

```vue
<v-text-field
  v-model="title"
  :counter="50"
  :rules="[v => v.length <= 50 || 'Max 50 characters']"
  label="Title"
/>
```

### Input Masks

```vue
<v-text-field
  v-model="phone"
  mask="phone"
  label="Phone"
/>
<!-- Outputs: (###) ### - #### -->

<v-text-field
  v-model="creditCard"
  mask="credit-card"
  label="Credit Card"
/>
<!-- Outputs: #### - #### - #### - #### -->

<v-text-field
  v-model="custom"
  :mask="'###-##-####'"
  label="Custom Mask"
/>
```

### Mask Characters

| Mask | Description |
|------|-------------|
| `#` | Any digit |
| `A` | Any capital letter |
| `a` | Any lowercase letter |
| `N` | Any capital alphanumeric |
| `n` | Any lowercase alphanumeric |
| `X` | Any special character or space |

## v-textarea

```vue
<v-textarea
  v-model="description"
  label="Description"
  :counter="500"
  :rules="[v => v.length <= 500 || 'Max 500 characters']"
  auto-grow
/>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `auto-grow` | boolean | false | Auto-grow height |
| `no-resize` | boolean | false | Disable resize |
| `outline` | boolean | false | Outlined style |
| `row-height` | number/string | 24 | Row height in pixels |
| `rows` | number/string | 5 | Default number of rows |

## v-select

### Basic Select

```vue
<v-select
  v-model="selected"
  :items="items"
  label="Select Item"
/>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `append-icon` | string | '$vuetify.icons.dropdown' | Append icon |
| `attach` | any | false | Attach to element |
| `autofocus` | boolean | false | Auto focus |
| `box` | boolean | false | Box style |
| `chips` | boolean | false | Display as chips |
| `clearable` | boolean | false | Allow clear |
| `deletable-chips` | boolean | false | Allow deleting chips |
| `dense` | boolean | false | Dense mode |
| `disabled` | boolean | false | Disabled state |
| `error-messages` | array | [] | Error messages |
| `hide-details` | boolean | false | Hide details |
| `hint` | string | - | Hint text |
| `items` | array | [] | Select items |
| `item-avatar` | string/object | 'avatar' | Avatar property |
| `item-disabled` | string/object | 'disabled' | Disabled property |
| `item-text` | string/object | 'text' | Text property |
| `item-value` | string/object | 'value' | Value property |
| `label` | string | - | Label text |
| `multiple` | boolean | false | Allow multiple |
| `menu-props` | object | - | Menu props |
| `outline` | boolean | false | Outlined style |
| `persistent-hint` | boolean | false | Always show hint |
| `prepend-icon` | string | - | Prepend icon |
| `return-object` | boolean | false | Return object |
| `rules` | array | [] | Validation rules |
| `single-line` | boolean | false | Single line mode |
| `small-chips` | boolean | false | Small chips |
| `solo` | boolean | false | Solo style |

### Object Items

```vue
<v-select
  v-model="selected"
  :items="users"
  item-text="name"
  item-value="id"
  label="Select User"
/>
<!-- users: [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }] -->
```

### Multiple Selection

```vue
<v-select
  v-model="selected"
  :items="items"
  multiple
  chips
  deletable-chips
  label="Select Multiple"
/>
```

### Slots

```vue
<v-select :items="items" label="Custom">
  <template slot="item" slot-scope="{ item }">
    <v-list-tile-avatar>
      <v-icon>{{ item.icon }}</v-icon>
    </v-list-tile-avatar>
    <v-list-tile-content>
      <v-list-tile-title>{{ item.text }}</v-list-tile-title>
      <v-list-tile-sub-title>{{ item.description }}</v-list-tile-sub-title>
    </v-list-tile-content>
  </template>
</v-select>
```

## v-autocomplete

```vue
<v-autocomplete
  v-model="selected"
  :items="items"
  :search-input.sync="search"
  label="Autocomplete"
/>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `allow-overflow` | boolean | true | Allow overflow |
| `auto-select-first` | boolean | false | Auto-select first |
| `filter` | function | - | Custom filter |
| `hide-no-data` | boolean | false | Hide no data |
| `hide-selected` | boolean | false | Hide selected |
| `no-data-text` | string | - | No data text |
| `search-input` | string | - | Search input value |

### Async Autocomplete

```vue
<template>
  <v-autocomplete
    v-model="selected"
    :items="items"
    :loading="loading"
    :search-input.sync="search"
    cache-items
    flat
    hide-no-data
    label="Search Users"
  />
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      items: [],
      search: null,
      selected: null
    }
  },
  watch: {
    search(val) {
      if (!val) return
      this.loading = true
      this.fetchUsers(val)
    }
  },
  methods: {
    async fetchUsers(query) {
      const response = await fetch(`/api/users?q=${query}`)
      this.items = await response.json()
      this.loading = false
    }
  }
}
</script>
```

## v-combobox

Select with custom entry (user can type custom values):

```vue
<v-combobox
  v-model="selected"
  :items="items"
  label="Select or Create"
  multiple
  chips
/>
```

## Selection Controls

### v-checkbox

```vue
<v-checkbox
  v-model="checked"
  label="Accept terms"
  :rules="[v => !!v || 'You must accept!']"
/>
```

### v-switch

```vue
<v-switch
  v-model="enabled"
  label="Enable feature"
/>
```

### v-radio-group

```vue
<v-radio-group v-model="selected" row>
  <v-radio label="Option A" value="a" />
  <v-radio label="Option B" value="b" />
  <v-radio label="Option C" value="c" />
</v-radio-group>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Selection color |
| `disabled` | boolean | Disabled state |
| `false-value` | any | Value when unchecked (checkbox) |
| `indeterminate` | boolean | Indeterminate state (checkbox) |
| `input-value` | any | Input value |
| `label` | string | Label text |
| `true-value` | any | Value when checked (checkbox) |
| `value` | any | Value (radio) |

### Radio Group Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `column` | boolean | true | Vertical layout |
| `row` | boolean | false | Horizontal layout |
| `mandatory` | boolean | true | Require selection |

## Validation Patterns

### Rule Functions

```javascript
// Required
[v => !!v || 'This field is required']

// Min length
[v => v.length >= 8 || 'Minimum 8 characters']

// Max length
[v => v.length <= 50 || 'Maximum 50 characters']

// Email format
[v => /.+@.+\..+/.test(v) || 'Invalid email']

// Number range
[v => v >= 0 && v <= 100 || 'Must be between 0 and 100']

// Custom validation
[v => this.customValidator(v) || 'Custom error message']

// Async validation (use with caution)
async (v) => {
  const valid = await this.checkAsync(v)
  return valid || 'Already taken'
}
```

### Third-Party Integration

#### VeeValidate

```vue
<template>
  <v-text-field
    v-model="email"
    v-validate="'required|email'"
    :error-messages="errors.collect('email')"
    data-vv-name="email"
    label="Email"
  />
</template>
```

#### Vuelidate

```vue
<template>
  <v-text-field
    v-model="email"
    :error-messages="emailErrors"
    @blur="$v.email.$touch()"
    label="Email"
  />
</template>

<script>
import { required, email } from 'vuelidate/lib/validators'

export default {
  validations: {
    email: { required, email }
  },
  computed: {
    emailErrors() {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('Must be valid email')
      !this.$v.email.required && errors.push('Email is required')
      return errors
    }
  }
}
</script>
```

## Complete Form Example

```vue
<template>
  <v-form ref="form" v-model="valid">
    <v-text-field
      v-model="user.name"
      :rules="nameRules"
      :counter="50"
      label="Full Name"
      prepend-icon="person"
      required
    />

    <v-text-field
      v-model="user.email"
      :rules="emailRules"
      label="Email"
      prepend-icon="email"
      required
    />

    <v-text-field
      v-model="user.password"
      :append-icon="showPassword ? 'visibility' : 'visibility_off'"
      :rules="passwordRules"
      :type="showPassword ? 'text' : 'password'"
      label="Password"
      prepend-icon="lock"
      counter
      @click:append="showPassword = !showPassword"
    />

    <v-select
      v-model="user.role"
      :items="roles"
      :rules="[v => !!v || 'Role is required']"
      label="Role"
      prepend-icon="group"
    />

    <v-checkbox
      v-model="user.terms"
      :rules="[v => !!v || 'You must accept']"
      label="Accept Terms of Service"
    />

    <v-btn :disabled="!valid" color="primary" @click="submit">
      Submit
    </v-btn>
    <v-btn @click="reset">Reset</v-btn>
  </v-form>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      showPassword: false,
      user: {
        name: '',
        email: '',
        password: '',
        role: null,
        terms: false
      },
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 50 || 'Name must be less than 50 characters'
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+/.test(v) || 'Email must be valid'
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => v.length >= 8 || 'Password must be at least 8 characters'
      ],
      roles: ['Admin', 'User', 'Guest']
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit('submit', this.user)
      }
    },
    reset() {
      this.$refs.form.reset()
    }
  }
}
</script>
```