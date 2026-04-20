-include ~/.claude/Makefile

# C3 Plugin Development
# Use --plugin-dir to test locally before releasing

local: ARGS=--plugin-dir ./
local: claude

SRC = $(PWD)

# Validate skills and agents structure
validate:
	@python bin/validate.py

# Validate plugin structure
validate-plugin:
	@claude plugin validate .

# Test plugin locally (overrides installed plugin)
test-plugin:
	@claude --plugin-dir $(SRC)

# Version management
version-current:
	@python bin/version.py current

version-bump-major:
	@python bin/version.py bump --part major

version-bump-minor:
	@python bin/version.py bump --part minor

version-bump-patch:
	@python bin/version.py bump --part patch

# Prepare release (bump version and update changelog)
release-major:
	@python bin/version.py release --part major

release-minor:
	@python bin/version.py release --part minor

release-patch:
	@python bin/version.py release --part patch

# Create git tag for current version
tag:
	@plugin_version=$$(python bin/version.py current | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'); \
	echo "Creating tag v$$plugin_version"; \
	git tag -a "v$$plugin_version" -m "Release $$plugin_version"; \
	echo "Tag created: v$$plugin_version"; \
	echo "Push with: git push origin v$$plugin_version"
