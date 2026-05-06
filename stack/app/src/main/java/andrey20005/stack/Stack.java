package andrey20005.stack;

public interface Stack<T> {
    public void push(T element) throws StackOverflowException;

    public T pop() throws EmptyStackException;

    public T get(int i) throws NoSuchElementException;

    public default T peek() throws EmptyStackException {
        try { return get(0); }
        catch (NoSuchElementException e) {
            throw new EmptyStackException();
        }
    }
}
