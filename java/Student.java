public class Student {
    Student() {};
    Student(String name) {
        this.name = name;
    }
    
    private String name;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public static void main(String[] arg) {
        Student this_student = new Student();
        this_student.setName("HARRY");
        Student other_student = new Student("SALLY");
        System.out.printf("%s %s\n", this_student.getName(), other_student.getName());
    }
}
