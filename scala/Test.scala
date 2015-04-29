object Test {
    def main(args: Array[String]) {
        println( delayed(1000) )
        println( delayed(time()) )
    }
    def time() = {
        println( "Getting time in nano seconds" )
        System.nanoTime
    }
    def delayed( t: => Long ) = {
        println( "In delayed method" )
        val _t0 = t
        println( "Param: " + _t0 )
        val _t1 = t
        println( "Param: " + _t1 )
        t
    }
}