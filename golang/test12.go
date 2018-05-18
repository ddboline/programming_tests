package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

type rot13Reader struct {
	r io.Reader
}

func (v *rot13Reader) Read(b []byte) (n int, e error) {
	tot := 0
	n, err := v.r.Read(b)
	if err != nil {
		return 0, err
	}
	for i, b_ := range b {
		if b_ >= 'a' && b_ <= 'z' {
			b[i] = (b_+13-'a')%26 + 'a'
		} else if b_ >= 'A' && b_ <= 'Z' {
			b[i] = (b_+13-'A')%26 + 'A'
		}
	}
	tot += n
	return tot, nil
}

func main() {
	s := strings.NewReader("Lbh penpxrq gur pbqr!")
	r := rot13Reader{s}
	io.Copy(os.Stdout, &r)
	fmt.Println()
}
