CC = g++
CXXFLAGS = -O3 -ansi
LDFLAGS = -lm
TARGET = boolop
OBJS = polygon.o utilities.o main.o booleanop.o

$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) $(LDFLAGS)

booleanop.o: booleanop.cpp booleanop.h polygon.h utilities.h point.h bbox.h segment.h

main.o: main.cpp booleanop.h polygon.h utilities.h point.h bbox.h segment.h

polygon.o: polygon.cpp polygon.h utilities.h point.h bbox.h segment.h

utilities.o: utilities.cpp utilities.h point.h bbox.h segment.h

clean:
	rm $(TARGET) $(OBJS) *~
