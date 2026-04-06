# Custom Fields

Creating custom field components for VueFormGenerator.

## Overview

Custom fields extend VueFormGenerator with custom input types. Use the `abstractField` mixin to create reusable field components.

## Basic Custom Field

### Component Structure

```vue
<!-- components/field-custom-input.vue -->
<template>
  <div class="custom-input-wrapper">
    <input
      type="text"
      v-model="value"
      :placeholder="schema.placeholder"
      :disabled="disabled"
      class="form-control" />
  </div>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-custom-input',
  mixins: [abstractField],
  computed: {
    disabled() {
      // Handle disabled state
      if (typeof this.schema.disabled === 'function') {
        return this.schema.disabled(this.model)
      }
      return this.schema.disabled || false
    }
  }
}
</script>

<style scoped>
.custom-input-wrapper {
  /* Custom styles */
}
</style>
```

### Registration

Register globally with naming convention `field-[A-Z][A-z]*`:

```javascript
// main.js
import CustomInput from './components/field-custom-input.vue'

Vue.component('field-custom-input', CustomInput)
```

### Usage in Schema

Use the field name (without 'field' prefix) as the type:

```javascript
{
  type: 'custom-input',
  model: 'customField',
  label: 'Custom Field',
  placeholder: 'Enter value'
}
```

## abstractField Mixin

The mixin provides:

| Property/Method | Description |
|-----------------|-------------|
| `value` | Getter/setter for model value |
| `model` | Reference to the form model |
| `schema` | Reference to field schema |
| `disabled` | Computed disabled state |
| `readonly` | Computed readonly state |
| `visible` | Computed visibility |
| `errors` | Validation errors array |
| `validate()` | Trigger validation |

## Custom Field Examples

### Masked Input

```vue
<!-- components/field-phone.vue -->
<template>
  <input
    type="tel"
    v-model="value"
    :placeholder="schema.placeholder || '(000) 000-0000'"
    :disabled="disabled"
    class="form-control" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-phone',
  mixins: [abstractField],
  watch: {
    value(newVal) {
      // Format as (000) 000-0000
      const cleaned = newVal.replace(/\D/g, '')
      if (cleaned.length <= 10) {
        const formatted = cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3')
        this.value = formatted
      }
    }
  }
}
</script>
```

### Tags Input

```vue
<!-- components/field-tags.vue -->
<template>
  <div class="tags-input">
    <div class="tags-container">
      <span
        v-for="(tag, index) in tags"
        :key="index"
        class="tag badge badge-secondary">
        {{ tag }}
        <button type="button" class="close" @click="removeTag(index)">&times;</button>
      </span>
    </div>
    <input
      type="text"
      v-model="newTag"
      @keydown.enter.prevent="addTag"
      @keydown.tab.prevent="addTag"
      :placeholder="schema.placeholder || 'Add tag...'"
      class="form-control" />
  </div>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-tags',
  mixins: [abstractField],
  data() {
    return {
      newTag: ''
    }
  },
  computed: {
    tags() {
      return this.value || []
    }
  },
  methods: {
    addTag() {
      if (this.newTag.trim()) {
        const tags = [...this.tags, this.newTag.trim()]
        this.value = tags
        this.newTag = ''
      }
    },
    removeTag(index) {
      const tags = [...this.tags]
      tags.splice(index, 1)
      this.value = tags
    }
  }
}
</script>
```

### Rating Input

```vue
<!-- components/field-rating.vue -->
<template>
  <div class="rating-input">
    <span
      v-for="i in maxStars"
      :key="i"
      @click="setRating(i)"
      :class="['star', { active: i <= rating }]">
      ★
    </span>
    <span class="rating-value">{{ rating }} / {{ maxStars }}</span>
  </div>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-rating',
  mixins: [abstractField],
  computed: {
    rating() {
      return this.value || 0
    },
    maxStars() {
      return this.schema.max || 5
    }
  },
  methods: {
    setRating(rating) {
      this.value = rating
    }
  }
}
</script>

<style scoped>
.rating-input .star {
  font-size: 24px;
  cursor: pointer;
  color: #ccc;
}
.rating-input .star.active {
  color: gold;
}
</style>
```

### Color Picker

```vue
<!-- components/field-color.vue -->
<template>
  <div class="color-picker">
    <input
      type="color"
      v-model="value"
      :disabled="disabled"
      class="form-control" />
    <span class="color-preview" :style="{ backgroundColor: value }"></span>
  </div>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-color',
  mixins: [abstractField]
}
</script>

<style scoped>
.color-picker {
  display: flex;
  align-items: center;
  gap: 10px;
}
.color-preview {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
</style>
```

### JSON Editor

```vue
<!-- components/field-json.vue -->
<template>
  <div class="json-editor">
    <textarea
      v-model="jsonText"
      :placeholder="schema.placeholder"
      :disabled="disabled"
      rows="10"
      class="form-control"
      :class="{ 'is-invalid': error }" />
    <div v-if="error" class="invalid-feedback">{{ error }}</div>
  </div>
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-json',
  mixins: [abstractField],
  data() {
    return {
      jsonText: '',
      error: null
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(newVal) {
        try {
          this.jsonText = JSON.stringify(newVal, null, 2)
          this.error = null
        } catch (e) {
          this.jsonText = ''
        }
      }
    },
    jsonText(newVal) {
      try {
        const parsed = JSON.parse(newVal)
        this.value = parsed
        this.error = null
      } catch (e) {
        this.error = 'Invalid JSON'
      }
    }
  }
}
</script>
```

## Vuetify Integration

### Creating Vuetify Fields

```vue
<!-- components/field-v-text-field.vue -->
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
    outlined
    dense />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-text-field',
  mixins: [abstractField]
}
</script>
```

### Vuetify Select

```vue
<!-- components/field-v-select.vue -->
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
    :clearable="schema.clearable"
    outlined
    dense />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-select',
  mixins: [abstractField],
  computed: {
    items() {
      const values = typeof this.schema.values === 'function'
        ? this.schema.values(this.model)
        : this.schema.values

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

### Vuetify Checkbox

```vue
<!-- components/field-v-checkbox.vue -->
<template>
  <v-checkbox
    v-model="value"
    :label="schema.label"
    :disabled="disabled"
    :error-messages="errors"
    :color="schema.color || 'primary'" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-checkbox',
  mixins: [abstractField]
}
</script>
```

### Vuetify Switch

```vue
<!-- components/field-v-switch.vue -->
<template>
  <v-switch
    v-model="value"
    :label="schema.label"
    :disabled="disabled"
    :error-messages="errors"
    :color="schema.color || 'primary'"
    :inset="schema.inset !== false" />
</template>

<script>
import { abstractField } from 'vue-form-generator'

export default {
  name: 'field-v-switch',
  mixins: [abstractField]
}
</script>
```

### Vuetify Date Picker

```vue
<!-- components/field-v-date-picker.vue -->
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
        prepend-icon="mdi-calendar"
        readonly
        v-on="on" />
    </template>
    <v-date-picker
      v-model="value"
      :min="schema.min"
      :max="schema.max"
      no-title
      scrollable />
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
      return this.value  // Format as needed
    }
  }
}
</script>
```

## Publishing Custom Fields

### Package Structure

For community packages, use `vfg-field-*` naming:

```
vfg-field-calendar/
├── package.json
├── src/
│   ├── CalendarField.vue
│   └── index.js
└── README.md
```

### package.json

```json
{
  "name": "vfg-field-calendar",
  "version": "1.0.0",
  "main": "dist/vfg-field-calendar.umd.js",
  "keywords": ["vue", "vue-form-generator", "field", "calendar"],
  "peerDependencies": {
    "vue": "^2.6.0",
    "vue-form-generator": "^2.3.0"
  }
}
```

### Usage

```javascript
import CalendarField from 'vfg-field-calendar'

Vue.component('field-calendar', CalendarField)
```

## See Also

- [Custom Fields Documentation](https://vue-generators.gitbook.io/vue-generators/fields/custom_fields)
- [abstractField Source](https://github.com/vue-generators/vue-form-generator/blob/master/src/fields/abstractField.js)