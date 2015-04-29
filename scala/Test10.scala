class Point(xc: Int, yc:Int) {
    var x = xc
    var y = yc

    def move(dx: Int, dy:Int) {
        x = x + dx
        y = y + dy
        printf("Point x,y : %d %d\n", x, y)
    }
}

object Test10 {
    def main(args: Array[String]) {
        val pt = new Point(10,20)
        
        pt.move(10,10)
        pt.move(10,10)
    }
}
