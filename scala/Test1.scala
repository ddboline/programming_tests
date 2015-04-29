object Test1 {
    def main(args: Array[String]) {
        println( "Returned Value : " + addInt() )
    }
    def addInt( a:Int=5, b:Int=7 ) : Int = {
        var sum = 0
        sum = a + b
        sum
    }
}