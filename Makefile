MODEL ?= glm-5:cloud
ARGS ?=

all: claude

claude:
	ollama launch claude --model ${MODEL} -- $(ARGS)

update:
	claude --update

resume: ARGS=--resume
resume: claude

# Deployment: symlink everything in ~/.claude

SRC = $(PWD)
TRG = ~/.claude/

TOINSTALL=agents bin settings.json skills
SRCS=$(addprefix $(SRC)/,$(TOINSTALL))

install:
	ln -sF $(SRCS) $(TRG)
	ln -sF `pwd`/CLAUDE.global.md $(TRG)/CLAUDE.md
