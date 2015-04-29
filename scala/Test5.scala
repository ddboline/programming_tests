object Test5 {
    def main(args: Array[String]) {
        println( apply( layout, 10 ) )
        println( layout(20.0) )
    }
    
    def apply( f: Int => String, v: Int ) = f(v)
    
    def layout[A](x: A) = "[" + x.toString() + "]"
}
