import scala.util.matching.Regex

object Test17 {
    def main(args: Array[String]) {
        val pattern = "(S|s)cala".r
        val str = "Scala is scalable and cool"
        
        println((pattern findAllIn str).mkString(","))
        println(pattern replaceFirstIn(str, "Java"))
        
    }
}
