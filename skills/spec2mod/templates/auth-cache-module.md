# Auth Cache Module Template

## auth_cache.py

```python
"""
Authentication cache for persisting and resuming sessions.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional, Any


class Token:
    """OAuth2 token data."""

    def __init__(
        self,
        access_token: str,
        expires_in: int,
        refresh_token: Optional[str] = None,
        token_type: str = "Bearer",
    ):
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.token_type = token_type

    def to_dict(self) -> dict[str, Any]:
        """Convert token to dictionary."""
        return {
            "access_token": self.access_token,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Token":
        """Create Token from dictionary."""
        return cls(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
        )


class AuthCache:
    """
    Manages persistent authentication cache.

    Stores tokens in a JSON file for session resumption across REPL restarts.
    """

    def __init__(self, cache_dir: Optional[Path] = None, package_name: str = "{{package_name}}"):
        """
        Initialize auth cache.

        Args:
            cache_dir: Directory for cache files (defaults to ~/.{package_name})
            package_name: Package name for default cache directory
        """
        self.cache_dir = cache_dir or (Path.home() / f".{package_name}")
        self.cache_file = self.cache_dir / "auth_cache.json"

    def _ensure_dir(self) -> None:
        """Ensure cache directory exists."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def save(self, token: Token) -> None:
        """
        Save token to cache.

        Args:
            token: Token to cache
        """
        self._ensure_dir()

        cache_data = token.to_dict()
        cache_data["saved_at"] = time.time()

        # Write with restricted permissions (600)
        self.cache_file.write_text(json.dumps(cache_data, indent=2))
        self.cache_file.chmod(0o600)

    def load(self) -> Optional[Token]:
        """
        Load token from cache.

        Returns:
            Cached Token or None if not found/invalid
        """
        if not self.cache_file.exists():
            return None

        try:
            data = json.loads(self.cache_file.read_text())

            # Check if token is still valid (with 5 minute buffer)
            saved_at = data.get("saved_at", 0)
            expires_in = data.get("expires_in", 0)
            age = time.time() - saved_at

            # Token expired?
            if age >= expires_in - 300:  # 5 minute buffer
                return None

            # Adjust expires_in to remaining time
            data["expires_in"] = int(expires_in - age)
            return Token.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def load_refresh_token(self) -> Optional[str]:
        """
        Load just the refresh token from cache.

        Returns:
            Cached refresh token or None
        """
        if not self.cache_file.exists():
            return None

        try:
            data = json.loads(self.cache_file.read_text())
            return data.get("refresh_token")
        except (json.JSONDecodeError, KeyError):
            return None

    def clear(self) -> None:
        """Clear the auth cache."""
        if self.cache_file.exists():
            self.cache_file.unlink()
```

## Template Variables

| Variable | Source |
|----------|---------|
| `{{package_name}}` | User-specified package name |