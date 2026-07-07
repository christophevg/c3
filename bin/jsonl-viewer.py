#!/usr/bin/env python3
"""
JSONL Viewer for Claude Code session logs.

A less-like terminal viewer for browsing and searching Claude Code session logs
with rendered, human-readable output.

Usage:
  jsonl-viewer                    # Interactive session browser
  jsonl-viewer --search PATTERN   # Search across all sessions
  jsonl-viewer --help              # Show help
"""

import curses
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List


def find_claude_dir() -> Path:
  """Find the Claude Code configuration directory."""
  home = Path.home()
  claude_dir = home / ".claude"
  if not claude_dir.exists():
    raise FileNotFoundError(f"Claude directory not found: {claude_dir}")
  return claude_dir


def find_session_files(claude_dir: Path) -> list[dict]:
  """Find all session JSONL files with metadata."""
  projects_dir = claude_dir / "projects"
  if not projects_dir.exists():
    return []

  sessions = []

  for project_dir in projects_dir.iterdir():
    if not project_dir.is_dir():
      continue

    # Extract project name from directory
    project_name = project_dir.name
    if "-Users-xtof-Workspace-" in project_name:
      project_name = project_name.split("-Users-xtof-Workspace-", 1)[1]
    elif "-Users-" in project_name:
      project_name = project_name.split("-Users-", 1)[1]

    # Find main session files (not subagents)
    for jsonl_file in project_dir.glob("*.jsonl"):
      try:
        stat = jsonl_file.stat()
        sessions.append({
          'path': jsonl_file,
          'project': project_name,
          'session_id': jsonl_file.stem,
          'mtime': datetime.fromtimestamp(stat.st_mtime),
          'size': stat.st_size,
          'is_subagent': False,
        })
      except Exception:
        continue

  # Sort by modification time (newest first)
  sessions.sort(key=lambda s: s['mtime'], reverse=True)
  return sessions


def find_subagent_files(session_path: Path) -> list[dict]:
  """Find subagent JSONL files for a session."""
  # Session file is like: project/session-id.jsonl
  # Subagents are in: project/session-id/subagents/
  session_dir = session_path.parent / session_path.stem
  subagents_dir = session_dir / "subagents"

  if not subagents_dir.exists():
    return []

  subagents = []

  # Find all agent-*.jsonl files
  for jsonl_file in subagents_dir.glob("agent-*.jsonl"):
    try:
      # Read metadata if available
      meta_file = jsonl_file.with_suffix('.meta.json')
      if not meta_file.exists():
        # Try alternative naming: agent-xxx.jsonl -> agent-xxx.meta.json
        meta_file = jsonl_file.stem + '.meta.json'
        meta_file = subagents_dir / meta_file

      agent_type = "unknown"
      description = ""
      if meta_file.exists():
        try:
          with open(meta_file, 'r') as f:
            meta = json.load(f)
            agent_type = meta.get('agentType', 'unknown')
            description = meta.get('description', '')
        except Exception:
          pass

      stat = jsonl_file.stat()
      subagents.append({
        'path': jsonl_file,
        'project': session_path.stem,
        'session_id': jsonl_file.stem,
        'mtime': datetime.fromtimestamp(stat.st_mtime),
        'size': stat.st_size,
        'is_subagent': True,
        'agent_type': agent_type,
        'description': description,
      })
    except Exception:
      continue

  # Sort by modification time
  subagents.sort(key=lambda s: s['mtime'])
  return subagents


def count_messages(session_path: Path) -> int:
  """Count messages in a session file."""
  count = 0
  try:
    with open(session_path, 'r') as f:
      for line in f:
        line = line.strip()
        if line:
          count += 1
  except Exception:
    pass
  return count


def extract_messages(session_path: Path) -> list[dict]:
  """Extract messages from a session file."""
  messages = []

  try:
    with open(session_path, 'r') as f:
      for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line:
          continue

        try:
          entry = json.loads(line)
        except json.JSONDecodeError:
          continue

        # Extract message content
        message = parse_entry(entry, line_num)
        if message:
          messages.append(message)

  except Exception as e:
    messages.append({
      'line': line_num,
      'timestamp': None,
      'role': 'error',
      'content': f"Error reading file: {e}"
    })

  return messages


def parse_entry(entry: dict, line_num: int) -> Optional[dict]:
  """Parse a JSONL entry into a message."""

  # Get entry type
  entry_type = entry.get('type', 'unknown')
  subtype = entry.get('subtype')

  # Extract timestamp
  timestamp = entry.get('timestamp')
  if timestamp:
    try:
      if isinstance(timestamp, str):
        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        timestamp = ts.strftime('%H:%M:%S')
      else:
        timestamp = None
    except Exception:
      timestamp = None

  # Handle different entry types
  if entry_type == 'user':
    # User message
    message = entry.get('message', {})
    content = None

    if isinstance(message, dict):
      content = message.get('content', '')
      # Content blocks
      if isinstance(content, list):
        parts = []
        for item in content:
          if isinstance(item, dict):
            if item.get('type') == 'text':
              parts.append(item.get('text', ''))
            elif item.get('type') == 'tool_result':
              tool_id = item.get('tool_use_id', 'unknown')
              result = item.get('content', '')
              if isinstance(result, list):
                result = '\n'.join(str(r) for r in result[:3])
              parts.append(f"[Tool Result: {tool_id}]\n{str(result)[:500]}")
        content = '\n'.join(parts) if parts else str(content)
    elif isinstance(message, str):
      content = message

    return {
      'line': line_num,
      'timestamp': timestamp,
      'role': 'user',
      'content': content or '',
    }

  elif entry_type == 'assistant':
    # Assistant response
    message = entry.get('message', {})
    content_parts = []

    if isinstance(message, dict):
      content = message.get('content', [])
      if isinstance(content, list):
        for item in content:
          if isinstance(item, dict):
            item_type = item.get('type')
            if item_type == 'text':
              content_parts.append(item.get('text', ''))
            elif item_type == 'thinking':
              thinking = item.get('thinking', '')
              content_parts.append(f"[Thinking]\n{thinking}")
            elif item_type == 'tool_use':
              tool_name = item.get('name', 'unknown')
              tool_input = item.get('input', {})
              # Format tool input
              if isinstance(tool_input, dict) and len(tool_input) > 0:
                input_str = json.dumps(tool_input, indent=2)
                if len(input_str) > 300:
                  input_str = input_str[:300] + '...'
              else:
                input_str = '{}'
              content_parts.append(f"[Tool: {tool_name}]\n{input_str}")
          elif isinstance(item, str):
            content_parts.append(item)
      elif isinstance(content, str):
        content_parts.append(content)
    elif isinstance(message, str):
      content_parts.append(message)

    return {
      'line': line_num,
      'timestamp': timestamp,
      'role': 'assistant',
      'content': '\n'.join(content_parts) if content_parts else '',
    }

  elif entry_type == 'system':
    # System metadata entries
    if subtype == 'turn_duration':
      duration = entry.get('durationMs', 0)
      msg_count = entry.get('messageCount', 0)
      pending = entry.get('pendingBackgroundAgentCount', 0)
      return {
        'line': line_num,
        'timestamp': timestamp,
        'role': 'system',
        'content': f"Turn: {duration}ms, {msg_count} messages" + (f", {pending} pending agents" if pending else ""),
      }
    elif subtype == 'compact_boundary':
      return {
        'line': line_num,
        'timestamp': timestamp,
        'role': 'system',
        'content': "--- Context Compacted ---",
      }
    else:
      # Generic system entry
      return {
        'line': line_num,
        'timestamp': timestamp,
        'role': 'system',
        'content': f"System: {subtype or 'unknown'}",
      }

  elif entry_type == 'agent-setting':
    agent_name = entry.get('agentSetting', 'unknown')
    return {
      'line': line_num,
      'timestamp': timestamp,
      'role': 'agent',
      'content': f"Agent: {agent_name}",
    }

  elif entry_type == 'mode':
    mode = entry.get('mode', 'unknown')
    return {
      'line': line_num,
      'timestamp': timestamp,
      'role': 'config',
      'content': f"Mode: {mode}",
    }

  elif entry_type == 'permission-mode':
    perm = entry.get('permissionMode', 'unknown')
    return {
      'line': line_num,
      'timestamp': timestamp,
      'role': 'config',
      'content': f"Permission: {perm}",
    }

  elif entry_type == 'attachment':
    attachment = entry.get('attachment', {})
    att_type = attachment.get('type', 'unknown')

    if att_type == 'agent_listing_delta':
      # Agent listing - show available agents
      agents = attachment.get('addedTypes', [])
      lines = attachment.get('addedLines', [])
      if lines:
        # Show first few agents as summary
        summary = f"Available Agents ({len(agents)} total)"
        content = summary + "\n\n" + "\n".join(lines[:5])
        if len(lines) > 5:
          content += f"\n... and {len(lines) - 5} more"
        return {
          'line': line_num,
          'timestamp': timestamp,
          'role': 'agents',
          'content': content,
        }
    elif att_type == 'skill_listing':
      # Skill listing - show available skills
      content = attachment.get('content', '')
      if content:
        # Count skills
        skill_count = attachment.get('skillCount', 0)
        summary = f"Available Skills ({skill_count} total)"
        # Show first few skills
        skill_lines = content.split('\n')[:5]
        content = summary + "\n\n" + "\n".join(skill_lines)
        if len(content) > 500:
          content = content[:500] + "\n... (truncated)"
        return {
          'line': line_num,
          'timestamp': timestamp,
          'role': 'skills',
          'content': content,
        }
    elif att_type == 'command_permissions':
      # Command permissions
      allowed = attachment.get('allowedTools', [])
      return {
        'line': line_num,
        'timestamp': timestamp,
        'role': 'config',
        'content': f"Allowed Tools: {len(allowed)} tools",
      }
    # Skip other attachment types
    return None

  # Skip pure metadata entries (no content to display)
  elif entry_type in ('file-history-snapshot', 'ai-title', 'last-prompt', 'queue-operation'):
    return None

  return None


class SessionViewer:
  """Curses-based viewer for JSONL sessions with less-like navigation."""

  def __init__(self, sessions: List[dict]):
    self.sessions = sessions
    self.current_session_idx = None
    self.search_pattern = None

  def run(self):
    """Run the curses application."""
    curses.wrapper(self._run_curses)

  def _run_curses(self, stdscr):
    """Main curses loop."""
    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_CYAN, -1)
    curses.init_pair(8, curses.COLOR_WHITE, -1)  # Gray (white on default bg)

    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable special keys

    while True:
      if self.current_session_idx is None:
        # Show overview
        action = self._show_overview(stdscr)
        if action == 'quit':
          break
        elif action == 'select':
          continue  # current_session_idx is set
      else:
        # Show session
        action = self._show_session(stdscr)
        if action == 'quit':
          break
        elif action == 'back':
          self.current_session_idx = None
          self.search_pattern = None

  def _show_overview(self, stdscr) -> str:
    """Show session overview. Returns 'quit', 'select', or 'search'."""
    height, width = stdscr.getmaxyx()
    offset = 0
    selected = 0

    while True:
      stdscr.clear()

      # Header
      header = "CLAUDE CODE SESSION BROWSER"
      stdscr.addstr(0, 0, "=" * width)
      stdscr.addstr(1, (width - len(header)) // 2, header)
      stdscr.addstr(2, 0, "=" * width)

      # Column headers
      col_header = f"{'#':<4} {'Session':<36} {'Project':<20} {'Time':<12} {'Messages':<10}"
      stdscr.addstr(3, 0, col_header)
      stdscr.addstr(4, 0, "-" * width)

      # Sessions
      max_rows = height - 8
      for i, session in enumerate(self.sessions[offset:offset + max_rows]):
        row = i + 5
        session_id = session['session_id'][:36]
        project = session['project'][:20]
        time_str = session['mtime'].strftime('%Y-%m-%d %H:%M')
        msg_count = count_messages(session['path'])

        line = f"{offset + i + 1:<4} {session_id:<36} {project:<20} {time_str:<12} {msg_count:<10}"

        # Highlight selected
        if offset + i == selected:
          stdscr.attron(curses.A_REVERSE)
          stdscr.addstr(row, 0, line[:width])
          stdscr.attroff(curses.A_REVERSE)
        else:
          stdscr.addstr(row, 0, line[:width])

      # Footer
      footer = f"Total: {len(self.sessions)} sessions | ↑↓ navigate | Enter select | / search | q quit"
      stdscr.addstr(height - 2, 0, "-" * width)
      stdscr.addstr(height - 1, 0, footer[:width])

      stdscr.refresh()

      # Handle input
      key = stdscr.getch()

      if key == ord('q'):
        return 'quit'
      elif key == curses.KEY_UP:
        selected = max(0, selected - 1)
        if selected < offset:
          offset = selected
      elif key == curses.KEY_DOWN:
        selected = min(len(self.sessions) - 1, selected + 1)
        if selected >= offset + max_rows:
          offset = selected - max_rows + 1
      elif key == ord('\n') or key == curses.KEY_ENTER:
        if 0 <= selected < len(self.sessions):
          self.current_session_idx = selected
          return 'select'
      elif key == ord('/'):
        # Search
        pattern = self._get_input(stdscr, "Search: ")
        if pattern:
          self._global_search(stdscr, pattern)
        # Stay in overview after search

    return 'quit'

  def _show_session(self, stdscr) -> str:
    """Show session messages with less-like scrolling. Returns 'quit', 'back', or 'select'."""
    height, width = stdscr.getmaxyx()
    session = self.sessions[self.current_session_idx]

    # Load main session messages
    all_messages = extract_messages(session['path'])

    # Load subagent messages
    subagents = find_subagent_files(session['path'])
    subagent_messages = []
    for subagent in subagents:
      # Add subagent header
      subagent_messages.append({
        'timestamp': None,
        'role': 'subagent',
        'content': f"--- Subagent: {subagent['agent_type']} ---\n{subagent['description']}",
      })
      # Load subagent messages
      subagent_msgs = extract_messages(subagent['path'])
      subagent_messages.extend(subagent_msgs)

    # Combine main session + subagents
    if subagent_messages:
      all_messages.extend(subagent_messages)

    # Apply search filter if active
    if self.search_pattern:
      regex = re.compile(self.search_pattern, re.IGNORECASE)
      messages = [m for m in all_messages if regex.search(m.get('content', ''))]
    else:
      messages = all_messages

    # Build display lines (each message can be multiple lines)
    lines = []
    line_to_msg = []  # Map line index to message index

    # Role colors (using curses color pairs)
    role_colors = {
      'user': 6,       # Cyan
      'assistant': 5,  # Magenta
      'thinking': 4,   # Blue
      'system': 8,     # Gray/dim
      'tool': 3,       # Yellow
      'tool_result': 2, # Green
      'agent': 3,      # Yellow (agent-setting)
      'config': 8,     # Gray (mode, permission-mode)
      'subagent': 1,   # Red (subagent header)
      'agents': 4,     # Blue (agent listing)
      'skills': 4,     # Blue (skill listing)
    }

    for msg_idx, msg in enumerate(messages):
      timestamp = msg.get('timestamp', '??:??:??')
      role = msg.get('role', 'unknown')
      content = msg.get('content', '')
      color = role_colors.get(role, 0)

      # Format header line
      header = f"{timestamp} [{role}]"
      lines.append((header, color, msg_idx))
      line_to_msg.append(msg_idx)

      # Content lines
      for content_line in content.split('\n'):
        lines.append((content_line, 0, msg_idx))
        line_to_msg.append(msg_idx)

      # Blank line between messages
      lines.append(('', 0, msg_idx))
      line_to_msg.append(msg_idx)

    offset = 0

    while True:
      stdscr.clear()

      # Header
      session_id = session['session_id'][:36]
      project = session['project'][:20]

      if self.search_pattern:
        header = f"Session: {session_id} ({project}) - {len(messages)}/{len(all_messages)} matches for '{self.search_pattern}'"
      else:
        header = f"Session: {session_id} ({project}) - {len(messages)} messages"
      stdscr.addstr(0, 0, "=" * width)
      stdscr.addstr(1, (width - len(header)) // 2, header[:width])
      stdscr.addstr(2, 0, "=" * width)

      # Messages
      max_rows = height - 5
      for i, (line_text, color, msg_idx) in enumerate(lines[offset:offset + max_rows]):
        row = i + 3
        try:
          if color > 0:
            stdscr.attron(curses.color_pair(color))
            stdscr.addstr(row, 0, line_text[:width])
            stdscr.attroff(curses.color_pair(color))
          else:
            stdscr.addstr(row, 0, line_text[:width])
        except curses.error:
          pass  # Ignore edge case at end of screen

      # Footer
      footer_line = height - 2
      if offset + max_rows >= len(lines):
        footer = "(END) | ↑↓/j/k scroll | Space/b page | g/G start/end | / search | n/p next/prev | b back | q quit"
      else:
        footer = f"-- More -- ({offset + max_rows}/{len(lines)}) | ↑↓/j/k scroll | Space/b page | / search | b back | q quit"

      stdscr.addstr(footer_line, 0, "-" * width)
      stdscr.addstr(footer_line + 1, 0, footer[:width])

      stdscr.refresh()

      # Handle input
      key = stdscr.getch()

      if key == ord('q'):
        return 'quit'
      elif key == ord('b'):
        return 'back'
      elif key == curses.KEY_UP or key == ord('k'):
        offset = max(0, offset - 1)
      elif key == curses.KEY_DOWN or key == ord('j'):
        offset = min(max(0, len(lines) - max_rows), offset + 1)
      elif key == ord(' '):  # Page down
        offset = min(max(0, len(lines) - max_rows), offset + max_rows)
      elif key == curses.KEY_PPAGE:  # Page up
        offset = max(0, offset - max_rows)
      elif key == ord('g'):  # Go to start
        offset = 0
      elif key == ord('G'):  # Go to end
        offset = max(0, len(lines) - max_rows)
      elif key == ord('/'):
        # Search
        pattern = self._get_input(stdscr, "Search: ")
        if pattern:
          self.search_pattern = pattern
          return 'back'  # Will re-filter and show
      elif key == ord('n') and self.search_pattern:
        # Next match
        regex = re.compile(self.search_pattern, re.IGNORECASE)
        current_msg = line_to_msg[offset] if offset < len(line_to_msg) else 0
        for i in range(current_msg + 1, len(messages)):
          if regex.search(messages[i].get('content', '')):
            # Find line index for this message
            for line_idx, (text, color, midx) in enumerate(lines):
              if midx == i:
                offset = line_idx
                break
            break
      elif key == ord('p') and self.search_pattern:
        # Previous match
        regex = re.compile(self.search_pattern, re.IGNORECASE)
        current_msg = line_to_msg[offset] if offset < len(line_to_msg) else 0
        for i in range(current_msg - 1, -1, -1):
          if regex.search(messages[i].get('content', '')):
            # Find line index for this message
            for line_idx, (text, color, midx) in enumerate(lines):
              if midx == i:
                offset = line_idx
                break
            break

    return 'back'

  def _get_input(self, stdscr, prompt: str) -> str:
    """Get text input from user."""
    height, width = stdscr.getmaxyx()

    # Show prompt
    curses.echo()
    curses.curs_set(1)

    stdscr.move(height - 1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(height - 1, 0, prompt)

    # Get input
    input_win = curses.newwin(1, width - len(prompt), height - 1, len(prompt))
    input_win.keypad(True)

    text = ""
    while True:
      key = input_win.getch()
      if key == ord('\n') or key == curses.KEY_ENTER:
        break
      elif key == 27:  # Escape
        text = ""
        break
      elif key == curses.KEY_BACKSPACE or key == 127:
        text = text[:-1]
        input_win.move(0, len(text))
        input_win.clrtoeol()
      elif 32 <= key <= 126:  # Printable chars
        text += chr(key)
        input_win.addch(chr(key))

    curses.noecho()
    curses.curs_set(0)
    return text

  def _global_search(self, stdscr, pattern: str):
    """Search across all sessions and show results."""
    height, width = stdscr.getmaxyx()
    regex = re.compile(pattern, re.IGNORECASE)

    results = []
    for session in self.sessions:
      # Include subagents in search
      all_messages = extract_messages(session['path'])
      subagents = find_subagent_files(session['path'])
      for subagent in subagents:
        all_messages.append({
          'timestamp': None,
          'role': 'subagent',
          'content': f"--- Subagent: {subagent['agent_type']} ---\n{subagent['description']}",
        })
        all_messages.extend(extract_messages(subagent['path']))

      matches = [m for m in all_messages if regex.search(m.get('content', ''))]
      if matches:
        results.append((session, matches))

    # Display results
    offset = 0
    selected = 0
    while True:
      stdscr.clear()

      header = f"Search results for '{pattern}' - {len(results)} sessions"
      stdscr.addstr(0, 0, "=" * width)
      stdscr.addstr(1, (width - len(header)) // 2, header[:width])
      stdscr.addstr(2, 0, "=" * width)

      max_rows = height - 5
      for i, (session, matches) in enumerate(results[offset:offset + max_rows]):
        row = i + 3
        session_id = session['session_id'][:36]
        project = session['project'][:20]
        line = f"{offset + i + 1:<4} {session_id:<36} {project:<20} {len(matches)} matches"

        # Highlight selected
        if offset + i == selected:
          stdscr.attron(curses.A_REVERSE)
          stdscr.addstr(row, 0, line[:width])
          stdscr.attroff(curses.A_REVERSE)
        else:
          stdscr.addstr(row, 0, line[:width])

      footer = "↑↓ navigate | Enter select | Esc back"
      stdscr.addstr(height - 2, 0, "-" * width)
      stdscr.addstr(height - 1, 0, footer[:width])

      stdscr.refresh()

      key = stdscr.getch()
      if key == 27:  # Escape
        break
      elif key == curses.KEY_UP:
        selected = max(0, selected - 1)
        if selected < offset:
          offset = selected
      elif key == curses.KEY_DOWN:
        selected = min(len(results) - 1, selected + 1)
        if selected >= offset + max_rows:
          offset = selected - max_rows + 1
      elif key == ord('\n') or key == curses.KEY_ENTER:
        # Select session
        for i, s in enumerate(self.sessions):
          if s['path'] == results[selected][0]['path']:
            self.current_session_idx = i
            self.search_pattern = pattern
            break
        break


def interactive_mode(sessions: list[dict]):
  """Run interactive session browser."""
  viewer = SessionViewer(sessions)
  viewer.run()


def main():
  """Main entry point."""
  import argparse

  parser = argparse.ArgumentParser(
    description='JSONL Viewer for Claude Code session logs',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Navigation (Overview):
  ↑/↓         Navigate sessions
  Enter       Select session
  /           Search across sessions
  q           Quit

Navigation (Session):
  ↑/↓ or j/k  Scroll one line
  Space       Page down
  b           Page up
  g           Go to start
  G           Go to end
  /           Search within session
  n           Next match (when searching)
  p           Previous match (when searching)
  b           Back to overview
  q           Quit
"""
  )
  parser.add_argument('--search', '-s', metavar='PATTERN', help='Search across all sessions')
  parser.add_argument('--project', '-p', metavar='NAME', help='Filter by project name')
  parser.add_argument('--last', '-n', type=int, metavar='N', help='Show only last N sessions')

  args = parser.parse_args()

  try:
    claude_dir = find_claude_dir()
    sessions = find_session_files(claude_dir)

    # Filter by project
    if args.project:
      sessions = [s for s in sessions if args.project.lower() in s['project'].lower()]

    # Filter by count
    if args.last:
      sessions = sessions[:args.last]

    # Search mode
    if args.search:
      print(f"Searching for '{args.search}' across {len(sessions)} sessions...")
      pattern = re.compile(args.search, re.IGNORECASE)

      for session in sessions:
        # Include subagents in search
        all_messages = extract_messages(session['path'])
        subagents = find_subagent_files(session['path'])
        for subagent in subagents:
          all_messages.append({
            'timestamp': None,
            'role': 'subagent',
            'content': f"--- Subagent: {subagent['agent_type']} ---\n{subagent['description']}",
          })
          all_messages.extend(extract_messages(subagent['path']))

        matches = [m for m in all_messages if pattern.search(m.get('content', ''))]

        if matches:
          print(f"\n{session['path']}")
          print(f"  Project: {session['project']}")
          print(f"  Matches: {len(matches)}")
          for m in matches[:5]:  # Show first 5 matches
            print(f"  - [{m['role']}] {m['content'][:100]}...")

      return

    # Interactive mode
    if not sessions:
      print("No sessions found.")
      return

    interactive_mode(sessions)

  except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)
  except KeyboardInterrupt:
    print("\nGoodbye!")
    sys.exit(0)


if __name__ == "__main__":
  main()