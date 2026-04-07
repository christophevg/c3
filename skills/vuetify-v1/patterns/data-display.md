# Vuetify 1.5 Data Display Patterns

## v-data-table

### Basic Table

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :search="search"
/>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `custom-filter` | function | - | Custom search filter |
| `custom-sort` | function | - | Custom sort function |
| `dark` | boolean | false | Dark theme |
| `disable-initial-sort` | boolean | false | Disable initial sort |
| `expand` | boolean | false | Enable row expansion |
| `filter` | function | - | Filter function |
| `headers` | array | [] | Column headers (required) |
| `hide-actions` | boolean | false | Hide pagination |
| `hide-headers` | boolean | false | Hide headers |
| `item-key` | string | 'id' | Unique row key |
| `items` | array | [] | Table data (required) |
| `light` | boolean | false | Light theme |
| `loading` | boolean/string | false | Loading state |
| `must-sort` | boolean | false | Force sorting |
| `pagination` | object | - | Pagination control |
| `rows-per-page-items` | array | [5,10,25] | Rows per page options |
| `rows-per-page-text` | string | 'Rows per page:' | Rows per page label |
| `search` | any | - | Search filter |
| `select-all` | boolean/string | false | Enable select all |
| `sort-icon` | string | 'arrow_up' | Sort icon |
| `total-items` | number | - | Total for server-side |

### Headers Structure

```javascript
headers: [
  {
    text: 'Name',
    value: 'name',
    align: 'left',      // 'left', 'center', 'right'
    sortable: true,
    class: 'custom-class',
    width: '25%'
  },
  {
    text: 'Status',
    value: 'status',
    align: 'center'
  },
  {
    text: 'Actions',
    value: 'actions',
    sortable: false
  }
]
```

### Table with Search

```vue
<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="items"
      :search="search"
    />
  </v-card>
</template>
```

### Custom Cell Template (V1.5 slot syntax)

```vue
<v-data-table :headers="headers" :items="items">
  <template slot="items" slot-scope="props">
    <td>{{ props.item.name }}</td>
    <td>{{ props.item.email }}</td>
    <td>
      <v-chip :color="props.item.status === 'active' ? 'success' : 'error'">
        {{ props.item.status }}
      </v-chip>
    </td>
    <td>
      <v-btn icon @click="edit(props.item)">
        <v-icon>edit</v-icon>
      </v-btn>
      <v-btn icon @click="delete(props.item)">
        <v-icon>delete</v-icon>
      </v-btn>
    </td>
  </template>
</v-data-table>
```

### Row Selection

```vue
<v-data-table
  v-model="selected"
  :headers="headers"
  :items="items"
  select-all
  item-key="id"
>
  <template slot="items" slot-scope="props">
    <td>
      <v-checkbox
        v-model="props.selected"
        primary
        hide-details
      />
    </td>
    <td>{{ props.item.name }}</td>
    <td>{{ props.item.email }}</td>
  </template>
</v-data-table>
```

### Expandable Rows

```vue
<v-data-table :headers="headers" :items="items" expand>
  <template slot="items" slot-scope="props">
    <tr @click="props.expanded = !props.expanded">
      <td>{{ props.item.name }}</td>
      <td>{{ props.item.email }}</td>
    </tr>
  </template>
  <template slot="expand" slot-scope="props">
    <v-card flat>
      <v-card-text>Expanded content for {{ props.item.name }}</v-card-text>
    </v-card>
  </template>
</v-data-table>
```

### Server-Side Pagination

```vue
<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :pagination.sync="pagination"
    :total-items="totalItems"
    :loading="loading"
    @update:pagination="fetchData"
  />
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      items: [],
      totalItems: 0,
      pagination: {
        descending: false,
        page: 1,
        rowsPerPage: 10,
        sortBy: 'name'
      }
    }
  },
  methods: {
    async fetchData() {
      this.loading = true
      const { page, rowsPerPage, sortBy, descending } = this.pagination
      const response = await fetch(
        `/api/items?page=${page}&limit=${rowsPerPage}&sort=${sortBy}&order=${descending ? 'desc' : 'asc'}`
      )
      const data = await response.json()
      this.items = data.items
      this.totalItems = data.total
      this.loading = false
    }
  }
}
</script>
```

## v-list

### Basic List

```vue
<v-list>
  <v-list-tile to="/home">
    <v-list-tile-action>
      <v-icon>home</v-icon>
    </v-list-tile-action>
    <v-list-tile-content>
      <v-list-tile-title>Home</v-list-tile-title>
    </v-list-tile-content>
  </v-list-tile>
</v-list>
```

### List Tile Props (V1.5 uses v-list-tile, V2 uses v-list-item)

| Prop | Type | Description |
|------|------|-------------|
| `active-class` | string | Active class |
| `avatar` | boolean | Avatar style |
| `disabled` | boolean | Disabled state |
| `to` | string/object | Router link |

### List with Avatar

```vue
<v-list two-line>
  <v-list-tile avatar>
    <v-list-tile-avatar>
      <img :src="user.avatar">
    </v-list-tile-avatar>
    <v-list-tile-content>
      <v-list-tile-title>{{ user.name }}</v-list-tile-title>
      <v-list-tile-sub-title>{{ user.email }}</v-list-tile-sub-title>
    </v-list-tile-content>
    <v-list-tile-action>
      <v-btn icon @click="edit">
        <v-icon>edit</v-icon>
      </v-btn>
    </v-list-tile-action>
  </v-list-tile>
</v-list>
```

### Expandable List Group

```vue
<v-list>
  <v-list-group prepend-icon="account_circle">
    <v-list-tile slot="activator">
      <v-list-tile-title>Users</v-list-tile-title>
    </v-list-tile>
    <v-list-tile to="/users/active">
      <v-list-tile-title>Active</v-list-tile-title>
    </v-list-tile>
    <v-list-tile to="/users/inactive">
      <v-list-tile-title>Inactive</v-list-tile-title>
    </v-list-tile>
  </v-list-group>
</v-list>
```

## v-card

### Basic Card

```vue
<v-card>
  <v-card-title>
    <h3>Card Title</h3>
  </v-card-title>
  <v-card-text>
    Card content goes here.
  </v-card-text>
  <v-card-actions>
    <v-btn flat color="primary">Action</v-btn>
    <v-spacer />
    <v-btn flat @click="cancel">Cancel</v-btn>
  </v-card-actions>
</v-card>
```

### Card with Image

```vue
<v-card>
  <v-card-media
    src="/images/hero.jpg"
    height="200px"
  />
  <v-card-title primary-title>
    <div>
      <h3 class="headline">Title</h3>
      <div>Secondary text</div>
    </div>
  </v-card-title>
  <v-card-text>
    Content here
  </v-card-text>
  <v-card-actions>
    <v-btn flat color="primary">Share</v-btn>
    <v-btn flat color="primary">Explore</v-btn>
  </v-card-actions>
</v-card>
```

### Card Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | string | - | Background color |
| `dark` | boolean | false | Dark theme |
| `elevation` | number/string | - | Shadow depth (0-24) |
| `flat` | boolean | false | No shadow |
| `height` | number/string | - | Fixed height |
| `hover` | boolean | false | Hover elevation |
| `img` | string | - | Background image |
| `light` | boolean | false | Light theme |
| `max-height` | number/string | - | Max height |
| `max-width` | number/string | - | Max width |
| `min-height` | number/string | - | Min height |
| `min-width` | number/string | - | Min width |
| `raised` | boolean | false | Higher elevation |
| `ripple` | boolean/object | - | Ripple effect |
| `tile` | boolean | false | No border radius |
| `to` | string/object | - | Router link |
| `width` | number/string | - | Fixed width |

### Horizontal Card

```vue
<v-card>
  <v-layout row>
    <v-flex xs7>
      <v-card-title>Card Title</v-card-title>
      <v-card-text>Content</v-card-text>
    </v-flex>
    <v-flex xs5>
      <v-card-media
        src="/images/thumbnail.jpg"
        height="150px"
        contain
      />
    </v-flex>
  </v-layout>
</v-card>
```

## v-chip

### Basic Chip

```vue
<v-chip>Default</v-chip>
<v-chip color="primary">Primary</v-chip>
<v-chip color="success" text-color="white">Success</v-chip>
```

### Closable Chip

```vue
<v-chip v-model="show" close @input="onClose">
  <v-avatar><img src="/avatar.jpg"></v-avatar>
  John Doe
</v-chip>
```

### Chip with Icon

```vue
<v-chip>
  <v-avatar class="primary">
    <v-icon>account_circle</v-icon>
  </v-avatar>
  User Name
</v-chip>
```

### Outline Chip

```vue
<v-chip outline color="primary">Outline</v-chip>
```

### Label Chip

```vue
<v-chip label color="pink" text-color="white">
  <v-icon left>label</v-icon>
  Tag
</v-chip>
```

## v-divider

```vue
<v-list>
  <v-list-tile>Item 1</v-list-tile>
  <v-list-tile>Item 2</v-list-tile>
  <v-divider />
  <v-list-tile>Item 3</v-list-tile>
</v-list>

<!-- Inset divider -->
<v-divider inset />

<!-- Vertical divider (in horizontal layout) -->
<v-layout row>
  <v-flex xs6>Left</v-flex>
  <v-divider vertical />
  <v-flex xs6>Right</v-flex>
</v-layout>
```

## v-avatar

```vue
<v-avatar size="36">
  <img src="/avatar.jpg" alt="Avatar">
</v-avatar>

<v-avatar color="primary">
  <span class="white--text headline">JD</span>
</v-avatar>

<v-avatar tile>
  <img src="/logo.png">
</v-avatar>
```

## v-timeline (V1.5 syntax)

```vue
<v-timeline>
  <v-timeline-item
    v-for="(event, i) in events"
    :key="i"
    :color="event.color"
  >
    <template slot="opposite">
      <span>{{ event.date }}</span>
    </template>
    <v-card>
      <v-card-title>{{ event.title }}</v-card-title>
      <v-card-text>{{ event.content }}</v-card-text>
    </v-card>
  </v-timeline-item>
</v-timeline>
```