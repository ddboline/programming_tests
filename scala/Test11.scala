class Point(val xc: Int, val yc: Int) {
    var x = xc
    var y = yc

    def move(dx: Int, dy:Int) {
        x += dx
        y += dy
        printf("Point x,y : %d,%d\n", x, y)
    }
}
    
class Location(override val xc: Int, override val yc: Int, val zc: Int) extends Point(xc, yc) {
    var z = zc
    
    def move(dx: Int, dy: Int, dz: Int) {
        x += dx
        y += dy
        z += dz
        printf("Point x,y,z : %d,%d,%d\n", x, y, z)
    }
}

object Test11 {
    def main(args: Array[String]) {
        val pt = new Location(10,20,5)
        
        pt.move(10,10,10)
        pt.move(10,10,10)
    }
}
