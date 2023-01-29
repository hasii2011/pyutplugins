```mermaid
classDiagram
    direction RL
    %% Links follow
    DiagramElement ..|> IResizable
    class IResizable { 
        + setSize()
        +int getMinimumSize()
    }
    class DiagramElement { 
    }
```
