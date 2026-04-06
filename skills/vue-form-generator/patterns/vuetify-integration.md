# Vuetify Integration Patterns

Using VueFormGenerator with Vuetify components in Baseweb projects.

## Overview

VueFormGenerator uses Bootstrap-friendly styling by default. For Vuetify projects, create custom field components that wrap Vuetify inputs.

## Setup

### 1. Install VueFormGenerator

```bash
npm install vue-form-generator
```

### 2. Register Custom Fields

```javascript
// src/fields/index.js
import TextField from './field-v-text-field.vue'
import SelectField from './field-v-select.vue'
import CheckboxField from './field-v-checkbox.vue'
import SwitchField from './field-v-switch.vue'
import DatePickerField from './field-v-date-picker.vue'
import TextareaField from './field-v-textarea.vue'

export default {
  install(Vue) {
    Vue.component('field-v-text-field', TextField)
    Vue.component('field-v-select', SelectField)
    Vue.component('field-v-checkbox', CheckboxField)
    Vue.component('field-v-switch', SwitchField)
    Vue.component('field-v-date-picker', DatePickerField)
    Vue.component('field-v-textarea', TextareaField)
  }
}
```

### 3. Use in Main

```javascript
// main.js
import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import VueFormGenerator from 'vue-form-generator'
import CustomFields from './fields'

Vue.use(Vuetify)
Vue.use(VueFormGenerator)
Vue.use(CustomFields)
```

## Custom Vuetify Fields

### Text Field

```vue
<!-- src/fields/field-v-text-field.vue -->
<template>
  <v-text-field
    v-model="value"
    :label="schema.label"
    :hint="schema.hint"
    :persistent-hint="!!schema.hint"
    :placeholder="schema.placeholder"
    :disabled="disabled"
    :readonly="readonly"
    :required="schema.required"
    :error-messages="errors"
    :type="schema.inputType || 'text'"
    :prepend-icon="schema.prependIcon"
    :append-icon="schema.appendIcon"
    :clearable="schema.clearable"
    :counter="schema.max"
    :outlined="schema.outlined !== false"
    :dense="schema.dense !== false"
    :rules="vuetifyRules"
    @click:append="onAppendClick" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-text-field',
  mixins: [abstractField],
  computed: {
    vuetifyRules() {
      const rules = []

      if (schema.required) {
        rules.push(v => !!v || `${schema.label} is required`)
      }

      if (schema.min) {
        rules.push(v => !v || v.length >= schema.min || `Minimum ${schema.min} characters`)
      }

      if (schema.max) {
        rules.push(v => !v || v.length <= schema.max || `Maximum ${schema.max} characters`)
      }

      return rules
    }
  },
  methods: {
    onAppendClick() {
      if (this.schema.onAppendClick) {
        this.schema.onAppendClick(this.model, this.value)
      }
    }
  }
}
</script>
```

### Select

```vue
<!-- src/fields/field-v-select.vue -->
<template>
  <v-select
    v-model="value"
    :label="schema.label"
    :items="items"
    :disabled="disabled"
    :required="schema.required"
    :error-messages="errors"
    :multiple="schema.multi"
    :chips="schema.multi"
    :deletable-chips="schema.multi"
    :small-chips="schema.smallChips"
    :clearable="schema.clearable"
    :prepend-icon="schema.prependIcon"
    :append-icon="schema.appendIcon"
    :outlined="schema.outlined !== false"
    :dense="schema.dense !== false"
    :menu-props="schema.menuProps"
    item-text="text"
    item-value="value" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-select',
  mixins: [abstractField],
  computed: {
    items() {
      // Get values from schema (can be function or array)
      const values = typeof this.schema.values === 'function'
        ? this.schema.values(this.model)
        : this.schema.values || []

      // Transform to Vuetify format
      if (values.length > 0 && typeof values[0] === 'object') {
        return values.map(v => ({
          text: v[this.schema.selectOptions?.name || 'name'],
          value: v[this.schema.selectOptions?.value || 'value']
        }))
      }

      return values.map(v => ({ text: v, value: v }))
    }
  }
}
</script>
```

### Checkbox

```vue
<!-- src/fields/field-v-checkbox.vue -->
<template>
  <v-checkbox
    v-model="value"
    :label="schema.label"
    :disabled="disabled"
    :error-messages="errors"
    :color="schema.color || 'primary'"
    :hide-details="schema.hideDetails"
    :class="schema.styleClasses" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-checkbox',
  mixins: [abstractField]
}
</script>
```

### Switch

```vue
<!-- src/fields/field-v-switch.vue -->
<template>
  <v-switch
    v-model="value"
    :label="schema.label"
    :disabled="disabled"
    :error-messages="errors"
    :color="schema.color || 'primary'"
    :inset="schema.inset !== false"
    :hide-details="schema.hideDetails"
    :class="schema.styleClasses" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-switch',
  mixins: [abstractField]
}
</script>
```

### Textarea

```vue
<!-- src/fields/field-v-textarea.vue -->
<template>
  <v-textarea
    v-model="value"
    :label="schema.label"
    :hint="schema.hint"
    :persistent-hint="!!schema.hint"
    :placeholder="schema.placeholder"
    :disabled="disabled"
    :readonly="readonly"
    :required="schema.required"
    :error-messages="errors"
    :rows="schema.rows || 4"
    :auto-grow="schema.autoGrow"
    :counter="schema.max"
    :outlined="schema.outlined !== false"
    :dense="schema.dense !== false" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-textarea',
  mixins: [abstractField]
}
</script>
```

### Date Picker

```vue
<!-- src/fields/field-v-date-picker.vue -->
<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    min-width="290px">
    <template v-slot:activator="{ on }">
      <v-text-field
        v-model="formattedDate"
        :label="schema.label"
        :disabled="disabled"
        :error-messages="errors"
        :outlined="schema.outlined !== false"
        :dense="schema.dense !== false"
        prepend-icon="mdi-calendar"
        readonly
        v-on="on" />
    </template>
    <v-date-picker
      v-model="value"
      :min="schema.min"
      :max="schema.max"
      :no-title="schema.noTitle !== false"
      scrollable>
      <v-spacer />
      <v-btn text @click="menu = false">Cancel</v-btn>
      <v-btn text color="primary" @click="menu = false">OK</v-btn>
    </v-date-picker>
  </v-menu>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-date-picker',
  mixins: [abstractField],
  data() {
    return {
      menu: false
    }
  },
  computed: {
    formattedDate() {
      if (!this.value) return ''
      // Format date as needed
      return this.value
    }
  }
}
</script>
```

### Radio Group

```vue
<!-- src/fields/field-v-radio.vue -->
<template>
  <v-radio-group
    v-model="value"
    :label="schema.label"
    :disabled="disabled"
    :error-messages="errors"
    :row="schema.row"
    :column="schema.column"
    :mandatory="schema.mandatory">
    <v-radio
      v-for="option in options"
      :key="option.value"
      :label="option.text"
      :value="option.value"
      :color="schema.color || 'primary'" />
  </v-radio-group>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-radio',
  mixins: [abstractField],
  computed: {
    options() {
      const values = typeof this.schema.values === 'function'
        ? this.schema.values(this.model)
        : this.schema.values || []

      if (values.length > 0 && typeof values[0] === 'object') {
        return values.map(v => ({
          text: v[this.schema.selectOptions?.name || 'name'],
          value: v[this.schema.selectOptions?.value || 'value']
        }))
      }

      return values.map(v => ({ text: v, value: v }))
    }
  }
}
</script>
```

### Autocomplete

```vue
<!-- src/fields/field-v-autocomplete.vue -->
<template>
  <v-autocomplete
    v-model="value"
    :label="schema.label"
    :items="items"
    :disabled="disabled"
    :required="schema.required"
    :error-messages="errors"
    :loading="loading"
    :search-input.sync="search"
    :clearable="schema.clearable"
    :multiple="schema.multi"
    :chips="schema.multi"
    :outlined="schema.outlined !== false"
    :dense="schema.dense !== false"
    :no-filter="schema.noFilter"
    :item-text="schema.selectOptions?.name || 'name'"
    :item-value="schema.selectOptions?.value || 'value'"
    @update:search="onSearch" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-autocomplete',
  mixins: [abstractField],
  data() {
    return {
      search: '',
      loading: false
    }
  },
  computed: {
    items() {
      return typeof this.schema.values === 'function'
        ? this.schema.values(this.model)
        : this.schema.values || []
    }
  },
  methods: {
    async onSearch(query) {
      if (this.schema.onSearch) {
        this.loading = true
        try {
          await this.schema.onSearch(query, this.model)
        } finally {
          this.loading = false
        }
      }
    }
  }
}
</script>
```

## Schema Examples

### Text Input

```javascript
{
  type: 'v-text-field',
  model: 'name',
  label: 'Name',
  placeholder: 'Enter your name',
  required: true,
  prependIcon: 'mdi-account',
  outlined: true,
  dense: true
}
```

### Select

```javascript
{
  type: 'v-select',
  model: 'country',
  label: 'Country',
  values: [
    { code: 'US', name: 'United States' },
    { code: 'CA', name: 'Canada' },
    { code: 'MX', name: 'Mexico' }
  ],
  selectOptions: {
    value: 'code',
    name: 'name'
  },
  outlined: true
}
```

### Dynamic Select

```javascript
{
  type: 'v-select',
  model: 'region',
  label: 'Region',
  values: function(model) {
    const regions = {
      'US': ['California', 'New York', 'Texas'],
      'CA': ['Ontario', 'Quebec', 'British Columbia'],
      'MX': ['Jalisco', 'Mexico City', 'Nuevo Leon']
    }
    return regions[model.country] || []
  },
  visible: function(model) {
    return !!model.country
  }
}
```

### Date Picker

```javascript
{
  type: 'v-date-picker',
  model: 'birthDate',
  label: 'Birth Date',
  min: '1900-01-01',
  max: new Date().toISOString().split('T')[0],
  outlined: true
}
```

### Checkbox

```javascript
{
  type: 'v-checkbox',
  model: 'agreeToTerms',
  label: 'I agree to the terms and conditions',
  color: 'primary'
}
```

## Complete Form Example

```vue
<template>
  <v-card>
    <v-card-title>User Registration</v-card-title>
    <v-card-text>
      <vue-form-generator
        :schema="schema"
        :model="model"
        :options="formOptions"
        @validated="onValidated" />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="reset">Reset</v-btn>
      <v-btn color="primary" :disabled="!isValid" @click="submit">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      model: {
        name: '',
        email: '',
        role: '',
        birthDate: '',
        bio: '',
        notifications: true,
        agreeToTerms: false
      },
      schema: {
        fields: [
          {
            type: 'v-text-field',
            model: 'name',
            label: 'Full Name',
            placeholder: 'John Doe',
            required: true,
            prependIcon: 'mdi-account',
            validator: ['required', 'string']
          },
          {
            type: 'v-text-field',
            model: 'email',
            label: 'Email',
            inputType: 'email',
            placeholder: 'john@example.com',
            required: true,
            prependIcon: 'mdi-email',
            validator: ['required', 'email']
          },
          {
            type: 'v-select',
            model: 'role',
            label: 'Role',
            values: [
              { value: 'admin', text: 'Administrator' },
              { value: 'user', text: 'User' },
              { value: 'guest', text: 'Guest' }
            ],
            outlined: true
          },
          {
            type: 'v-date-picker',
            model: 'birthDate',
            label: 'Birth Date',
            max: new Date().toISOString().split('T')[0]
          },
          {
            type: 'v-textarea',
            model: 'bio',
            label: 'Biography',
            placeholder: 'Tell us about yourself...',
            rows: 3,
            autoGrow: true
          },
          {
            type: 'v-switch',
            model: 'notifications',
            label: 'Email Notifications',
            inset: true
          },
          {
            type: 'v-checkbox',
            model: 'agreeToTerms',
            label: 'I agree to the terms and conditions',
            validator: (value) => value ? [] : ['You must agree to continue']
          }
        ]
      },
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      },
      isValid: false
    }
  },
  methods: {
    onValidated(isValid) {
      this.isValid = isValid
    },
    reset() {
      this.model = {
        name: '',
        email: '',
        role: '',
        birthDate: '',
        bio: '',
        notifications: true,
        agreeToTerms: false
      }
    },
    submit() {
      if (this.isValid) {
        this.$emit('submit', this.model)
      }
    }
  }
}
</script>
```

## See Also

- [VueFormGenerator Custom Fields](https://vue-generators.gitbook.io/vue-generators/fields/custom_fields)
- [Vuetify Forms Skill](/.claude/skills/vuetify/SKILL.md)
- [Baseweb Skill](/.claude/skills/baseweb/SKILL.md)