YOKER_FROM = ../yoker
-include Makefile.yoker

install: $(HOME)/.yoker/Makefile $(HOME)/.yoker/AGENTS.md ## Install a Yoker supporting Makefile and global AGENTS.md

$(HOME)/.yoker/Makefile: Makefile.yoker
	@echo "Installing $< in $@"
	@mkdir -p $(HOME)/.yoker
	@ln -sf $(realpath $<) $@

$(HOME)/.yoker/AGENTS.md: AGENTS.global.md
	@echo "Installing $< in $@"
	@mkdir -p $(HOME)/.yoker
	@ln -sf $(realpath $<) $@


# Validate skills and agents structure
$(HOME)/.yoker/AGENTS.md: AGENTS.global.md
	@echo "Installing $< in $@"
	@mkdir -p $(HOME)/.yoker
	@ln -sf $(realpath $<) $@

# Validate skills and agents structure
validate:
	@uv run python bin/validate.py
