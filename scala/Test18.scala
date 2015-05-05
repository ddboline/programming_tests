// import _root_.usr.share.py4j.GatewayServer
import py4j._

class AdditionApplication {
    def addition(first: Int, second: Int): Int = {
        return first + second
    }
}

object Test18 {
    def main(args: Array[String]) {
        val app = new AdditionApplication()
        val server = new GatewayServer(app)
        server.start()
    }
}