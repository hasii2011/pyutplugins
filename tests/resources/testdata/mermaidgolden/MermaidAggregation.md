```mermaid
classDiagram
    direction RL
    %% Links follow
    Author "1.*" o-- "0.*" Book : fakeAuthor
    class Author { 
        +bool amIEgotistical()
    }
    class Book { 
        + bogusExpert(unImportant)
    }
```
