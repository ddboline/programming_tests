package main

import (
	"golang.org/x/tour/wc"
	"strings"
)

func WordCount(s string) map[string]int {
	wordcount := make(map[string]int)
	for _, word := range strings.Fields(s) {
		wordcount[word]++
	}
	return wordcount
}

func main() {
	wc.Test(WordCount)
}
