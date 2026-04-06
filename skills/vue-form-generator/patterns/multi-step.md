# Multi-Step Forms

Implementing wizard-style forms with VueFormGenerator.

## Overview

VueFormGenerator doesn't have built-in multi-step support. Implement it by splitting schemas and managing step state manually.

## Basic Multi-Step Form

```vue
<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{ steps[currentStep].legend }}</span>
      <v-spacer />
      <span class="subtitle-1">Step {{ currentStep + 1 }} of {{ steps.length }}</span>
    </v-card-title>

    <v-card-text>
      <!-- Progress bar -->
      <v-progress-linear
        :value="(currentStep / (steps.length - 1)) * 100"
        class="mb-4" />

      <!-- Current step form -->
      <vue-form-generator
        ref="form"
        :schema="steps[currentStep]"
        :model="model"
        :options="formOptions"
        @validated="onStepValidated" />
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        @click="prevStep"
        :disabled="currentStep === 0">
        Previous
      </v-btn>
      <v-spacer />
      <v-btn
        v-if="currentStep < steps.length - 1"
        color="primary"
        @click="nextStep"
        :disabled="!stepValid">
        Next
      </v-btn>
      <v-btn
        v-else
        color="primary"
        @click="submit"
        :disabled="!stepValid">
        Submit
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      currentStep: 0,
      stepValid: false,
      model: {
        // Personal info
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        // Address
        street: '',
        city: '',
        state: '',
        zip: '',
        // Preferences
        newsletter: false,
        notifications: 'email'
      },
      steps: [
        {
          legend: 'Personal Information',
          fields: [
            { type: 'input', inputType: 'text', model: 'firstName', label: 'First Name', required: true },
            { type: 'input', inputType: 'text', model: 'lastName', label: 'Last Name', required: true },
            { type: 'input', inputType: 'email', model: 'email', label: 'Email', required: true, validator: 'email' },
            { type: 'input', inputType: 'tel', model: 'phone', label: 'Phone' }
          ]
        },
        {
          legend: 'Address',
          fields: [
            { type: 'input', inputType: 'text', model: 'street', label: 'Street Address', required: true },
            { type: 'input', inputType: 'text', model: 'city', label: 'City', required: true },
            { type: 'select', model: 'state', label: 'State', values: this.getStates(), required: true },
            { type: 'input', inputType: 'text', model: 'zip', label: 'ZIP Code', required: true }
          ]
        },
        {
          legend: 'Preferences',
          fields: [
            { type: 'checkbox', model: 'newsletter', label: 'Subscribe to newsletter' },
            { type: 'radios', model: 'notifications', label: 'Notification Preference', values: ['email', 'sms', 'none'] }
          ]
        }
      ],
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      }
    }
  },
  methods: {
    onStepValidated(isValid, errors) {
      this.stepValid = isValid
    },
    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--
      }
    },
    nextStep() {
      if (this.$refs.form.validate()) {
        this.currentStep++
      }
    },
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit('submit', this.model)
      }
    },
    getStates() {
      return ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA']
    }
  }
}
</script>
```

## Wizard with Progress Steps

```vue
<template>
  <v-card>
    <!-- Step indicators -->
    <v-stepper v-model="currentStep" alt-labels>
      <v-stepper-header>
        <v-stepper-step
          v-for="(step, index) in steps"
          :key="index"
          :step="index + 1"
          :complete="index < currentStep"
          :editable="index <= maxCompletedStep">
          {{ step.legend }}
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content
          v-for="(step, index) in steps"
          :key="index"
          :step="index + 1">
          <vue-form-generator
            ref="form"
            :schema="step"
            :model="model"
            :options="formOptions" />

          <v-btn
            text
            @click="prevStep"
            :disabled="currentStep === 1">
            Previous
          </v-btn>
          <v-btn
            v-if="currentStep < steps.length"
            color="primary"
            @click="nextStep">
            Next
          </v-btn>
          <v-btn
            v-else
            color="primary"
            @click="submit">
            Submit
          </v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-card>
</template>
```

## API-Driven Multi-Step Form

```javascript
// Load steps from API
async loadFormSchema() {
  const response = await fetch('/api/form-schema?form=registration')
  const data = await response.json()

  this.steps = data.steps.map(step => ({
    legend: step.title,
    fields: step.fields.map(field => ({
      type: field.type,
      model: field.model,
      label: field.label,
      required: field.required,
      validator: field.validator,
      values: field.values  // Could be API-driven too
    }))
  }))

  this.model = data.model || {}
}
```

## Step Validation State

Track validation state per step:

```javascript
data() {
  return {
    currentStep: 0,
    stepValidation: [],  // Track validity per step
    steps: [...]
  }
},
methods: {
  onStepValidated(isValid, errors) {
    this.$set(this.stepValidation, this.currentStep, isValid)
  },
  canProceedToStep(stepIndex) {
    // All previous steps must be valid
    return this.stepValidation.slice(0, stepIndex).every(valid => valid)
  },
  getStepStatus(stepIndex) {
    if (this.currentStep > stepIndex) {
      return this.stepValidation[stepIndex] ? 'completed' : 'error'
    }
    return this.currentStep === stepIndex ? 'active' : 'pending'
  }
}
```

## Save and Resume

Persist form state to allow resuming:

```javascript
// Save state to localStorage
saveState() {
  const state = {
    currentStep: this.currentStep,
    model: this.model,
    timestamp: Date.now()
  }
  localStorage.setItem('form-state', JSON.stringify(state))
},

// Resume from saved state
resumeState() {
  const saved = localStorage.getItem('form-state')
  if (saved) {
    const state = JSON.parse(saved)
    // Check if state is recent (e.g., within 24 hours)
    if (Date.now() - state.timestamp < 24 * 60 * 60 * 1000) {
      this.currentStep = state.currentStep
      this.model = state.model
    }
  }
},

// Clear saved state
clearState() {
  localStorage.removeItem('form-state')
}
```

## Complete Wizard Component

```vue
<template>
  <v-card class="wizard-form">
    <v-card-title>
      <v-row align="center">
        <v-col>
          <h2 class="headline">{{ title }}</h2>
        </v-col>
        <v-col cols="auto">
          <v-chip small>Step {{ currentStepIndex + 1 }} of {{ steps.length }}</v-chip>
        </v-col>
      </v-row>
    </v-card-title>

    <!-- Progress indicator -->
    <v-card-text>
      <v-stepper v-model="currentStepIndex" class="elevation-0">
        <v-stepper-header>
          <template v-for="(step, index) in steps">
            <v-stepper-step
              :key="`step-${index}`"
              :step="index + 1"
              :complete="isStepComplete(index)"
              :editable="canEditStep(index)">
              {{ step.legend }}
            </v-stepper-step>
            <v-divider
              v-if="index < steps.length - 1"
              :key="`divider-${index}`" />
          </template>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content
            v-for="(step, index) in steps"
            :key="index"
            :step="index + 1">
            <vue-form-generator
              :ref="`form-${index}`"
              :schema="step"
              :model="model"
              :options="formOptions"
              @validated="(valid) => onStepValidated(index, valid)" />

            <div class="mt-4">
              <v-btn
                v-if="index > 0"
                text
                @click="prevStep">
                <v-icon left>mdi-arrow-left</v-icon>
                Previous
              </v-btn>
              <v-spacer />
              <v-btn
                v-if="index < steps.length - 1"
                color="primary"
                @click="nextStep"
                :disabled="!stepValidity[index]">
                Next
                <v-icon right>mdi-arrow-right</v-icon>
              </v-btn>
              <v-btn
                v-else
                color="primary"
                @click="submit"
                :disabled="!stepValidity[index]">
                <v-icon left>mdi-check</v-icon>
                Submit
              </v-btn>
            </div>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'WizardForm',
  props: {
    title: String,
    steps: {
      type: Array,
      required: true
    },
    initialModel: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      currentStepIndex: 0,
      model: { ...this.initialModel },
      stepValidity: this.steps.map(() => false),
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      }
    }
  },
  methods: {
    onStepValidated(index, isValid) {
      this.$set(this.stepValidity, index, isValid)
    },
    isStepComplete(index) {
      return index < this.currentStepIndex && this.stepValidity[index]
    },
    canEditStep(index) {
      return index <= this.currentStepIndex
    },
    prevStep() {
      if (this.currentStepIndex > 0) {
        this.currentStepIndex--
      }
    },
    nextStep() {
      const form = this.$refs[`form-${this.currentStepIndex}`]
      if (form && form[0] && form[0].validate()) {
        this.currentStepIndex++
      }
    },
    submit() {
      // Validate all steps
      let allValid = true
      this.steps.forEach((_, index) => {
        const form = this.$refs[`form-${index}`]
        if (form && form[0] && !form[0].validate()) {
          allValid = false
        }
      })

      if (allValid) {
        this.$emit('submit', this.model)
      }
    }
  }
}
</script>
```

## See Also

- [VueFormGenerator Groups](https://vue-generators.gitbook.io/vue-generators/groups)
- [Vuetify Stepper](https://vuetifyjs.com/en/components/steppers/)