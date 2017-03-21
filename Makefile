SRCS=$(wildcard *.c)
OBJS=$(SRCS:.c=.o)
all: ${EXEC} $(OBJS)
clean:
	rm *.o
