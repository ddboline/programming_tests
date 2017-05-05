package main

import "golang.org/x/tour/pic"

func Pic(dx, dy int) [][]uint8 {
    var pic_array = make([][]uint8, dx)
    for ix:=0 ; ix<dx ; ix++ {
        pic_array[ix] = make([]uint8, dy)
    }
    for ix:0 ; ix<5 ; ix++ {
        pic_array[ix][ix] = 1.0
    }
}

func main() {
	pic.Show(Pic)
    var dx, dy = 5, 5
    var pic_array = make([][]uint8, dx)
    for ix:=0 ; ix<dx ; ix++ {
        pic_array[ix] = make([]uint8, dy)
    }
}
