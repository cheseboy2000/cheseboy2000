package main
import (
	"fmt"
	"sync"
	"strconv"
)
var wg sync.WaitGroup
func main()  {
	for i:=0;i<10;i++{
		wg.Add(1)
		go rungo("hello word , "+strconv.Itoa(i))
	}
	wg.Wait()
}
func rungo(t string){
	defer wg.Done()
	fmt.Println(t)
}
