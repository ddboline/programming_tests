public class HelloWorld {
    public static void main(String[] args){
        PrintHelloWorld();
        Student this_student = new Student();
        this_student.setName("HARRY");
        Student other_student = new Student("SALLY");
        System.out.printf("%s %s\n", this_student.getName(), other_student.getName());
        
        int[] intarray = new int[10];
        for(int i=0; i<10; i++){
            intarray[i] = 3*i+2;
        }
        for(int i=0; i<10; i++){
            System.out.printf("%d %d\n", i, intarray[i]);
        }
    }
    public static int PrintHelloWorld() {
        System.out.println("Hello World!");
        
        int myNumber = 5;
        double d = 4.5;
        d = 3.0;
        System.out.printf("%d %.1f\n", myNumber, d);
        
        char c = 'g';
        String s1 = new String("What up?");
        
        System.out.printf("%s %c\n", s1, c);
        
        int val = 0xFFFF;
        val &= 0xF;
        System.out.printf("%x\n", val);
        
        int[] arr = new int[10];
        for(int i=0; i<arr.length; i++) { arr[i] = 10-i; }
        System.out.printf("%d\n", arr.length);
        for(int i: arr)
            System.out.printf("%d ", i);
        System.out.printf("\n");
        return myNumber;
    }
}
