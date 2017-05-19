package main

import (
	"fmt"
	"math"
)

func Sqrt(x float64) float64 {
	var zn = 1.0
	for zn1 := zn + 1.0; math.Abs(zn1-zn) > 1e-12; zn1 = zn - (zn*zn-x)/(2*zn) {
		fmt.Printf("zn %f %f\n", zn, zn1)
		zn = zn1
	}
	return zn
}

func main() {
	fmt.Println(Sqrt(2), math.Sqrt(2))
}
