import java.util.Date

object Test3 {
    def main(args: Array[String]) {
        val logWithDateBound = log(new Date, _: String)
        logWithDateBound("message1")
        Thread.sleep(1000)
        logWithDateBound("message2")
        Thread.sleep(1000)
        logWithDateBound("message3")
    }
    def log(date: => Date, message: String) = {
        println(date + "-----" + message)
    }
}