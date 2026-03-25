SRC = $(PWD)
TRG = ~/.claude/

TOINSTALL=agents bin settings.json skills
SRCS=$(addprefix $(SRC)/,$(TOINSTALL))

install:
	ln -sF $(SRCS) $(TRG)
