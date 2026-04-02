-include ~/.claude/Makefile

# Deployment: symlink everything in ~/.claude

SRC = $(PWD)
TRG = ~/.claude/

TOINSTALL=agents bin settings.json skills
SRCS=$(addprefix $(SRC)/,$(TOINSTALL))

install:
	ln -sF $(SRCS) $(TRG)
	ln -sF `pwd`/CLAUDE.global.md $(TRG)/CLAUDE.md
	ln -sF `pwd`/Makefile.claude $(TRG)/Makefile
