# Data Display Patterns

Comprehensive patterns for Vuetify V3 data display components.

## Data Tables

### v-data-table (Client-Side)

Client-side data table with sorting and filtering.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `headers` | array | Column definitions |
| `items` | array | Table data |
| `search` | string | Search filter |
| `sort-by` | array | Sort configuration |
| `group-by` | array | Group configuration |
| `loading` | boolean | Loading state |
| `density` | string | Density: `default`, `comfortable`, `compact` |
| `hover` | boolean | Hover effect on rows |
| `items-per-page` | number | Items per page (default: 10) |
| `show-select` | boolean | Show checkbox for selection |
| `show-expand` | boolean | Show expand button |

**V3 Changes:**
- `value` prop → `model-value`
- `@input` event → `@update:model-value`
- Sort format: `[{ key: 'field', order: 'asc' }]`
- `item-value` required for selection
- Slot syntax: `#item.field="{ item }"` instead of `slot="item"` and `slot-scope`

```vue
<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :search="search"
    :sort-by="sortBy"
    class="elevation-1"
  >
    <template #top>
      <v-toolbar flat>
        <v-toolbar-title>Users</v-toolbar-title>
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
      </v-toolbar>
    </template>

    <template #item.status="{ item }">
      <v-chip :color="item.status === 'active' ? 'success' : 'error'">
        {{ item.status }}
      </v-chip>
    </template>

    <template #item.actions="{ item }">
      <v-icon icon="mdi-pencil" class="mr-2" @click="editItem(item)" />
      <v-icon icon="mdi-delete" @click="deleteItem(item)" />
    </template>
  </v-data-table>
</template>

<script setup>
import { ref } from 'vue'

const search = ref('')
const sortBy = ref([{ key: 'name', order: 'asc' }])

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Email', key: 'email', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

const items = [
  { name: 'John Doe', email: 'john@example.com', status: 'active' },
  { name: 'Jane Smith', email: 'jane@example.com', status: 'inactive' }
]
</script>
```

### v-data-table-server (Server-Side)

Server-side data table for large datasets.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `headers` | array | Column definitions |
| `items` | array | Table data from server |
| `items-length` | number | Total items on server |
| `loading` | boolean | Loading state |
| `items-per-page` | number | Items per page |

**Key Events:**

| Event | Description |
|-------|-------------|
| `@update:options` | Pagination/sorting changes |
| `@update:page` | Page change |
| `@update:items-per-page` | Items per page change |
| `@update:sort-by` | Sort change |

**Note:** Vuetify does NOT have built-in server-side filtering. Implement custom search fields.

```vue
<template>
  <v-data-table-server
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    :items-per-page="itemsPerPage"
    @update:options="loadItems"
  >
    <template #top>
      <v-text-field
        v-model="search"
        label="Search"
        @update:model-value="searchItems"
      />
    </template>

    <template #item.name="{ item }">
      <strong>{{ item.name }}</strong>
    </template>
  </v-data-table-server>
</template>

<script setup>
import { ref } from 'vue'

const search = ref('')
const loading = ref(false)
const serverItems = ref([])
const totalItems = ref(0)
const itemsPerPage = ref(10)

const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  loading.value = true

  try {
    // Build query parameters
    const params = new URLSearchParams({
      page,
      perPage: itemsPerPage,
    })

    // Add sort parameters
    if (sortBy.length) {
      params.append('sortBy', sortBy[0].key)
      params.append('sortOrder', sortBy[0].order)
    }

    // Add search
    if (search.value) {
      params.append('search', search.value)
    }

    const response = await fetch(`/api/data?${params}`)
    const data = await response.json()

    serverItems.value = data.items
    totalItems.value = data.total
  } finally {
    loading.value = false
  }
}

const searchItems = () => {
  loadItems({ page: 1, itemsPerPage: itemsPerPage.value, sortBy: [] })
}
</script>
```

### Data Table with Selection

```vue
<v-data-table
  v-model="selected"
  :headers="headers"
  :items="items"
  item-value="id"
  show-select
>
  <template #item.name="{ item }">
    {{ item.name }}
  </template>
</v-data-table>

<script setup>
import { ref } from 'vue'

const selected = ref([])

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' }
]

const items = [
  { id: 1, name: 'John', email: 'john@example.com' },
  { id: 2, name: 'Jane', email: 'jane@example.com' }
]
</script>
```

### Data Table with Expansion

```vue
<v-data-table
  :headers="headers"
  :items="items"
  show-expand
>
  <template #expanded-row="{ item }">
    <tr>
      <td colspan="3">
        <v-card flat>
          <v-card-text>
            {{ item.details }}
          </v-card-text>
        </v-card>
      </td>
    </tr>
  </template>
</v-data-table>
```

### Data Table with Grouping

```vue
<v-data-table
  :headers="headers"
  :items="items"
  group-by="category"
>
  <template #group-header="{ item, isOpen, toggle }">
    <tr>
      <td colspan="3">
        <v-btn @click="toggle" icon>
          <v-icon :icon="isOpen ? 'mdi-minus' : 'mdi-plus'" />
        </v-btn>
        {{ item.value }} ({{ item.items.length }} items)
      </td>
    </tr>
  </template>
</v-data-table>
```

## Simple Table

### v-table

Simple table without built-in features (renamed from `v-simple-table` in V2).

```vue
<v-table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="item in items" :key="item.id">
      <td>{{ item.name }}</td>
      <td>{{ item.email }}</td>
      <td>
        <v-chip :color="item.status === 'active' ? 'success' : 'error'">
          {{ item.status }}
        </v-chip>
      </td>
    </tr>
  </tbody>
</v-table>
```

## Cards

### v-card

Versatile container for content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `variant` | string | Style: `elevated`, `flat`, `tonal`, `outlined`, `text`, `plain` |
| `color` | string | Background color |
| `elevation` | number | Shadow elevation |
| `loading` | boolean | Loading state |
| `hover` | boolean | Hover elevation effect |
| `to` | string/object | Vue Router link |
| `href` | string | External link |
| `disabled` | boolean | Disable card |
| `rounded` | string/boolean | Border radius |
| `max-width` | number/string | Maximum width |

**V3 Changes:**
- `raised` prop removed, use `variant="elevated"`
- `flat` prop → use `variant="flat"`

```vue
<!-- Basic card -->
<v-card>
  <v-card-title>Card Title</v-card-title>
  <v-card-text>Card content goes here.</v-card-text>
  <v-card-actions>
    <v-btn color="primary">Action</v-btn>
  </v-card-actions>
</v-card>

<!-- Elevated card -->
<v-card variant="elevated" elevation="8">
  <v-card-title>Elevated Card</v-card-title>
</v-card>

<!-- Outlined card -->
<v-card variant="outlined">
  <v-card-title>Outlined Card</v-card-title>
</v-card>

<!-- Loading card -->
<v-card :loading="loading">
  <v-card-title>Loading Card</v-card-title>
</v-card>

<!-- Card with image -->
<v-card max-width="400">
  <v-img
    src="https://example.com/image.jpg"
    height="200"
    cover
  />
  <v-card-title>Card with Image</v-card-title>
  <v-card-text>Description of the card.</v-card-text>
  <v-card-actions>
    <v-btn color="primary" variant="text">Share</v-btn>
    <v-btn color="primary" variant="text">Learn More</v-btn>
  </v-card-actions>
</v-card>

<!-- Router link card -->
<v-card to="/details" hover>
  <v-card-title>Clickable Card</v-card-title>
</v-card>
```

### Card Sub-components

```vue
<v-card>
  <!-- Title -->
  <v-card-title>
    <v-icon icon="mdi-account" start />
    Card Title
  </v-card-title>

  <!-- Subtitle -->
  <v-card-subtitle>Card Subtitle</v-card-subtitle>

  <!-- Text content -->
  <v-card-text>
    <p>Card text content goes here.</p>
  </v-card-text>

  <!-- Image -->
  <v-card-img src="image.jpg" height="200" />

  <!-- Actions -->
  <v-card-actions>
    <v-btn color="primary">Action 1</v-btn>
    <v-spacer />
    <v-btn>Cancel</v-btn>
  </v-card-actions>
</v-card>
```

## Lists

### v-list

Display interface for items.

**V3 Changes:**
- `v-list-item-content` removed (use CSS grid)
- `v-list-item-group` removed (use `v-model:selected` on `v-list`)
- Use `v-list-item-title` and `v-list-item-subtitle` directly

```vue
<!-- Basic list -->
<v-list>
  <v-list-item to="/home">
    <template #prepend>
      <v-icon icon="mdi-home" />
    </template>
    <v-list-item-title>Home</v-list-item-title>
  </v-list-item>

  <v-list-item to="/settings">
    <template #prepend>
      <v-icon icon="mdi-cog" />
    </template>
    <v-list-item-title>Settings</v-list-item-title>
  </v-list-item>
</v-list>

<!-- List with selection (V3) -->
<v-list v-model:selected="selected" selectable>
  <v-list-item value="item1">
    <template #prepend>
      <v-icon icon="mdi-home" />
    </template>
    <v-list-item-title>Item 1</v-list-item-title>
  </v-list-item>

  <v-list-item value="item2">
    <template #prepend>
      <v-icon icon="mdi-cog" />
    </template>
    <v-list-item-title>Item 2</v-list-item-title>
  </v-list-item>
</v-list>

<script setup>
import { ref } from 'vue'
const selected = ref([])
</script>

<!-- List with avatar -->
<v-list>
  <v-list-item>
    <template #prepend>
      <v-avatar :image="user.avatar" />
    </template>
    <v-list-item-title>{{ user.name }}</v-list-item-title>
    <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
  </v-list-item>
</v-list>

<!-- Two-line list -->
<v-list lines="two">
  <v-list-item>
    <template #prepend>
      <v-icon icon="mdi-account" />
    </template>
    <v-list-item-title>Two-line Item</v-list-item-title>
    <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
  </v-list-item>
</v-list>

<!-- Three-line list -->
<v-list lines="three">
  <v-list-item>
    <template #prepend>
      <v-icon icon="mdi-account" />
    </template>
    <v-list-item-title>Three-line Item</v-list-item-title>
    <v-list-item-subtitle>
      First line of secondary text
    </v-list-item-subtitle>
    <v-list-item-subtitle>
      Second line of secondary text
    </v-list-item-subtitle>
  </v-list-item>
</v-list>

<!-- List group (expandable) -->
<v-list>
  <v-list-group value="settings">
    <template #activator="{ props }">
      <v-list-item v-bind="props">
        <template #prepend>
          <v-icon icon="mdi-cog" />
        </template>
        <v-list-item-title>Settings</v-list-item-title>
      </v-list-item>
    </template>

    <v-list-item to="/settings/general">
      <v-list-item-title>General</v-list-item-title>
    </v-list-item>

    <v-list-item to="/settings/security">
      <v-list-item-title>Security</v-list-item-title>
    </v-list-item>
  </v-list-group>
</v-list>
```

## Chips

### v-chip

Small pieces of information for tags, filters, and selections.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Background color |
| `variant` | string | Style: `elevated`, `flat`, `tonal`, `outlined`, `text`, `plain` |
| `size` | string | Size: `x-small`, `small`, `default`, `large`, `x-large` |
| `closable` | boolean | Show close button |
| `draggable` | boolean | Enable dragging |
| `filter` | boolean | Filter chip (for chip groups) |
| `label` | boolean | Square corners |
| `outlined` | boolean | Outlined style (deprecated, use variant) |
| `pill` | boolean | Pill shape |

**V3 Changes:**
- `close` prop → `closable`
- `outlined` prop → `variant="outlined"`
- `@click:close` event → `@click:close` (same)

```vue
<!-- Basic chip -->
<v-chip>Basic Chip</v-chip>

<!-- Colored chip -->
<v-chip color="primary">Primary</v-chip>
<v-chip color="success">Success</v-chip>
<v-chip color="error">Error</v-chip>

<!-- Closable chip -->
<v-chip closable @click:close="removeChip">
  <v-icon start icon="mdi-account" />
  John Doe
</v-chip>

<!-- Filter chip (for chip groups) -->
<v-chip-group v-model="selected">
  <v-chip filter value="vue">Vue.js</v-chip>
  <v-chip filter value="react">React</v-chip>
  <v-chip filter value="angular">Angular</v-chip>
</v-chip-group>

<!-- Draggable chip -->
<v-chip draggable @dragstart="onDragStart">
  Drag me
</v-chip>

<!-- Chip with avatar -->
<v-chip>
  <v-avatar start>
    <v-icon icon="mdi-account" />
  </v-avatar>
  John Doe
</v-chip>

<!-- Chip with image -->
<v-chip>
  <v-avatar start image="avatar.jpg" />
  John Doe
</v-chip>
```

### v-chip-group

Group of selectable chips.

```vue
<v-chip-group v-model="selected" column multiple>
  <v-chip filter>Vue.js</v-chip>
  <v-chip filter>React</v-chip>
  <v-chip filter>Angular</v-chip>
</v-chip-group>

<script setup>
import { ref } from 'vue'
const selected = ref([])
</script>
```

## Data Iterator

### v-data-iterator

Grid layout with pagination and filtering.

```vue
<v-data-iterator
  :items="items"
  :items-per-page="12"
  :search="search"
>
  <template #header>
    <v-toolbar>
      <v-text-field
        v-model="search"
        label="Search"
        hide-details
      />
    </v-toolbar>
  </template>

  <template #default="{ items }">
    <v-row>
      <v-col
        v-for="item in items"
        :key="item.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card>
          <v-card-title>{{ item.name }}</v-card-title>
          <v-card-text>{{ item.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </template>
</v-data-iterator>
```

## Virtual Scroll

### v-virtual-scroll

Efficient rendering of long lists.

```vue
<v-virtual-scroll
  :items="items"
  :item-height="50"
  height="400"
>
  <template #default="{ item }">
    <v-list-item>
      <v-list-item-title>{{ item.name }}</v-list-item-title>
    </v-list-item>
  </template>
</v-virtual-scroll>

<script setup>
import { ref } from 'vue'

const items = ref(
  Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`
  }))
)
</script>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Data table not sorting | Use `sort-by` with array: `[{ key: 'field', order: 'asc' }]` |
| Server table not filtering | Implement custom search, Vuetify doesn't filter server tables |
| Selection not working | Add `item-value` prop and use `v-model` |
| List group not expanding | Ensure `value` prop is set on `v-list-group` |
| Chip group not selecting | Use `v-model` and `value` on chips |
| `v-list-item-content` error | Removed in V3, use children directly |
| Table slots not working | Use `#item.field="{ item }"` syntax, not `slot="item"` |
| Card link not working | Use `to` for router links, `href` for external links |