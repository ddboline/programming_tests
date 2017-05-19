package main

import (
	"fmt"
	"math"
)

type ErrNegativeSqrt float64

func (e ErrNegativeSqrt) Error() string {
	return fmt.Sprintf("cannot Sqrt negative number: %v\n", float64(e))
}

func Sqrt(x float64) (float64, error) {
	if x < 0.0 {
		return 0, ErrNegativeSqrt(x)
	}
	var zn = 1.0
	for zn1 := zn + 1.0; math.Abs(zn1-zn) > 1e-12; zn1 = zn - (zn*zn-x)/(2*zn) {
		fmt.Printf("zn %f %f\n", zn, zn1)
		zn = zn1
	}
	return zn, nil
}

func main() {
	fmt.Println(Sqrt(2))
	fmt.Println(Sqrt(-2))
}
