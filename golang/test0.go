package main

import "fmt"

func add(x, y float64) float64 {
	return x + y
}

func main() {
        var x, y float32 = 42, 13
	fmt.Println(add(float64(x), float64(y)))
}
