object Test14 {
    def main(args: Array[String]) {
        for(x <- -5 to 5) {
            printf("%d %s\n", x, matchTest(x))
        }
        for(x <- Array("one", "two", "three")) {
            printf("%s %s\n", x, matchTest(x))
        }
    }
    def matchTest(x: Any): Any = x match {
        case 1 => "one"
        case 2 => "two"
        case "two" => 2
        case y: Int => "scala.Int"
        case _ => "many"
    }
}
