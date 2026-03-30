SRC = $(PWD)
TRG = ~/.claude/

TOINSTALL=agents bin settings.json skills
SRCS=$(addprefix $(SRC)/,$(TOINSTALL))

MODEL ?= glm-5:cloud

# symlink everything in ~/.claude
install:
	ln -sF $(SRCS) $(TRG)
	ln -sF CLAUDE.global.md $(TRG)

claude: update-claude
	ollama launch claude --model ${MODEL}

update-claude:
	brew upgrade claude-code
