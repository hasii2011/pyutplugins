```mermaid
classDiagram
    direction RL
    %% Links follow
    class SimpleClass { 
        <<type>>
        +str publicMethod()
        -float privateMethod()
        #int protectedMethod()
        + methodNoReturnType()
        + methodWithParameters(parameter1, parameter2)
    }
```
