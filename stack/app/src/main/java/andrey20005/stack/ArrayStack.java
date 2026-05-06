package andrey20005.stack;

public class ArrayStack<T> implements Stack<T> {
    protected Object[] data;
    protected int size = 0;
    protected final int l;

    public ArrayStack(int l) {
        data = new Object[l];
        this.l = l;
    }

    @Override
    public void push(T element) throws StackOverflowException {
        if (size >= l) throw new StackOverflowException();
        data[size++] = element;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T pop() throws EmptyStackException {
        if (size <= 0) throw new EmptyStackException();
        return (T) data[--size];
    }

    @SuppressWarnings("unchecked")
    @Override
    public T get(int i) throws NoSuchElementException {
        if (size-i-1 < 0) throw new NoSuchElementException();
        return (T) data[size-i-1];
    }

    @SuppressWarnings("unchecked")
    @Override
    public T peek() throws EmptyStackException {
        if (size <= 0) throw new EmptyStackException();
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
        // return res;
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
