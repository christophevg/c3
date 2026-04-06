# Validation Patterns

Comprehensive validation patterns for VueFormGenerator.

## Built-in Validators

### Available Validators

| Validator | Purpose | Example |
|-----------|---------|---------|
| `required` | Field must have value | `validator: 'required'` |
| `string` | String value | `validator: 'string'` |
| `number` | Numeric value | `validator: 'number'` |
| `integer` | Integer value | `validator: 'integer'` |
| `double` | Decimal number | `validator: 'double'` |
| `email` | Email format | `validator: 'email'` |
| `url` | HTTP URL | `validator: 'url'` |
| `date` | Valid Date | `validator: 'date'` |
| `regexp` | Regex match | `validator: 'regexp'` |
| `creditCard` | Credit card | `validator: 'creditCard'` |
| `alpha` | Letters only | `validator: 'alpha'` |
| `alphaNumeric` | Alphanumeric | `validator: 'alphaNumeric'` |

### Using Validators

```javascript
// Single validator (string shorthand)
{ type: 'input', model: 'email', validator: 'email' }

// Single validator (function)
{ type: 'input', model: 'email', validator: validators.email }

// Multiple validators (all must pass)
{ type: 'input', model: 'age', validator: ['required', 'integer'] }

// With parameters
{
  type: 'input',
  model: 'password',
  min: 8,
  max: 64,
  validator: 'string'  // Uses min/max from schema
}
```

### Validator Parameters

```javascript
// String length
{
  type: 'input',
  model: 'name',
  min: 2,
  max: 50,
  validator: 'string'
}

// Number range
{
  type: 'input',
  inputType: 'number',
  model: 'age',
  min: 0,
  max: 150,
  validator: 'number'
}

// Date range
{
  type: 'dateTimePicker',
  model: 'eventDate',
  min: new Date(),
  max: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
  validator: 'date'
}

// Regex pattern
{
  type: 'input',
  model: 'phone',
  pattern: /^\+?[\d\s-]+$/,
  validator: 'regexp'
}
```

## Custom Validators

### Synchronous Validator

```javascript
const zipcodeValidator = (value) => {
  const re = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
  if (!re.test(value)) {
    return ['Invalid ZIP code format (e.g., 12345 or 12345-6789)'];
  }
  return [];
};

// Usage
{
  type: 'input',
  model: 'zipCode',
  label: 'ZIP Code',
  validator: zipcodeValidator
}
```

### Asynchronous Validator

```javascript
const uniqueEmailValidator = (value, field, model) => {
  return new Promise((resolve) => {
    // Skip if empty (let 'required' handle it)
    if (!value) {
      resolve([]);
      return;
    }

    // Check uniqueness via API
    fetch(`/api/check-email?email=${encodeURIComponent(value)}`)
      .then(response => response.json())
      .then(data => {
        if (data.exists) {
          resolve(['This email is already registered']);
        } else {
          resolve([]);
        }
      })
      .catch(() => {
        resolve([]);  // Don't block on network error
      });
  });
};

// Usage
{
  type: 'input',
  inputType: 'email',
  model: 'email',
  validator: uniqueEmailValidator
}
```

### Complex Validator

```javascript
const passwordValidator = (value) => {
  const errors = [];

  if (!value) {
    return ['Password is required'];
  }

  if (value.length < 8) {
    errors.push('Password must be at least 8 characters');
  }

  if (!/[A-Z]/.test(value)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  if (!/[a-z]/.test(value)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  if (!/[0-9]/.test(value)) {
    errors.push('Password must contain at least one number');
  }

  if (!/[!@#$%^&*]/.test(value)) {
    errors.push('Password must contain at least one special character (!@#$%^&*)');
  }

  return errors;
};

// Usage
{
  type: 'input',
  inputType: 'password',
  model: 'password',
  label: 'Password',
  validator: passwordValidator
}
```

### Password Confirmation Validator

```javascript
const confirmPasswordValidator = (value, field, model) => {
  if (value !== model.password) {
    return ['Passwords do not match'];
  }
  return [];
};

// Usage
{
  type: 'input',
  inputType: 'password',
  model: 'confirmPassword',
  label: 'Confirm Password',
  validator: confirmPasswordValidator
}
```

## Global Validators

Register validators globally for reuse:

```javascript
// main.js
Vue.use(VueFormGenerator, {
  validators: {
    zipcode: (value) => {
      const re = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
      return re.test(value) ? [] : ['Invalid ZIP code'];
    },
    phone: (value) => {
      const re = /^\+?[\d\s-]+$/;
      return re.test(value) ? [] : ['Invalid phone number'];
    },
    strongPassword: (value) => {
      if (value.length < 8) return ['Minimum 8 characters'];
      if (!/[A-Z]/.test(value)) return ['At least one uppercase letter'];
      if (!/[a-z]/.test(value)) return ['At least one lowercase letter'];
      if (!/[0-9]/.test(value)) return ['At least one number'];
      return [];
    }
  }
});

// Usage in schema
{ type: 'input', model: 'zip', validator: 'zipcode' }
{ type: 'input', model: 'phone', validator: 'phone' }
{ type: 'input', model: 'password', validator: 'strongPassword' }
```

## Custom Error Messages

### Locale Customization

```javascript
{
  type: 'input',
  inputType: 'password',
  model: 'password',
  min: 8,
  validator: validators.string.locale({
    fieldIsRequired: "Password is required!",
    textTooSmall: "Password must be at least {1} characters"
  })
}
```

### Dynamic Error Messages

```javascript
{
  type: 'input',
  model: 'username',
  validator: (value, field, model) => {
    if (!value) return ['Username is required'];
    if (value.length < 3) return [`Username must be at least 3 characters (currently ${value.length})`];
    if (!/^[a-zA-Z0-9_]+$/.test(value)) return ['Username can only contain letters, numbers, and underscores'];
    return [];
  }
}
```

## Validation Options

### Form-Level Options

```javascript
formOptions: {
  validateAfterLoad: true,      // Validate on mount
  validateAfterChanged: true,   // Validate on every change
  validateAsync: true,          // Enable async validators
  validateDebounceTime: 300     // Debounce validation (ms)
}
```

### Field-Level Debounce

```javascript
{
  type: 'input',
  model: 'username',
  validator: uniqueUsernameValidator,
  validateDebounceTime: 500  // Wait 500ms before validating
}
```

## Conditional Validation

### Validate Based on Other Fields

```javascript
fields: [
  {
    type: 'checkbox',
    model: 'hasCompany',
    label: 'I represent a company'
  },
  {
    type: 'input',
    model: 'companyName',
    label: 'Company Name',
    visible: (model) => model.hasCompany,
    required: (model) => model.hasCompany,  // Required only if hasCompany is true
    validator: (value, field, model) => {
      if (model.hasCompany && !value) {
        return ['Company name is required'];
      }
      return [];
    }
  }
]
```

### Cross-Field Validation

```javascript
fields: [
  { type: 'input', inputType: 'number', model: 'minPrice', label: 'Min Price' },
  {
    type: 'input',
    inputType: 'number',
    model: 'maxPrice',
    label: 'Max Price',
    validator: (value, field, model) => {
      if (model.minPrice && parseFloat(value) < parseFloat(model.minPrice)) {
        return ['Max price must be greater than min price'];
      }
      return [];
    }
  }
]
```

## Validation Events

### Field-Level Events

```javascript
{
  type: 'input',
  model: 'email',
  validator: 'email',
  onValidated: (model, errors, field) => {
    if (errors.length > 0) {
      console.log('Email validation errors:', errors);
    } else {
      console.log('Email is valid');
    }
  }
}
```

### Form-Level Events

```vue
<vue-form-generator
  :schema="schema"
  :model="model"
  @validated="onFormValidated">
</vue-form-generator>

<script>
export default {
  methods: {
    onFormValidated(isValid, errors, component) {
      console.log('Form valid:', isValid);
      console.log('All errors:', errors);
    }
  }
}
</script>
```

## Complete Form Example

```javascript
const userSchema = {
  fields: [
    {
      type: 'input',
      inputType: 'text',
      model: 'username',
      label: 'Username',
      placeholder: 'Enter username',
      required: true,
      validator: ['required', 'string'],
      min: 3,
      max: 20,
      validateDebounceTime: 500,
      onValidated: (model, errors) => {
        console.log('Username validated:', errors);
      }
    },
    {
      type: 'input',
      inputType: 'email',
      model: 'email',
      label: 'Email',
      required: true,
      validator: ['required', 'email']
    },
    {
      type: 'input',
      inputType: 'password',
      model: 'password',
      label: 'Password',
      required: true,
      min: 8,
      validator: 'strongPassword'
    },
    {
      type: 'input',
      inputType: 'password',
      model: 'confirmPassword',
      label: 'Confirm Password',
      validator: (value, field, model) => {
        if (value !== model.password) {
          return ['Passwords do not match'];
        }
        return [];
      }
    },
    {
      type: 'select',
      model: 'role',
      label: 'Role',
      required: true,
      values: ['admin', 'user', 'guest'],
      validator: 'required'
    },
    {
      type: 'checkbox',
      model: 'agreeToTerms',
      label: 'I agree to the terms and conditions',
      required: true,
      validator: (value) => value ? [] : ['You must agree to the terms']
    }
  ]
};
```

## See Also

- [Built-in Validators](https://vue-generators.gitbook.io/vue-generators/validation/built-in-validators)
- [Custom Validators](https://icebob.gitbooks.io/vueformgenerator/content/validation/custom-validators.html)