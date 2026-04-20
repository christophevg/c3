-include ~/.claude/Makefile

# Deployment: symlink individual files to ~/.claude
# This allows multiple sources to contribute skills/agents
# Alternative: install as plugin via marketplace

SRC = $(PWD)
TRG = $(HOME)/.claude

install: install-agents install-skills install-bin install-files

# Validate skills and agents structure
validate:
	@python bin/validate.py

# Validate plugin structure
validate-plugin:
	@claude plugin validate .

# Test plugin locally
test-plugin:
	@claude --plugin-dir $(SRC)

# Build plugin for distribution
build-plugin:
	@echo "Plugin ready for distribution via marketplace"
	@echo "Install with: claude plugin install c3@christophe.vg"

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

# Create target directories if they don't exist
$(TRG)/agents $(TRG)/skills $(TRG)/bin:
	mkdir -p $@

# Install individual agent files
install-agents: $(TRG)/agents
	@for agent in $(SRC)/agents/*.md; do \
		ln -sf $$agent $(TRG)/agents/; \
	done

# Install individual skill folders (each skill is a folder)
install-skills: $(TRG)/skills
	@for skill in $(SRC)/skills/*/; do \
		ln -sf $$skill $(TRG)/skills/; \
	done

# Install individual bin scripts
install-bin: $(TRG)/bin
	@for script in $(SRC)/bin/*; do \
		ln -sf $$script $(TRG)/bin/; \
	done

# Install root-level files
install-files:
	ln -sf $(SRC)/settings.json $(TRG)/
	ln -sf $(SRC)/CLAUDE.global.md $(TRG)/CLAUDE.md
	ln -sf $(SRC)/Makefile.claude $(TRG)/Makefile

# Uninstall: remove only symlinks pointing to this source
uninstall: uninstall-agents uninstall-skills uninstall-bin uninstall-files

uninstall-agents:
	@for agent in $(SRC)/agents/*.md; do \
		name=$$(basename $$agent); \
		target="$(TRG)/agents/$$name"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$agent" ]; then \
			rm "$$target"; \
		fi; \
	done

uninstall-skills:
	@for skill in $(SRC)/skills/*/; do \
		name=$$(basename "$$skill"); \
		target="$(TRG)/skills/$$name"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$skill" ]; then \
			rm "$$target"; \
		fi; \
	done

uninstall-bin:
	@for script in $(SRC)/bin/*; do \
		name=$$(basename "$$script"); \
		target="$(TRG)/bin/$$name"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$script" ]; then \
			rm "$$target"; \
		fi; \
	done

uninstall-files:
	@if [ -L "$(TRG)/settings.json" ] && [ "$$(readlink "$(TRG)/settings.json")" = "$(SRC)/settings.json" ]; then \
		rm "$(TRG)/settings.json"; \
	fi
	@if [ -L "$(TRG)/CLAUDE.md" ] && [ "$$(readlink "$(TRG)/CLAUDE.md")" = "$(SRC)/CLAUDE.global.md" ]; then \
		rm "$(TRG)/CLAUDE.md"; \
	fi
	@if [ -L "$(TRG)/Makefile" ] && [ "$$(readlink "$(TRG)/Makefile")" = "$(SRC)/Makefile.claude" ]; then \
		rm "$(TRG)/Makefile"; \
	fi
