---
name: vue-form-generator
description: Use this skill when creating complex, schema-based forms in Vue.js applications. Preferred for larger forms, dynamic forms, and API-driven form schemas.
triggers:
  - when creating complex forms in Vue/Baseweb
  - when asked about schema-based forms
  - when implementing multi-step forms
  - when creating dynamic or API-driven forms
  - when working with VueFormGenerator library
---

# VueFormGenerator Skill

Schema-based form generator for Vue.js 2 applications. Creates reactive forms from JSON schema definitions - ideal for complex, dynamic, or API-driven forms.

## Overview

This skill provides:

| Capability | Description |
|------------|-------------|
| Schema Definition | JSON-based form schemas for reusable forms |
| Field Types | 21+ built-in field types |
| Validation | 12 built-in validators + custom validation |
| Custom Fields | Create reusable field components |
| Dynamic Forms | Conditional visibility, computed values |
| Multi-step Forms | Wizard-style form patterns |

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

## Installation

```bash
npm install vue-form-generator
```

```javascript
import Vue from 'vue'
import VueFormGenerator from 'vue-form-generator'
import 'vue-form-generator/dist/vfg.css'

Vue.use(VueFormGenerator)
```

### Core vs Full Bundle

```javascript
// Core (41kb) - Essential fields only
import VueFormGenerator from 'vue-form-generator/dist/vfg-core.js'
import 'vue-form-generator/dist/vfg-core.css'

// Full (50kb) - All field types
import VueFormGenerator from 'vue-form-generator'
import 'vue-form-generator/dist/vfg.css'
```

## Basic Usage

```vue
<template>
  <vue-form-generator
    :schema="schema"
    :model="model"
    :options="formOptions"
    @validated="onValidated">
  </vue-form-generator>
</template>

<script>
export default {
  data() {
    return {
      model: {
        name: '',
        email: '',
        status: 'active'
      },
      schema: {
        fields: [
          {
            type: 'input',
            inputType: 'text',
            label: 'Name',
            model: 'name',
            required: true,
            validator: 'string'
          },
          {
            type: 'input',
            inputType: 'email',
            label: 'Email',
            model: 'email',
            validator: 'email'
          },
          {
            type: 'select',
            label: 'Status',
            model: 'status',
            values: ['active', 'inactive']
          }
        ]
      },
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      }
    }
  },
  methods: {
    onValidated(isValid, errors) {
      console.log('Valid:', isValid, 'Errors:', errors)
    }
  }
}
</script>
```

## Schema Structure

### Fields

```javascript
schema: {
  fields: [
    {
      type: 'input',           // Field type
      inputType: 'text',       // Input type (for 'input' fields)
      label: 'Field Label',    // Display label
      model: 'fieldName',      // Model property (supports dot notation)
      placeholder: 'Enter...', // Placeholder text
      required: true,          // Required field
      readonly: false,         // Read-only
      disabled: false,         // Disabled
      visible: true,           // Show/hide (can be function)
      hint: 'Help text',       // Hint text
      help: 'Tooltip',         // Tooltip
      validator: 'string',     // Validator(s)
      styleClasses: 'col-6'    // CSS classes
    }
  ]
}
```

### Groups

```javascript
schema: {
  groups: [
    {
      legend: 'Personal Info',
      fields: [
        { type: 'input', model: 'firstName', label: 'First Name' },
        { type: 'input', model: 'lastName', label: 'Last Name' }
      ]
    },
    {
      legend: 'Contact',
      fields: [
        { type: 'input', inputType: 'email', model: 'email', label: 'Email' },
        { type: 'input', inputType: 'tel', model: 'phone', label: 'Phone' }
      ]
    }
  ]
}
```

### Nested Models

```javascript
model: {
  user: {
    profile: {
      name: 'John',
      address: {
        city: 'New York',
        country: 'USA'
      }
    }
  }
}

// Schema with dot notation
{
  type: 'input',
  model: 'user.profile.name',      // Deep nesting
  label: 'Name'
},
{
  type: 'input',
  model: 'user.profile.address.city',  // Very deep
  label: 'City'
}
```

## Field Types

### Core Fields (Available in Core Bundle)

| Type | Description | Key Properties |
|------|-------------|----------------|
| `input` | Text input | `inputType`: text, password, email, number, etc. |
| `textArea` | Multi-line text | `rows`, `placeholder` |
| `select` | Dropdown | `values`: array or function |
| `checkbox` | Boolean checkbox | `default` |
| `checklist` | Multiple checkboxes | `values`: array of options |
| `radios` | Radio button group | `values`: array of options |
| `label` | Static text | For timestamps, calculated values |
| `submit` | Submit button | `label`: button text |

### Optional Fields (Full Bundle)

| Type | Description | Dependencies |
|------|-------------|--------------|
| `cleave` | Formatted input | Cleave.js |
| `dateTimePicker` | Date/time picker | bootstrap-datetimepicker |
| `pikaday` | Date picker | Pikaday |
| `image` | Image upload | None |
| `switch` | Toggle switch | None |
| `slider` | Range slider | ion.rangeSlider |
| `noUiSlider` | Range slider | noUiSlider |
| `spectrum` | Color picker | Spectrum |
| `vueMultiSelect` | Multi-select | vueMultiSelect |
| `googleAddress` | Address autocomplete | Google Maps API |

## Validation

### Built-in Validators

| Validator | Purpose | Parameters |
|-----------|---------|------------|
| `required` | Field must have value | None |
| `string` | String value | `min`, `max` length |
| `number` | Numeric value | `min`, `max` |
| `integer` | Integer value | None |
| `double` | Decimal number | None |
| `email` | Email format | None |
| `url` | HTTP URL | None |
| `date` | Valid Date | `min`, `max` dates |
| `regexp` | Regex match | `schema.pattern` |
| `creditCard` | Credit card | None |
| `alpha` | Letters only | None |
| `alphaNumeric` | Alphanumeric | None |

### Using Validators

```javascript
// Single validator (string shorthand)
{ type: 'input', model: 'name', validator: 'string' }

// Single validator (function)
{ type: 'input', model: 'name', validator: validators.string }

// Multiple validators (all must pass)
{ type: 'input', model: 'age', validator: ['integer', 'required'] }

// With parameters
{ type: 'input', model: 'password', min: 6, validator: 'string' }
```

### Custom Validators

```javascript
// Synchronous validator
const zipcodeValidator = (value) => {
  const re = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
  if (!re.test(value)) {
    return ['Invalid Zip Code'];
  }
  return [];
};

// Asynchronous validator
const uniqueEmailValidator = (value) => {
  return new Promise((resolve) => {
    HTTP.get(`/checkEmail?value=${value}`)
      .then(() => resolve([]))
      .catch(() => resolve(['Email already exists']));
  });
};

// Register globally
Vue.use(VueFormGenerator, {
  validators: {
    zipcode: zipcodeValidator,
    uniqueEmail: uniqueEmailValidator
  }
});

// Usage
{ type: 'input', model: 'zip', validator: 'zipcode' }
```

### Debounced Validation

```javascript
// Per-field
{ type: 'input', model: 'name', validator: 'string', validateDebounceTime: 500 }

// Global
formOptions: {
  validateDebounceTime: 300
}
```

## Dynamic Fields

### Conditional Visibility

```javascript
{
  type: 'input',
  model: 'company',
  label: 'Company Name',
  visible: function(model) {
    return model && model.type === 'business';
  }
}
```

### Conditional Options

```javascript
{
  type: 'select',
  model: 'region',
  values: function(model) {
    switch(model.country) {
      case 'US': return ['California', 'New York', 'Texas'];
      case 'CA': return ['Ontario', 'Quebec', 'British Columbia'];
      default: return [];
    }
  },
  visible: function(model) {
    return !!model.country;
  }
}
```

### Disabled State

```javascript
{
  type: 'input',
  model: 'readonlyField',
  disabled: function(model) {
    return model.status === 'locked';
  }
}
```

### Data Transformation

```javascript
{
  model: 'price',
  get: (model) => model.price / 100,        // Cents to dollars
  set: (model, value) => model.price = value * 100  // Dollars to cents
}
```

## Form Options

```javascript
formOptions: {
  validateAfterLoad: true,      // Validate on mount
  validateAfterChanged: true,   // Real-time validation
  validateAsync: true,          // Enable async validators
  validateDebounceTime: 300,    // Debounce validation
  fieldIdPrefix: 'user-form-'   // Prefix for field IDs
}
```

## Events

### Component Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `validated` | `(isValid, errors, component)` | After validation |
| `model-updated` | `(newValue, propertyName)` | User input change |

```vue
<vue-form-generator
  :schema="schema"
  :model="model"
  @validated="onValidated"
  @model-updated="onModelUpdated">
</vue-form-generator>
```

### Field Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `onChanged` | `(model, newVal, oldVal, field)` | Value changed |
| `onValidated` | `(model, errors, field)` | Field validated |

```javascript
{
  type: 'select',
  model: 'country',
  values: countries,
  onChanged: (model, newVal, oldVal, field) => {
    model.region = null;  // Reset dependent field
  }
}
```

## Pattern Files

This skill includes detailed patterns:

- `patterns/field-types.md` - Complete field type reference
- `patterns/validation.md` - Validation patterns and custom validators
- `patterns/custom-fields.md` - Creating custom field components
- `patterns/multi-step.md` - Wizard-style forms
- `patterns/vuetify-integration.md` - Using Vuetify components with VFG

## Integration with Baseweb

```javascript
// pages/form.js
const FormPage = {
  navigation: {
    section: null,
    icon: 'form',
    text: 'Form',
    path: '/form',
    index: 10
  },
  template: `
<Page>
  <v-container>
    <v-card>
      <v-card-title>Dynamic Form</v-card-title>
      <v-card-text>
        <vue-form-generator
          :schema="schema"
          :model="model"
          :options="formOptions"
          @validated="onValidated">
        </vue-form-generator>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="reset">Reset</v-btn>
        <v-btn color="primary" :disabled="!isValid" @click="submit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</Page>
  `,
  data() {
    return {
      model: {},
      schema: { fields: [] },
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      },
      isValid: false
    };
  },
  mounted() {
    this.$vuetify.goTo(0);
    this.loadSchema();
  },
  methods: {
    loadSchema() {
      $.ajax({
        url: '/api/form-schema',
        success: (response) => {
          this.schema = response.schema;
          this.model = response.model || {};
        }
      });
    },
    onValidated(isValid, errors) {
      this.isValid = isValid;
    },
    reset() {
      this.model = {};
    },
    submit() {
      $.ajax({
        url: '/api/submit',
        method: 'POST',
        data: JSON.stringify(this.model),
        success: (response) => {
          this.$notify({
            group: 'notifications',
            title: 'Success',
            text: 'Form submitted successfully',
            type: 'success'
          });
        }
      });
    }
  }
};

Navigation.add(FormPage);
```

## Agent Collaboration

This skill collaborates with:

| Agent | Collaboration Point |
|-------|---------------------|
| UI/UX Designer | Form schema design, field layouts |
| Python Developer | API integration for schema loading |
| Functional Analyst | Form requirements, validation rules |

## See Also

- [VueFormGenerator Documentation](https://vue-generators.gitbook.io/vue-generators/)
- [GitHub Repository](https://github.com/vue-generators/vue-form-generator)
- [Vuetify Skill](/.claude/skills/vuetify/SKILL.md) - For Vuetify integration