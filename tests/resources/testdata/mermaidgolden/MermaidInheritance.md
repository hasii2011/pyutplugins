```mermaid
classDiagram
    direction RL
    %% Links follow
    Animal<|--Duck
    class Animal { 
        +bool isAnimal()
    }
    class Duck { 
        + swim()
        + quack()
    }
```
