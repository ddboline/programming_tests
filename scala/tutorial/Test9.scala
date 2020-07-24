object Test9 {
    def main(args: Array[String]) {
        val capitals = Map("France" -> "Paris", "Japan" -> "Tokyo")
        
        for(capital <- capitals.keys) {
            printf("capitals.get( \"%s\" ) : %s\n", capital, capitals.get(capital))
        }
        for(capital <- List("France", "Japan", "Oswego")){
            printf("capitals.get( \"%s\" ) : %s\n", capital, show(capitals.get(capital)))
        }
    }
    def show(x: Option[String]) = x match {
        case Some(s) => s
        case None => "?"
    }
}
