import Array.ofDim

object Test8 {
    def main(args: Array[String]) {
        var myMatrix = Array.ofDim[Int](3,3)
        for( i <- 0 to 2 ){
            for( j <- 0 to 2 ){
                myMatrix(i)(j) = i*i+j*j
            }
        }
        for( i <- 0 to 2 ){
            for( j <- 0 to 2 ){
                print(" " + myMatrix(i)(j))
            }
            println();
        }
        var fruit = Array("apples", "oranges", "pears", "mangoes", "banana")
        val fruitL = fruit.toList
        println(fruitL)
    }
}
