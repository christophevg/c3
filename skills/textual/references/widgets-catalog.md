# Widgets Catalog

Complete catalog of Textual widgets (35+ widgets).

## Core Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `Static` | Base for custom widgets | `content`, `expand`, `shrink`, `markup` |
| `Label` | Simple text display | Inherits from Static |
| `Button` | Clickable button | `label`, `variant` (default/primary/success/warning/error) |
| `Input` | Single-line text input | `value`, `placeholder`, `password`, `validators` |
| `Checkbox` | Boolean toggle | `value` |

## Data Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `DataTable` | Tabular data | `cursor_type`, `zebra_stripes`, `fixed_rows`, `fixed_columns` |
| `ListView` | Selectable list | `initial_index` |
| `ListItem` | List item container | - |
| `Tree` | Hierarchical data | `show_root`, `show_guides` |
| `DirectoryTree` | File system browser | `path` |

## Input Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `Input` | Text input | `placeholder`, `validators`, `restrict` |
| `TextArea` | Multi-line text | `language`, `soft_wrap`, `read_only` |
| `Select` | Dropdown | `options` as (display, value) tuples |
| `Checkbox` | Boolean | `value` |

## Layout Widgets

| Widget | Purpose |
|--------|---------|
| `Container` | Simple vertical container |
| `Vertical` | Expanding vertical, no scroll |
| `Horizontal` | Expanding horizontal, no scroll |
| `VerticalScroll` | Vertical with scrollbar |
| `HorizontalScroll` | Horizontal with scrollbar |
| `Grid` | Grid layout |
| `Center` | Center horizontally |
| `Middle` | Center vertically |
| `CenterMiddle` | Center both axes |
| `Right` | Align right |

## Navigation Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `Header` | App title at top | Auto-managed |
| `Footer` | Key bindings at bottom | Auto-managed |
| `TabbedContent` | Tab container | `initial`, `active` |
| `TabPane` | Tab content | `title` |
| `Tabs` | Tab bar only | - |

## Content Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `Markdown` | Markdown rendering | `markdown`, `open_links` |
| `Syntax` | Code highlighting | (from Rich) |
| `Collapsible` | Expandable section | `title`, `collapsed` |

## Progress Widgets

| Widget | Purpose | Key Parameters |
|--------|---------|----------------|
| `ProgressBar` | Progress indicator | `total`, `progress`, `show_eta` |
| `LoadingIndicator` | Loading spinner | - |

## Button Variants

```python
Button("Default")           # Default style
Button("Primary", variant="primary")     # Highlighted
Button("Success", variant="success")     # Green
Button("Warning", variant="warning")     # Yellow
Button("Error", variant="error")         # Red
```

## DataTable Methods

| Method | Description |
|--------|-------------|
| `add_column(label)` | Add column, returns ColumnKey |
| `add_row(*cells)` | Add row, returns RowKey |
| `clear()` | Clear all data |
| `get_cell(row, col)` | Get cell value |
| `update_cell(row, col, value)` | Update cell |
| `remove_row(row)` | Remove row |
| `remove_column(col)` | Remove column |

## Tree Methods

| Method | Description |
|--------|-------------|
| `root.add(label)` | Add expandable node |
| `root.add_leaf(label)` | Add leaf node |
| `root.expand()` | Expand node |
| `root.collapse()` | Collapse node |
| `root.remove()` | Remove node |

## ListView Methods

| Method | Description |
|--------|-------------|
| `append(item)` | Add to end |
| `insert(index, items)` | Insert at index |
| `pop(index)` | Remove by index |
| `clear()` | Clear all |

## Select Options Format

```python
Select([
  ("Display Text", "value1"),
  ("Option 2", "value2"),
], allow_blank=True)
```

## Widget Focus

```python
# Focusable widgets
can_focus = True

# Focus control
widget.focus()
widget.blur()

# Check focus
widget.has_focus
```

## Common Messages

| Widget | Message | Handler |
|--------|---------|---------|
| `Button` | `Button.Pressed` | `on_button_pressed` |
| `Input` | `Input.Changed` | `on_input_changed` |
| `Input` | `Input.Submitted` | `on_input_submitted` |
| `DataTable` | `DataTable.RowSelected` | `on_data_table_row_selected` |
| `ListView` | `ListView.Selected` | `on_list_view_selected` |
| `Tree` | `Tree.NodeSelected` | `on_tree_node_selected` |
| `Select` | `Select.Changed` | `on_select_changed` |