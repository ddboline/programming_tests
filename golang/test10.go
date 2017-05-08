package main

import (
	"fmt"
	"strings"
)

func main() {
	// Create a tic-tac-toe board.
        board := make([][]string, 3)
        for i:=0 ; i<3 ; i++ {
            board[i] = make([]string, 3)
            for j:=0 ; j<3 ; j++ {
                board[i][j] = "_"
            }
        }

	// The players take turns.
	board[0][0] = "X"
	board[2][2] = "O"
	board[1][2] = "X"
	board[1][0] = "O"
	board[0][2] = "X"

	for i := 0; i < len(board); i++ {
		fmt.Printf("%s\n", strings.Join(board[i], " "))
	}
}
