package andrey20005.stack;

public class DynamicStack<T> implements Stack<T> {

    private Object[] data;
    private int size = 0;
    private int capacity;

    // Конструктор с начальной емкостью
    public DynamicStack(int initialCapacity) {
        if (initialCapacity <= 0) {
            throw new IllegalArgumentException("Initial capacity must be positive");
        }
        this.capacity = initialCapacity;
        data = new Object[capacity];
    }

    // Полезный конструктор по умолчанию для начальной емкости 10 или другой подходящей константы
    public DynamicStack() {
        this(10); // Используем стандартную стартовую емкость
    }

    private void resize() {
        int newCapacity = capacity * 2;
        Object[] newData = new Object[newCapacity];
        
        // Копируем старые данные в новый массив
        for (int i = 0; i < size; i++) {
            newData[i] = data[i];
        }

        data = newData;
        capacity = newCapacity;
    }

    @Override
    public void push(T element) {
        // Если емкость достигнута, расширяем массив перед добавлением
        if (size == capacity) {
            resize();
        }
        data[size++] = element;
    }

    @Override
    @SuppressWarnings("unchecked")
    public T pop() throws EmptyStackException {
        if (size <= 0) throw new EmptyStackException();
        // Возвращаем и уменьшаем размер
        return (T) data[--size];
    }

    @Override
    @SuppressWarnings("unchecked")
    public T get(int i) throws NoSuchElementException {
        // Проверяем корректность индекса: 0 - верхний элемент, size-1 - самый нижний.
        if (i < 0 || i >= size) throw new NoSuchElementException();
        // Индекс в массиве = размер - i - 1
        return (T) data[size - i - 1];
    }

    @Override
    @SuppressWarnings("unchecked")
    public T peek() throws EmptyStackException {
        if (size <= 0) throw new EmptyStackException();
        // Верхний элемент находится в массиве по индексу size - 1
        return (T) data[size - 1];
    }

    @Override
    public String toString() {
        String res = "";
        try {
            T first = peek();
            res += "[" + first.toString();
        } catch (EmptyStackException e) {
            return "[]";
        }
        int i = 1;
        while (true) {
            try {
                res += ", " + get(i++).toString();
            } catch (NoSuchElementException e) {
                return res + "]";
            }
        }
    }
}

