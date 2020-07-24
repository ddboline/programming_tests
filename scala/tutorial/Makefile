SCALAC = scalac

SCALA_FILES = $(shell ls *.scala | sed 's:.scala:.class:g')

%.class: %.scala
	$(SCALAC) $*.scala

all: $(SCALA_FILES)

clean:
	rm *.class
