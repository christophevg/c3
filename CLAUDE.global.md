# Global Claude Code Instructions

These instructions are mandatory for all agents!

## Hello

Hello, I'm your operator. My name is Christophe Van Ginneken, often used in a shorter format as Christophe VG and my username is often xtof (e.g. local account) or christophevg (e.g. GitHub).

I have a website hosted on https://christophe.vg It contains information about me and the things I like, like sailing, cooking, taking photographs, technology,...

You can find projects I work on in `~/Workspace`. The most important ones of use to you include:

### `~/Workspace/agentic/c3`

This is a **Claude Code configuration harness** that provides reusable skills, agents, and settings for Python/Baseweb development projects. The configuration is designed to be symlinked into `~/.claude/` for use across multiple projects.

### `~/Workspace/agentic/incubator`

A personal agentic incubator for brainstorming, researching ideas, developing prototypes, and creating/training skills and agents.

### `~/Workspace/agentic/christophe.vg`

This repository holds my personal website, which is hosted on GitHub Pages, powered by Jekyll and styled using Minimal Mistakes. And since recently crafted together with a coding agent (you) and a nice model.

## Personal Goals

You are encouraged to help me in reaching my goals throughout the different projects we will work on.

In relation to coding agents I...

* ...want to create a collection of reusable skills, agents and tools to automate and support brainstorming, analyzing, designing, implementing and running of my project.
* ...want my coding agent to build and evolve its skills and agents by itself, a concept I consider self-learning. I only want to guide, not write skill, agent, tool definitions myself.

This way I want to create a conglomerate agent that "acts" like me, yet faster, better, more consistent, allowing me to focus on the core content.

## Best Practices to Strictly Follow

### Tool & Agent Usage

**VERY IMPORTANT**:
* You MUST avoid using the Bash tool for search commands like find and grep. Instead use Grep, Glob, or Task to search.
* You MUST use the `researcher agent` for all research.

### Agent Session Continuity

**CRITICAL**: When conducting multi-turn interactions with agents (interviews, analysis, research):

1. **Launch agent once** - Use the Agent tool to start the interaction
2. **Continue with SendMessage** - After the agent responds, use `SendMessage` with the agent ID to continue
3. **Never restart mid-conversation** - Do NOT launch a new Agent for follow-up questions

**Why**: Launching new agents between questions loses context, causes duplicate questions, and fragments analysis.

**Example**:
```
# Launch functional-analyst for interview
→ Agent responds with: agentId: abc123

# User answers question
→ Use SendMessage to: abc123 (NOT new Agent)

# Continue conversation...
→ Use SendMessage to: abc123
```

### Task → Skill/Agent Mapping

When the user asks you to work on a task, select the appropriate tool:

| Task Type | Use |
|-----------|-----|
| Analyze requirements, gather requirements, interview user | functional-analyst agent |
| Research a topic, investigate, gather information | researcher agent |
| Review code for quality, best practices | code-reviewer agent |
| Create Python code | python-developer agent |
| Learn from session, improve skills | lessons-learned skill |
| Commit changes | commit skill (/commit)

### Information Gathering

* If available, consult AGENTS.md

### Planning and Explaining

* Always begin with an overview of your plan
* Always explain your actions before executing them.

### Style and Formatting

* Always use two spaces for indentation in all file types.

### When Working in a Code-Driven Project

* Always write tests for new functionality and integrate them into the `tests` directory.
* Ensure that all tests are working at all times.
* Maintain test coverage.
* Ensure that every exception in the backend code is captured gracefully and reported back to the client in a human readable format. Also log the problem with context.

### Things to Ignore

* Ignore the `local` folder.
* Ignore files with `.local` extension.
* Ignore the `notes` folder.

### Basic Workflow

* Continue working on unchecked tasks from the `TODO.md` file in a top-down manner. Treat each task as the next prompt to process. Cross the Markdown checkbox when a task is completed and move it to the bottom of the file. At the end of each task, request a review before proceeding to the next task.
