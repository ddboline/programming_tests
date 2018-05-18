package main

import (
	"fmt"
)

type Address struct {
	city, state string
}
type Person struct {
	name    string
	age     int
	Address
}

func main() {
	var p = Person{name: "Naveen", age: 50, Address: Address{city: "Chicago", state: "Illinois"}}
	fmt.Println("Name:", p.name)
	fmt.Println("Age:", p.age)
	fmt.Println("City:", p.city)
	fmt.Println("State:", p.state)
}
