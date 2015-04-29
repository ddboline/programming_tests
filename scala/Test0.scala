object Test0 {
    def main(args: Array[String]) {
        printStrings( "Hello", "Scala", "Python" )
        printStrings( "NO!!!" )
    }
    def printStrings( args:String* ) = {
        var i = 0
        for( arg <- args ){
            println( "Arg value[" + i + "] = " + arg )
            i += 1
        }
    }
}