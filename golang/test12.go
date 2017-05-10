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
	for {
		n, err := v.r.Read(b)
		if err != nil {
			break
		}
		for i:=0 ; i<n; i++ {
			if b[i] >= 65 && b[i] <= 90 {
                            b[i] = (b[i] + 13 - 65) % 26 + 65
			} else if b[i] >= 97 && b[i] <= 122 {
                            b[i] = (b[i] + 13 - 97) % 26 + 97
                        }
		}
		tot += n
	}
	return tot, io.EOF
}

func main() {
	s := strings.NewReader("Lbh penpxrq gur pbqr!")
	r := rot13Reader{s}
	io.Copy(os.Stdout, &r)
        fmt.Println()
}
