import py4j._

object Py4j {
    def main(args: Array[String]) {
        val server = new GatewayServer(null)
        server.start()
    }
}
