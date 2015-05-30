class Rectangle extends Shape {
    Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    private double width, height;
    public double area() {
        return this.width * this.height;
    }
}