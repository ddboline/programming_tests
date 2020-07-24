object Test15 {
    def main(args: Array[String]) {
        for(x <- -5 to 5) {
            println(matchTest(x))
        }
        for(x <- Array("one", "two", "three")) {
            println(matchTest(x))
        }
    }
    def matchTest(x: Any) : Any = x match {
        case 1 => "one"
        case "two" => 2
        case y: Int => "scala.Int"
        case _ => "many"
    }
}
