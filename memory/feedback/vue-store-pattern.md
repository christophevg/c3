# Vue Store Pattern for Global State

**Date**: 2026-05-14
**Context**: Roomz I2-001 - Magic link authentication

## Lesson Learned

**NEVER use `$root` for shared state in Vue applications.**

### The Problem

When implementing authentication in Roomz, I tried using `$root` to share state between components:

```javascript
// ❌ WRONG: Causes race conditions
// AuthDialog sets authenticated=true
this.$root.authenticated = true;

// Chat sets authenticated=false (overwrites AuthDialog!)
this.$root.authenticated = false;
```

This caused race conditions:
- Multiple components initialize `$root` at different times
- Last component to initialize wins
- State changes don't propagate reliably
- Vue 3 doesn't have `$set` (automatic reactivity)

### The Solution

Use a centralized store pattern:

```javascript
// store.js or inline
store.registerModule("auth", {
  state: { checking: true, session: null },
  getters: {
    checking: (state) => state.checking,
    session: (state) => state.session
  },
  actions: {
    setup_session: async (context) => {
      const response = await fetch("/auth/me");
      context.commit("session", await response.json());
    }
  },
  mutations: {
    session: (state, data) => { state.session = data; }
  }
});

// Initialize once on document ready
document.addEventListener("DOMContentLoaded", () => {
  store.dispatch("setup_session");
});
```

Components access via getters:

```javascript
computed: {
  authenticated() { return store.getters.session != null; },
  currentUser() { return store.getters.session?.user; }
}
```

### Key Principles

1. **Single source of truth** — Store owns the state
2. **Single initialization** — Initialize once on document ready
3. **Reactive getters** — Components use computed properties
4. **No `$root`** — Never use `$root` for shared state
5. **No `$set` in Vue 3** — Reactivity is automatic

### Vue 3 Reactivity

Vue 3 has automatic reactivity. Do NOT use `$set`:

```javascript
// ❌ WRONG: Vue 3 doesn't have $set
this.$set(this.$root, 'authenticated', true);

// ✅ CORRECT: Direct assignment works
this.$root.authenticated = true;  // Only for component local state
store.commit('authenticated', true);  // For shared state
```

## User Corrections from Session

**User said:**
- "I've manually debugged and cleaned up the codebase. You were making things very complex."
- "I basically introduced a 'store' for managing the session and could remove a lot of code."

**Why This Matters:**
- `$root` causes race conditions in multi-component apps
- Store pattern is the standard Vue solution for shared state
- Vue 3 reactivity is automatic, no `$set` needed

## Memory Impact

**Created new skill:**
- `/skills/vue/skill.md` — Vue component patterns including store pattern

**Added to vue skill:**
- Store pattern for global state
- Vue 3 reactivity (automatic)
- Common mistakes to avoid

**Project-specific memory:**
- Roomz uses store pattern for authentication state