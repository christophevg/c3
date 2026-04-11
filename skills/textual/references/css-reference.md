# CSS Reference

Textual CSS syntax reference.

## Selectors

```css
/* Type selector - matches Python class name */
Button { }

/* ID selector */
#my-widget { }

/* Class selector */
.primary { }

/* Multiple classes */
.primary.large { }

/* Descendant combinator */
Container Button { }

/* Child combinator */
Container > Button { }

/* Pseudo-classes */
Button:focus { }
Button:hover { }
Button:disabled { }
Button:dark { }
Button:light { }
```

## Layout Properties

| Property | Values | Description |
|----------|--------|-------------|
| `layout` | `vertical`, `horizontal`, `grid` | Child arrangement |
| `dock` | `top`, `bottom`, `left`, `right` | Fixed position |
| `align` | `left/center/right top/middle/bottom` | Alignment |

## Grid Properties

| Property | Example | Description |
|----------|---------|-------------|
| `grid-size` | `3 4` | Columns and rows |
| `grid-columns` | `1fr 2fr 1fr` | Column sizes |
| `grid-rows` | `auto auto` | Row sizes |
| `grid-gutter` | `1` | Cell spacing |
| `column-span` | `2` | Span columns |
| `row-span` | `2` | Span rows |

## Dimension Properties

| Property | Example | Description |
|----------|---------|-------------|
| `width` | `20`, `50%`, `1fr` | Width |
| `height` | `10`, `50%` | Height |
| `min-width` | `10` | Minimum width |
| `max-width` | `100` | Maximum width |
| `min-height` | `5` | Minimum height |
| `max-height` | `50` | Maximum height |

## Units

| Unit | Example | Description |
|------|---------|-------------|
| Cells | `20` | Character columns/rows |
| Percentage | `50%` | Of parent |
| Viewport | `50vw`, `50vh` | Of terminal |
| Fractional | `1fr`, `2fr` | Flex ratio |
| Auto | `auto` | Fit content |

## Box Model

| Property | Example | Description |
|----------|---------|-------------|
| `padding` | `1`, `1 2`, `1 2 3 4` | Inner spacing |
| `margin` | `1` | Outer spacing |
| `border` | `solid red`, `heavy green` | Border style |
| `box-sizing` | `border-box`, `content-box` | Include border |

## Border Styles

```css
border: solid red;
border: heavy green;
border: double blue;
border: dashed yellow;
border: none;
border: hidden;
```

## Colors

| Format | Example |
|--------|---------|
| Named | `red`, `blue`, `green` |
| Hex | `#ff0000`, `#f00` |
| RGB | `rgb(255, 0, 0)` |

### Theme Colors

| Variable | Description |
|----------|-------------|
| `$primary` | Main color |
| `$secondary` | Secondary color |
| `$accent` | Accent color |
| `$foreground` | Text color |
| `$background` | Background color |
| `$surface` | Widget background |
| `$panel` | Panel background |
| `$error` | Error color |
| `$warning` | Warning color |
| `$success` | Success color |

### Color Shades

```css
background: $primary-lighten-1;
background: $primary-darken-2;
background: $error-muted;
```

## Text Properties

| Property | Values | Description |
|----------|--------|-------------|
| `color` | Color | Text color |
| `text-align` | `left`, `center`, `right` | Alignment |
| `text-style` | `bold`, `italic`, `underline` | Style |
| `text-wrap` | `wrap`, `nowrap`, `ellipsis` | Wrapping |

## Display Properties

| Property | Values | Description |
|----------|--------|-------------|
| `display` | `block`, `none` | Visibility |
| `visibility` | `visible`, `hidden` | Visibility |
| `opacity` | `0` to `1` | Transparency |

## Link Styles

```css
/* Hyperlinks in Markdown/Text */
link-color: blue;
link-color-hover: cyan;
link-background: transparent;
link-background-hover: yellow;
```

## Scrollbar Styles

```css
scrollbar-color: $primary;
scrollbar-color-hover: $accent;
scrollbar-background: $surface;
```

## Common Patterns

### Center Content

```css
Container {
  align: center middle;
}
```

### Dock Header/Footer

```css
#header {
  dock: top;
  height: 3;
}

#footer {
  dock: bottom;
  height: 1;
}
```

### Two-Column Layout

```css
Screen {
  layout: horizontal;
}

#left {
  width: 1fr;
}

#right {
  width: 2fr;
}
```

### Grid Dashboard

```css
Screen {
  layout: grid;
  grid-size: 3 2;
  grid-columns: 1fr 1fr 1fr;
  grid-rows: 2fr 1fr;
}
```

### Responsive (Dark/Light)

```css
Widget {
  background: $surface;
}

Widget:dark {
  color: white;
}

Widget:light {
  color: black;
}
```

## CSS Variables

```css
/* Define custom variables */
:root {
  --my-color: #ff0000;
}

/* Use variables */
Widget {
  background: var(--my-color);
}

/* Use theme variables */
Widget {
  color: $primary;
}
```

## @import

```css
/* Import another CSS file */
@import "other.tcss";

/* Import with glob pattern */
@import "widgets/*.tcss";
```