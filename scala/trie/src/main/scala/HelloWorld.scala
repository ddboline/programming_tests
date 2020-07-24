package example

object HelloWorld extends App {
  val h = HelloWorld
  println(h)
}

class HelloWorld {
  override def toString(): String = {
    "Hello World!"
  }
}
