object Test6 {
    def main(args: Array[String]) {
        println( "multiplier(1) value = " + multiplier(1) )
        println( "multiplier(2) value = " + multiplier(2) )
        factor = 5
        println( "multiplier(1) value = " + multiplier(1) )
        println( "multiplier(2) value = " + multiplier(2) )
        
        val greeting = "Hello World!"
        println( greeting )
        
        var greet = "Hello World!"
        println( greet )
        
        println( greet.length() )
        
        printf( "The length of this string is %d\n", greeting.length() )
    }
    var factor = 3
    val multiplier = (i:Int) => i * factor
}
