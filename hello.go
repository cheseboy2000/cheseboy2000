package main

import (
	"fmt"
	"time"
	//"math/rand"
)
func show(i int){
	// 设置种子，不然每次都会随机成0
    fmt.Println(i)
}
func main() {
	for i := 1; i <= 10; i++{
		go show(i)
		time.Sleep(10000)
	}
}