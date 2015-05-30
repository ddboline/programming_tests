class Circle extends Shape {
    Circle(double diameter) {
        this.diameter = diameter;
    }
    private static final double PI = Math.PI;
    private double diameter;
    public double area() {
        double radius = diameter / 2.0;
        return PI * radius * radius;
    }
}