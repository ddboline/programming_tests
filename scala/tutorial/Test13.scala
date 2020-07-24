trait Equal {
    def isEqual(x: Any): Boolean
    def isNotEqual(x: Any): Boolean = !isEqual(x)
}

class Point(val xc: Int, val yc: Int) extends Equal {
    var x = xc
    var y = yc

    def move(dx: Int, dy:Int) {
        x += dx
        y += dy
        printf("Point x,y : %d,%d\n", x, y)
    }
    
    def isEqual(obj: Any) = {
        obj.isInstanceOf[Point] &&
        obj.asInstanceOf[Point].x == x
    }
}

object Test13 {
    def main(args: Array[String]) {
        val p1 = new Point(2,3)
        val p2 = new Point(2,4)
        val p3 = new Point(3,3)
        
        printf("%s %s %s\n", p1.isNotEqual(p2), p1.isNotEqual(p3), p1.isNotEqual(2))
    }
}
