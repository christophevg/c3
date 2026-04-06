# Field Types Reference

Complete reference for VueFormGenerator field types.

## Core Fields

### input

Basic input field with various types.

```javascript
{
  type: 'input',
  inputType: 'text',  // text, password, email, number, tel, url, etc.
  label: 'Field Label',
  model: 'fieldName',
  placeholder: 'Enter value',
  required: true,
  readonly: false,
  disabled: false,
  hint: 'Helper text',
  validator: 'string'
}
```

**Input Types:**

| Type | Description |
|------|-------------|
| `text` | Single-line text |
| `password` | Password (masked) |
| `email` | Email input |
| `number` | Numeric input |
| `tel` | Telephone number |
| `url` | URL input |
| `search` | Search input |
| `date` | Date picker (native) |
| `time` | Time picker (native) |
| `datetime-local` | Date and time (native) |

### textArea

Multi-line text input.

```javascript
{
  type: 'textArea',
  label: 'Description',
  model: 'description',
  placeholder: 'Enter description...',
  rows: 4,
  maxRows: 10,
  hint: 'Max 500 characters'
}
```

### select

Dropdown selection.

```javascript
// Static options
{
  type: 'select',
  label: 'Country',
  model: 'country',
  values: ['USA', 'Canada', 'Mexico']
}

// Object options
{
  type: 'select',
  label: 'Status',
  model: 'status',
  values: [
    { id: 'active', name: 'Active' },
    { id: 'inactive', name: 'Inactive' }
  ],
  selectOptions: {
    value: 'id',
    name: 'name'
  }
}

// Dynamic options (function)
{
  type: 'select',
  label: 'Region',
  model: 'region',
  values: function(model) {
    return getRegionsForCountry(model.country);
  }
}

// Multiple selection
{
  type: 'select',
  label: 'Tags',
  model: 'tags',
  values: ['tag1', 'tag2', 'tag3'],
  multi: true,
  selectOptions: {
    closeOnSelect: false
  }
}
```

### checkbox

Boolean checkbox.

```javascript
{
  type: 'checkbox',
  label: 'I agree to terms',
  model: 'agreed',
  default: false
}

// With custom label
{
  type: 'checkbox',
  label: 'Notifications',
  model: 'notifications',
  default: true,
  hint: 'Receive email notifications'
}
```

### checklist

Multiple checkbox selection.

```javascript
{
  type: 'checklist',
  label: 'Features',
  model: 'features',
  values: ['wifi', 'parking', 'pool', 'gym'],
  default: []
}

// Object values
{
  type: 'checklist',
  label: 'Permissions',
  model: 'permissions',
  values: [
    { value: 'read', name: 'Read' },
    { value: 'write', name: 'Write' },
    { value: 'delete', name: 'Delete' }
  ]
}
```

### radios

Radio button group.

```javascript
{
  type: 'radios',
  label: 'Gender',
  model: 'gender',
  values: [
    { value: 'male', name: 'Male' },
    { value: 'female', name: 'Female' },
    { value: 'other', name: 'Other' }
  ]
}

// Simple values
{
  type: 'radios',
  label: 'Priority',
  model: 'priority',
  values: ['low', 'medium', 'high']
}
```

### label

Static text display.

```javascript
{
  type: 'label',
  label: 'Created At',
  model: 'createdAt',
  get: (model) => formatDate(model.createdAt)
}
```

### submit

Submit button.

```javascript
{
  type: 'submit',
  label: 'Save Changes',
  buttonText: 'Submit',  // Alternative to label
  validateBeforeSubmit: true,
  onSubmit: function(model) {
    console.log('Submitted:', model);
  }
}
```

## Optional Fields

### cleave

Formatted input using Cleave.js.

```javascript
{
  type: 'cleave',
  label: 'Phone',
  model: 'phone',
  cleaveOptions: {
    phone: true,
    phoneRegionCode: 'US'
  }
}

// Credit card
{
  type: 'cleave',
  label: 'Credit Card',
  model: 'cardNumber',
  cleaveOptions: {
    creditCard: true
  }
}

// Date
{
  type: 'cleave',
  label: 'Date',
  model: 'date',
  cleaveOptions: {
    date: true,
    datePattern: ['Y', 'm', 'd']
  }
}
```

### dateTimePicker

Date/time picker (requires bootstrap-datetimepicker).

```javascript
{
  type: 'dateTimePicker',
  label: 'Event Date',
  model: 'eventDate',
  placeholder: 'Pick a date',
  format: 'YYYY-MM-DD HH:mm',
  dateTimePickerOptions: {
    format: 'YYYY-MM-DD HH:mm',
    showClear: true,
    showClose: true
  }
}
```

### pikaday

Date picker (Pikaday, no jQuery dependency).

```javascript
{
  type: 'pikaday',
  label: 'Birth Date',
  model: 'birthDate',
  placeholder: 'Select date',
  pikadayOptions: {
    format: 'YYYY-MM-DD',
    maxDate: new Date()
  }
}
```

### image

Image upload/URL input.

```javascript
{
  type: 'image',
  label: 'Profile Picture',
  model: 'avatar',
  placeholder: 'Image URL or upload',
  browse: true,  // Show browse button
  required: false,
  hideInput: false
}
```

### switch

Toggle switch.

```javascript
{
  type: 'switch',
  label: 'Enable Notifications',
  model: 'notificationsEnabled',
  default: false,
  textOn: 'Yes',
  textOff: 'No'
}
```

### slider

Range slider (ion.rangeSlider, jQuery required).

```javascript
{
  type: 'slider',
  label: 'Volume',
  model: 'volume',
  min: 0,
  max: 100,
  sliderOptions: {
    type: 'single',
    step: 1,
    postfix: '%'
  }
}
```

### noUiSlider

Range slider (noUiSlider, vanilla JS).

```javascript
{
  type: 'noUiSlider',
  label: 'Price Range',
  model: 'priceRange',
  min: 0,
  max: 1000,
  noUiSliderOptions: {
    start: [0, 500],
    step: 10,
    connect: true,
    tooltips: true
  }
}
```

### spectrum

Color picker (Spectrum, jQuery required).

```javascript
{
  type: 'spectrum',
  label: 'Theme Color',
  model: 'themeColor',
  spectrumOptions: {
    showAlpha: true,
    showInput: true,
    preferredFormat: 'hex'
  }
}
```

### vueMultiSelect

Enhanced multi-select dropdown.

```javascript
{
  type: 'vueMultiSelect',
  label: 'Tags',
  model: 'tags',
  multiSelectOptions: {
    multiple: true,
    searchable: true,
    allowEmpty: true,
    options: ['tag1', 'tag2', 'tag3']
  }
}
```

### googleAddress

Google Maps address autocomplete.

```javascript
{
  type: 'googleAddress',
  label: 'Address',
  model: 'address',
  placeholder: 'Enter address',
  googleApiKey: 'YOUR_API_KEY'
}
```

## Field Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `type` | String | Field type (required) |
| `label` | String | Display label |
| `model` | String | Model property (supports dot notation) |
| `id` | String | Field ID (auto-generated if not set) |
| `inputType` | String | Input type for 'input' fields |
| `placeholder` | String | Placeholder text |
| `default` | Any | Default value for new models |
| `required` | Boolean | Required field |
| `disabled` | Boolean/Function | Disabled state |
| `readonly` | Boolean/Function | Read-only state |
| `visible` | Boolean/Function | Visibility |
| `featured` | Boolean/Function | Bold styling |
| `hint` | String | Hint text below field |
| `help` | String | Tooltip on hover |
| `validator` | String/Function/Array | Validation |
| `validateDebounceTime` | Number | Validation debounce (ms) |
| `styleClasses` | String/Array | CSS classes |
| `attributes` | Object | Custom HTML attributes |
| `values` | Array/Function | Options for select/checklist |
| `onChanged` | Function | Change callback |
| `onValidated` | Function | Validation callback |
| `get` | Function | Getter transformation |
| `set` | Function | Setter transformation |
| `buttons` | Array | Action buttons |
| `attributes` | Object | HTML attributes |
| `inputName` | String | Name attribute for input |

## Conditional Property Syntax

All boolean properties can be functions that receive the model:

```javascript
{
  type: 'input',
  model: 'companyName',
  visible: function(model) {
    return model.type === 'business';
  },
  disabled: function(model) {
    return model.status === 'locked';
  },
  required: function(model) {
    return model.type === 'business';
  }
}
```

## Common Patterns

### Two-Column Layout

```javascript
schema: {
  fields: [
    { type: 'input', model: 'firstName', label: 'First Name', styleClasses: 'col-6' },
    { type: 'input', model: 'lastName', label: 'Last Name', styleClasses: 'col-6' }
  ]
}
```

### Dependent Fields

```javascript
fields: [
  {
    type: 'select',
    model: 'country',
    values: countries,
    onChanged: function(model) {
      model.region = null;  // Reset dependent field
    }
  },
  {
    type: 'select',
    model: 'region',
    values: function(model) {
      return getRegionsForCountry(model.country);
    },
    visible: function(model) {
      return !!model.country;
    }
  }
]
```

### Calculated Field

```javascript
{
  type: 'label',
  label: 'Total',
  model: 'total',
  get: function(model) {
    return model.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

### Read-Only Field

```javascript
{
  type: 'input',
  model: 'id',
  readonly: true,
  visible: function(model) {
    return !!model.id;  // Show only for existing records
  }
}
```

## See Also

- [VueFormGenerator Fields Documentation](https://vue-generators.gitbook.io/vue-generators/fields)
- [Field Properties](https://vue-generators.gitbook.io/vue-generators/fields/field_properties)