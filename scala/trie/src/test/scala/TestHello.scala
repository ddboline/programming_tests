import org.scalatest._
import example.HelloWorld

class HelloWorldSpec extends FunSuite with DiagrammedAssertions {
    test("Hellow World returns nothing") {
        val h = new HelloWorld
        assert(h.toString == "Hello World!")
    }
}