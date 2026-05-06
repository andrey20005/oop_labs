package org.example;

import andrey20005.stack.ArrayStack;
import andrey20005.stack.DynamicStack;
import andrey20005.stack.EmptyStackException;
import andrey20005.stack.NoSuchElementException;
import andrey20005.stack.StackOverflowException;

public class App {

    public static void main(String[] args) {
        System.out.println("--- Testing ArrayStack (Fixed Capacity) ---");
        // Создаем стек с небольшой емкостью, чтобы протестировать переполнение
        ArrayStack<String> arrayStack = new ArrayStack<>(3);
        try {
            arrayStack.push("A");
            System.out.println("Push A. Stack: " + arrayStack); // [A]

            arrayStack.push("B");
            System.out.println("Push B. Stack: " + arrayStack); // [B, A] (Порядок в toString соответствует LIFO)

            arrayStack.push("C");
            System.out.println("Push C. Stack: " + arrayStack); // [C, B, A]

            // Пытаемся добавить четвертый элемент - должно произойти переполнение
            arrayStack.push("D"); 
        } catch (StackOverflowException e) {
            System.err.println("SUCCESS: Caught expected StackOverflowException: " + e.getMessage());
        } catch (EmptyStackException | NoSuchElementException e) {
            e.printStackTrace();
        }

        // Демонстрация pop/peek
        try {
            String popped = arrayStack.pop();
            System.out.println("Pop operation: " + popped); // C
            System.out.println("After pop. Stack: " + arrayStack); // [B, A]
            
            // Проверяем элемент под верхом (peek)
            String peeked = arrayStack.peek();
            System.out.println("Peek operation: " + peeked); // B

        } catch (Exception e) {
             e.printStackTrace();
        }


        System.out.println("\n--- Testing DynamicStack (Resizable Capacity) ---");
        // Создаем динамический стек с малой начальной емкостью
        DynamicStack<Integer> dynamicStack = new DynamicStack<>(2);

        dynamicStack.push(10); // Cap=2, Size=1
        System.out.println("Push 10. Stack: " + dynamicStack);

        dynamicStack.push(20); // Cap=2, Size=2
        System.out.println("Push 20. Stack: " + dynamicStack);

        // Этот push должен вызвать автоматическое расширение (Cap -> 4)
        dynamicStack.push(30); // Cap=4, Size=3
        System.out.println("Push 30 (Trigger Resize). Stack: " + dynamicStack);

        dynamicStack.push(40); // Cap=4, Size=4
        System.out.println("Push 40. Stack: " + dynamicStack);

        for (int i = 0; i < 60; i++) {
            dynamicStack.push(i);
        }
        System.out.println("Add 60 elements: " + dynamicStack);

        dynamicStack.pop(); dynamicStack.pop(); dynamicStack.pop(); dynamicStack.pop(); 

        System.out.println("After 4 pop: " + dynamicStack);
    }
}
