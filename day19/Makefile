CXXFLAGS += -Wall -Werror

all: optimized

optimized: CXXFLAGS += -O3
optimized: day19

debug: CXXFLAGS += -g3 -O0 -fsanitize=undefined
debug: day19

.PHONY: all optimized debug
