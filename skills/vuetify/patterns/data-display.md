# Data Display Patterns

Comprehensive patterns for Vuetify V2 data display components: tables, cards, lists, and more.

## Data Tables

### v-data-table

Display large amounts of data in a tabular format.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `headers` | array | Column definitions |
| `items` | array | Data objects |
| `search` | string | Text search filter |
| `sort-by` | array | Sort column(s) |
| `sort-desc` | boolean/array | Sort direction |
| `page` | number | Current page (1-indexed) |
| `items-per-page` | number | Items per page (-1 for all) |
| `loading` | boolean | Show loading state |
| `hide-default-footer` | boolean | Hide pagination |
| `hide-default-header` | boolean | Hide header |
| `dense` | boolean | Dense style |
| `footer-props` | object | Footer customization |

**Basic Usage:**

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :search="search"
  class="elevation-1"
/>

<script>
export default {
  data: () => ({
    search: '',
    headers: [
      { text: 'ID', value: 'id' },
      { text: 'Name', value: 'name' },
      { text: 'Email', value: 'email' },
      { text: 'Status', value: 'status' },
      { text: 'Actions', value: 'actions', sortable: false }
    ],
    items: [
      { id: 1, name: 'John', email: 'john@example.com', status: 'active' },
      { id: 2, name: 'Jane', email: 'jane@example.com', status: 'inactive' }
    ]
  })
}
</script>
```

### Custom Cell Slots

```vue
<v-data-table :headers="headers" :items="items">
  <!-- Custom status cell -->
  <template v-slot:item.status="{ item }">
    <v-chip
      :color="item.status === 'active' ? 'success' : 'error'"
      small
    >
      {{ item.status }}
    </v-chip>
  </template>

  <!-- Custom actions cell -->
  <template v-slot:item.actions="{ item }">
    <v-btn icon small @click="edit(item)">
      <v-icon small>mdi-pencil</v-icon>
    </v-btn>
    <v-btn icon small @click="delete(item)">
      <v-icon small>mdi-delete</v-icon>
    </v-btn>
  </template>
</v-data-table>
```

### Data Table with Search

```vue
<template>
  <v-card>
    <v-card-title>
      Users
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
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

### Data Table with Pagination

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :options.sync="options"
  :server-items-length="totalItems"
  :loading="loading"
  class="elevation-1"
  @update:options="loadItems"
/>

<script>
export default {
  data: () => ({
    totalItems: 0,
    items: [],
    loading: true,
    options: {},
    headers: [
      { text: 'ID', value: 'id' },
      { text: 'Name', value: 'name' }
    ]
  }),
  watch: {
    options: {
      handler() {
        this.loadItems()
      },
      deep: true
    }
  },
  methods: {
    async loadItems() {
      this.loading = true
      const { page, itemsPerPage, sortBy, sortDesc } = this.options
      // Fetch from API
      const response = await this.fetchItems(page, itemsPerPage, sortBy, sortDesc)
      this.items = response.items
      this.totalItems = response.total
      this.loading = false
    }
  }
}
</script>
```

### Server-side Data Table

```vue
<v-data-table
  :headers="headers"
  :items="items"
  :options.sync="options"
  :server-items-length="totalItems"
  :loading="loading"
  :footer-props="{
    'items-per-page-options': [10, 20, 50, 100]
  }"
  @update:options="updateOptions"
>
  <template v-slot:top>
    <v-toolbar flat>
      <v-toolbar-title>Users</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="dialog = true">
        New Item
      </v-btn>
    </v-toolbar>
  </template>
</v-data-table>
```

## Cards

### v-card

Versatile container for content.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `elevation` | number | Shadow depth 0-24 |
| `tile` | boolean | Remove border-radius |
| `flat` | boolean | Remove shadow |
| `outlined` | boolean | Outline border |
| `color` | string | Background color |
| `hover` | boolean | Higher elevation on hover |
| `loading` | boolean | Show loading state |
| `rounded` | string | Border-radius control |
| `max-width` | string/number | Maximum width |

**Card Components:**

- `v-card-title` - Title area
- `v-card-subtitle` - Subtitle area
- `v-card-text` - Text content
- `v-card-actions` - Action buttons area
- `v-card-img` - Image component

```vue
<!-- Basic card -->
<v-card>
  <v-card-title>Title</v-card-title>
  <v-card-text>Content here</v-card-text>
  <v-card-actions>
    <v-btn text>Action</v-btn>
  </v-card-actions>
</v-card>

<!-- Card with image -->
<v-card max-width="400">
  <v-img src="image.jpg" height="200" />
  <v-card-title>Card Title</v-card-title>
  <v-card-text>
    This is the card description.
  </v-card-text>
  <v-card-actions>
    <v-btn color="primary" text>Share</v-btn>
    <v-btn color="primary" text>Explore</v-btn>
  </v-card-actions>
</v-card>

<!-- Outlined card -->
<v-card outlined>
  <v-card-title>Outlined Card</v-card-title>
</v-card>

<!-- Hover effect -->
<v-card hover>
  <v-card-title>Hover Card</v-card-title>
</v-card>
```

### Card with Actions

```vue
<v-card>
  <v-card-title>
    <span class="headline">Edit User</span>
    <v-spacer />
    <v-btn icon @click="close">
      <v-icon>mdi-close</v-icon>
    </v-btn>
  </v-card-title>

  <v-card-text>
    <!-- Form content -->
  </v-card-text>

  <v-card-actions>
    <v-spacer />
    <v-btn text @click="close">Cancel</v-btn>
    <v-btn color="primary" @click="save">Save</v-btn>
  </v-card-actions>
</v-card>
```

### Media Card

```vue
<v-card max-width="300">
  <v-img src="photo.jpg" height="200">
    <v-card-title class="white--text align-end">
      Image Title
    </v-card-title>
  </v-img>

  <v-card-text>
    <div>Location: Paris, France</div>
    <div>Date: June 2024</div>
  </v-card-text>

  <v-card-actions>
    <v-btn icon>
      <v-icon>mdi-heart</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-share-variant</v-icon>
    </v-btn>
    <v-spacer />
    <v-btn icon>
      <v-icon>mdi-bookmark</v-icon>
    </v-btn>
  </v-card-actions>
</v-card>
```

### Card Grid

```vue
<v-container>
  <v-row>
    <v-col v-for="card in cards" :key="card.id" cols="12" sm="6" md="4" lg="3">
      <v-card>
        <v-img :src="card.image" height="200" />
        <v-card-title>{{ card.title }}</v-card-title>
        <v-card-text>{{ card.description }}</v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-container>
```

## Lists

### v-list

Display interface for items.

**Key Props:**

| Prop | Type | Description |
|------|------|-------------|
| `dense` | boolean | Dense style |
| `nav` | boolean | Navigation style |
| `two-line` | boolean | Two lines per item |
| `three-line` | boolean | Three lines per item |
| `subheader` | boolean | Include subheader |

**List Components:**

- `v-list-item` - List item container
- `v-list-item-icon` - Icon
- `v-list-item-content` - Content area
- `v-list-item-title` - Title
- `v-list-item-subtitle` - Subtitle
- `v-list-item-avatar` - Avatar image
- `v-list-item-action` - Action area

```vue
<!-- Basic list -->
<v-list>
  <v-list-item v-for="item in items" :key="item.id">
    <v-list-item-icon>
      <v-icon>{{ item.icon }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>{{ item.title }}</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</v-list>

<!-- Navigation list -->
<v-list nav dense>
  <v-list-item to="/" exact>
    <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
  <v-list-item to="/settings">
    <v-list-item-icon><v-icon>mdi-cog</v-icon></v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>Settings</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</v-list>

<!-- Two-line list with avatar -->
<v-list two-line>
  <v-list-item v-for="user in users" :key="user.id">
    <v-list-item-avatar>
      <v-img :src="user.avatar" />
    </v-list-item-avatar>
    <v-list-item-content>
      <v-list-item-title>{{ user.name }}</v-list-item-title>
      <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn icon @click="edit(user)">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</v-list>
```

### List with Subheaders

```vue
<v-list subheader>
  <v-subheader>Navigation</v-subheader>
  <v-list-item to="/">
    <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item-content>
  </v-list-item>

  <v-subheader>Settings</v-subheader>
  <v-list-item to="/settings">
    <v-list-item-icon><v-icon>mdi-cog</v-icon></v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>Settings</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</v-list>
```

### Expandable List Groups

```vue
<v-list>
  <v-list-group
    v-for="group in groups"
    :key="group.id"
    :prepend-icon="group.icon"
    no-action
  >
    <template v-slot:activator>
      <v-list-item-content>
        <v-list-item-title>{{ group.title }}</v-list-item-title>
      </v-list-item-content>
    </template>

    <v-list-item
      v-for="item in group.items"
      :key="item.id"
      :to="item.to"
    >
      <v-list-item-content>
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list-group>
</v-list>
```

## Expansion Panels

### v-expansion-panel

Accordion-style content.

```vue
<v-expansion-panels>
  <v-expansion-panel v-for="item in items" :key="item.id">
    <v-expansion-panel-header>
      {{ item.title }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      {{ item.content }}
    </v-expansion-panel-content>
  </v-expansion-panel>
</v-expansion-panels>

<!-- Multiple open -->
<v-expansion-panels multiple>
  <!-- panels -->
</v-expansion-panels>

<!-- Accordion (only one open) -->
<v-expansion-panels accordion>
  <!-- panels -->
</v-expansion-panels>

<!-- Inset style -->
<v-expansion-panels inset>
  <!-- panels -->
</v-expansion-panels>
```

## Timelines

### v-timeline

Display events chronologically.

```vue
<v-timeline>
  <v-timeline-item
    v-for="event in events"
    :key="event.id"
    :color="event.color"
    small
  >
    <template v-slot:opposite>
      <span :class="`headline font-weight-bold ${event.color}--text`">
        {{ event.date }}
      </span>
    </template>
    <v-card :color="event.color" dark>
      <v-card-title>{{ event.title }}</v-card-title>
      <v-card-text>{{ event.description }}</v-card-text>
    </v-card>
  </v-timeline-item>
</v-timeline>

<!-- Align left -->
<v-timeline align-left>
  <!-- items -->
</v-timeline>

<!-- Dense (no opposite) -->
<v-timeline dense>
  <!-- items -->
</v-timeline>
```

## Avatars

### v-avatar

Display avatars and profile images.

```vue
<!-- Basic avatar -->
<v-avatar size="48">
  <v-img src="avatar.jpg" />
</v-avatar>

<!-- With initials -->
<v-avatar color="primary" size="48">
  <span class="white--text headline">JD</span>
</v-avatar>

<!-- Avatar with status -->
<v-badge bordered bottom color="green" dot offset-x="10" offset-y="10">
  <v-avatar size="48">
    <v-img src="avatar.jpg" />
  </v-avatar>
</v-badge>

<!-- Avatar in list -->
<v-list-item-avatar>
  <v-img src="avatar.jpg" />
</v-list-item-avatar>
```

## Tooltips

### v-tooltip

Additional information on hover.

```vue
<v-tooltip bottom>
  <template v-slot:activator="{ on }">
    <v-btn icon v-on="on">
      <v-icon>mdi-help-circle</v-icon>
    </v-btn>
  </template>
  <span>Help text here</span>
</v-tooltip>

<!-- Tooltip on icon -->
<v-tooltip right>
  <template v-slot:activator="{ on }">
    <v-icon v-on="on">mdi-information</v-icon>
  </template>
  <span>More information</span>
</v-tooltip>
```

## See Also

- [Vuetify Data Tables](https://vuetifyjs.com/en/components/data-tables/)
- [Vuetify Cards](https://vuetifyjs.com/en/components/cards/)
- [Vuetify Lists](https://vuetifyjs.com/en/components/lists/)
- [Vuetify Expansion Panels](https://vuetifyjs.com/en/components/expansion-panels/)