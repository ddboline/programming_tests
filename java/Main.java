public class Main {
    public static void main(String[] args){
        Shape s1 = new Circle(5.0);
        Shape s2 = new Rectangle(5.0, 4.0);
        Shape larger = getLargerShape(s1, s2);
        
        System.out.println("The area of something something: " + larger.area());
    }
    public static Shape getLargerShape(Shape s1, Shape s2) {
        if(s1.area() > s2.area())
            return s1;
        else
            return s2;
    }
}
