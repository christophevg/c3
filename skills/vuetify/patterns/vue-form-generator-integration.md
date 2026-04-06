# VueFormGenerator Integration

Using VueFormGenerator with Vuetify components for complex forms.

## When to Use VueFormGenerator vs Vuetify Forms

| Use VueFormGenerator | Use Vuetify Forms |
|---------------------|-------------------|
| Complex, multi-step forms | Simple forms (1-5 fields) |
| Dynamic/conditional fields | Quick CRUD forms |
| API-driven form schemas | Static forms |
| Forms that change by user role | Prototypes |
| Reusable form patterns | One-off forms |
| Multi-object editing | Standard forms |

**Preference**: For larger forms in Baseweb projects, prefer VueFormGenerator's schema approach for maintainability.

## Integration Approach

VueFormGenerator doesn't include Vuetify components by default. Create custom field components that wrap Vuetify inputs.

### Custom Field Pattern

```vue
<!-- field-v-text-field.vue -->
<template>
  <v-text-field
    v-model="value"
    :label="schema.label"
    :hint="schema.hint"
    :disabled="disabled"
    :error-messages="errors"
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

### Registration

```javascript
import TextField from './field-v-text-field.vue'
Vue.component('field-v-text-field', TextField)
```

### Schema Usage

```javascript
{
  type: 'v-text-field',
  model: 'name',
  label: 'Name',
  placeholder: 'Enter name',
  required: true
}
```

## Common Vuetify Field Types

| Vuetify Component | VueFormGenerator Type |
|-------------------|----------------------|
| `v-text-field` | `v-text-field` |
| `v-textarea` | `v-textarea` |
| `v-select` | `v-select` |
| `v-autocomplete` | `v-autocomplete` |
| `v-checkbox` | `v-checkbox` |
| `v-switch` | `v-switch` |
| `v-radio-group` | `v-radio` |
| `v-date-picker` | `v-date-picker` |

## Complete Integration

See the VueFormGenerator skill for complete patterns:
- `patterns/vuetify-integration.md` - Full integration guide
- `patterns/custom-fields.md` - Creating custom fields
- `patterns/multi-step.md` - Multi-step wizard forms

## Quick Reference

### Text Input

```javascript
{
  type: 'v-text-field',
  model: 'name',
  label: 'Name',
  prependIcon: 'mdi-account',
  outlined: true
}
```

### Select

```javascript
{
  type: 'v-select',
  model: 'role',
  label: 'Role',
  values: [
    { value: 'admin', text: 'Administrator' },
    { value: 'user', text: 'User' }
  ]
}
```

### Checkbox

```javascript
{
  type: 'v-checkbox',
  model: 'agreeToTerms',
  label: 'I agree to the terms',
  color: 'primary'
}
```

### Date Picker

```javascript
{
  type: 'v-date-picker',
  model: 'birthDate',
  label: 'Birth Date',
  max: new Date().toISOString().split('T')[0]
}
```

## See Also

- [VueFormGenerator Skill](/.claude/skills/vue-form-generator/SKILL.md) - Full documentation
- [Forms Pattern](./forms.md) - Native Vuetify forms