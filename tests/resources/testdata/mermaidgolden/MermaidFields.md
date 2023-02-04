```mermaid
classDiagram
    direction RL
    %% Links follow
    class ClassWithFields { 
        -str privateField
        +int publicField
        #float protectedField
        +bool fieldNoDefaultValue
        - fieldNoType
        - fieldNoTypeNoDefaultValue
        <<type>>
    }
```
