# Common Patterns Templates

Ready-to-use code templates for frequent Vuetify V2 UI patterns.

## Page Layout

### Standard Page

```vue
<Page>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Page Title</h1>
      </v-col>
    </v-row>

    <!-- Content here -->
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Section Title</v-card-title>
          <v-card-text>Content</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Sidebar</v-card-title>
          <v-card-text>Sidebar content</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</Page>
```

### Dashboard Page

```vue
<Page>
  <v-container fluid>
    <!-- Stats Row -->
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-card>
          <v-card-text>
            <div class="text-overline">Stat 1</div>
            <div class="text-h4">{{ stat1 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card>
          <v-card-text>
            <div class="text-overline">Stat 2</div>
            <div class="text-h4">{{ stat2 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card>
          <v-card-text>
            <div class="text-overline">Stat 3</div>
            <div class="text-h4">{{ stat3 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card>
          <v-card-text>
            <div class="text-overline">Stat 4</div>
            <div class="text-h4">{{ stat4 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Main Content -->
    <v-row>
      <v-col cols="12" lg="8">
        <v-card>
          <v-card-title>Main Content</v-card-title>
          <v-card-text>
            <!-- Content here -->
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" lg="4">
        <v-card>
          <v-card-title>Sidebar</v-card-title>
          <v-card-text>
            <!-- Sidebar content -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</Page>
```

## CRUD Patterns

### List View

```vue
<Page>
  <v-container>
    <v-card>
      <v-card-title>
        <v-row align="center">
          <v-col>Items</v-col>
          <v-col cols="auto">
            <v-btn color="primary" @click="createItem">
              <v-icon left>mdi-plus</v-icon>
              New Item
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="items"
        :search="search"
        :loading="loading"
      >
        <template v-slot:top>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            class="mx-4"
          />
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="item.status === 'active' ? 'success' : 'error'" small>
            {{ item.status }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon small @click="edit(item)">
            <v-icon small>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon small @click="confirmDelete(item)">
            <v-icon small>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</Page>
```

### Edit Dialog

```vue
<v-dialog v-model="dialog" max-width="600">
  <v-card>
    <v-card-title>
      <span class="headline">{{ editedIndex === -1 ? 'New Item' : 'Edit Item' }}</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="editedItem.name"
          :rules="[v => !!v || 'Name is required']"
          label="Name"
        />
        <v-text-field
          v-model="editedItem.email"
          :rules="[v => /.+@.+\..+/.test(v) || 'Invalid email']"
          label="Email"
        />
        <v-select
          v-model="editedItem.status"
          :items="['active', 'inactive']"
          label="Status"
        />
      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn text @click="close">Cancel</v-btn>
      <v-btn color="primary" :disabled="!valid" @click="save">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

### Delete Confirmation

```vue
<v-dialog v-model="deleteDialog" max-width="400">
  <v-card>
    <v-card-title class="headline error--text">
      <v-icon left color="error">mdi-alert-circle</v-icon>
      Delete Item?
    </v-card-title>
    <v-card-text>
      This action cannot be undone. Are you sure you want to delete "{{ itemToDelete?.name }}"?
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="deleteDialog = false">Cancel</v-btn>
      <v-btn color="error" @click="deleteItem">Delete</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

## Form Patterns

### Login Form

```vue
<v-card max-width="400" class="mx-auto mt-8">
  <v-card-title class="justify-center">
    <h1 class="text-h5">Login</h1>
  </v-card-title>
  <v-card-text>
    <v-form ref="form" v-model="valid" @submit.prevent="login">
      <v-text-field
        v-model="email"
        :rules="emailRules"
        label="Email"
        prepend-icon="mdi-email"
        required
      />
      <v-text-field
        v-model="password"
        :rules="passwordRules"
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        label="Password"
        prepend-icon="mdi-lock"
        @click:append="showPassword = !showPassword"
        required
      />
      <v-checkbox v-model="remember" label="Remember me" />
      <v-btn type="submit" color="primary" block :disabled="!valid">
        Login
      </v-btn>
    </v-form>
  </v-card-text>
  <v-card-actions class="justify-center">
    <v-btn text to="/forgot-password">Forgot password?</v-btn>
  </v-card-actions>
</v-card>
```

### Settings Form

```vue
<v-card>
  <v-card-title>Settings</v-card-title>
  <v-card-text>
    <v-form>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="settings.name" label="Name" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="settings.email" label="Email" />
        </v-col>
      </v-row>

      <v-divider class="my-4" />

      <v-subheader>Notifications</v-subheader>
      <v-switch v-model="settings.emailNotifications" label="Email notifications" />
      <v-switch v-model="settings.pushNotifications" label="Push notifications" />

      <v-divider class="my-4" />

      <v-subheader>Appearance</v-subheader>
      <v-switch v-model="settings.darkMode" label="Dark mode" />
    </v-form>
  </v-card-text>
  <v-card-actions>
    <v-spacer />
    <v-btn text @click="reset">Reset</v-btn>
    <v-btn color="primary" @click="save">Save</v-btn>
  </v-card-actions>
</v-card>
```

## Filter Patterns

### Filter Panel

```vue
<v-card>
  <v-card-title>
    Filters
    <v-spacer />
    <v-btn text @click="resetFilters">Reset</v-btn>
  </v-card-title>
  <v-card-text>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.search"
          label="Search"
          clearable
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.status"
          :items="statusOptions"
          label="Status"
          clearable
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-menu
          v-model="dateMenu"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="filters.date"
              label="Date"
              prepend-icon="mdi-calendar"
              readonly
              v-on="on"
            />
          </template>
          <v-date-picker v-model="filters.date" @input="dateMenu = false" />
        </v-menu>
      </v-col>
    </v-row>
  </v-card-text>
</v-card>
```

### Active Filters Chips

```vue
<v-row v-if="activeFilters.length" class="mb-2">
  <v-chip
    v-for="filter in activeFilters"
    :key="filter.key"
    close
    class="mr-2"
    @click:close="removeFilter(filter.key)"
  >
    {{ filter.label }}: {{ filter.value }}
  </v-chip>
  <v-btn text small @click="clearFilters">Clear all</v-btn>
</v-row>
```

## Navigation Patterns

### Nested Menu

```vue
<v-navigation-drawer app v-model="drawer">
  <v-list dense>
    <v-list-item to="/" exact>
      <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-list-group prepend-icon="mdi-cog">
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item-content>
      </template>

      <v-list-item to="/settings/profile">
        <v-list-item-content>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item to="/settings/notifications">
        <v-list-item-content>
          <v-list-item-title>Notifications</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-group>
  </v-list>
</v-navigation-drawer>
```

## Empty States

### No Data

```vue
<v-card>
  <v-card-text>
    <v-row justify="center" align="center" class="py-8">
      <v-col cols="auto" class="text-center">
        <v-icon size="64" color="grey lighten-1">mdi-inbox</v-icon>
        <div class="text-h6 grey--text mt-4">No items found</div>
        <div class="text-body-2 grey--text">Add your first item to get started</div>
        <v-btn color="primary" class="mt-4" @click="create">
          <v-icon left>mdi-plus</v-icon>
          Add Item
        </v-btn>
      </v-col>
    </v-row>
  </v-card-text>
</v-card>
```

### Search No Results

```vue
<v-card>
  <v-card-text>
    <v-row justify="center" align="center" class="py-8">
      <v-col cols="auto" class="text-center">
        <v-icon size="64" color="grey lighten-1">mdi-magnify</v-icon>
        <div class="text-h6 grey--text mt-4">No results found</div>
        <div class="text-body-2 grey--text">Try adjusting your search or filters</div>
        <v-btn text class="mt-4" @click="clearSearch">Clear search</v-btn>
      </v-col>
    </v-row>
  </v-card-text>
</v-card>
```

## Loading States

### Skeleton Card

```vue
<v-card v-if="loading">
  <v-skeleton-loader type="image, card-heading, text, actions" />
</v-card>
<v-card v-else>
  <v-img :src="image" height="200" />
  <v-card-title>{{ title }}</v-card-title>
  <v-card-text>{{ description }}</v-card-text>
  <v-card-actions>
    <v-btn color="primary">Action</v-btn>
  </v-card-actions>
</v-card>
```

### Loading Overlay

```vue
<v-overlay :value="loading">
  <v-progress-circular indeterminate size="64" />
</v-overlay>
```

## Error Handling

### Error Alert

```vue
<v-alert
  v-if="error"
  type="error"
  dismissible
  @input="error = null"
>
  {{ error }}
</v-alert>
```

### Inline Error

```vue
<v-text-field
  v-model="field"
  :error="!!error"
  :error-messages="error"
  label="Field"
/>
```

## Integration with Baseweb

When using these patterns in Baseweb pages:

1. Wrap content in `<Page>` component
2. Use `Navigation.add()` to register pages
3. Use `$.ajax` for API calls
4. Use Vuex store modules for state
5. Clean up Socket.IO listeners in `beforeDestroy`

```javascript
const MyPage = {
  navigation: {
    section: "main",
    icon: "mdi-page",
    text: "My Page",
    path: "/my-page",
    index: 10
  },
  template: `
<Page>
  <!-- Content here -->
</Page>
  `,
  data() {
    return {
      items: [],
      loading: false,
      error: null
    };
  },
  mounted() {
    this.$vuetify.goTo(0);
    this.loadItems();
  },
  methods: {
    loadItems() {
      this.loading = true;
      $.ajax({
        url: "/api/items",
        success: (response) => {
          this.items = response.items;
          this.loading = false;
        },
        error: (xhr) => {
          this.error = xhr.responseText;
          this.loading = false;
        }
      });
    }
  }
};

Navigation.add(MyPage);
```