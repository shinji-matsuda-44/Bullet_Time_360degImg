CC		= g++ -O3

CFLAGS          = -Wall \
		  `pkg-config --cflags eigen3`

LIBS            = -lm

DEST		= 

SRCS		= common.c \
		  getargs.c \
		  main.c \
		  calib.c

OBJS		= $(SRCS:.c=.o)

DOC		= README

CHANGELOG	= ChangeLog

PROGRAM		= calib_from_line

all:		$(PROGRAM)

$(PROGRAM):	$(OBJS) $(HDRS) 
		$(CC) $(OBJS) $(LDFLAGS) $(LIBS) -o $(PROGRAM)

clean:;		rm -f *.o *~ $(PROGRAM)

install:	$(PROGRAM)
		install -s $(PROGRAM) $(DEST)
		strip $(DEST)/$(PROGRAM)

###								End of Makefile
