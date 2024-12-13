# REQUIREMENTS
Une liste avec plusieurs requirements

## REQ ID
FR.4.5.6.7

### SOURCE
La source est le blablablablabla

### PRIORITY
Normal

### STATUS
On ne s'en sert pas ici, on va plutot y aller avec les resultats de test, l'implementation etc pour y aller d'un status

### VERIFICATION METHOD
Will verify this with a test

### DEPENDENCIES
quoi faire ici

### DESCRIPTION

Une courte description sur une ligne qui va se rammasser dans le requirement graph ou table

### DETAILS

Ici on detail le requirement.

On peut y aller longuement sur plusieurs ligne.

Comme ceci :

``` mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +void eat()
        +void sleep()
    }

    class Mammal {
        +void giveBirth()
    }

    class Bird {
        +void fly()
    }

    Animal <|-- Mammal
    Animal <|-- Bird

    class Dog {
        +void bark()
    }

    Mammal <|-- Dog
```

ou bien ceci :

| Right | Left | Default | Center |
|------:|:-----|---------|:------:|
|   12  |  12  |    12   |    12  |
|  123  |  123 |   123   |   123  |
|    1  |    1 |     1   |     1  |



## REQ ID
SR.1.2.3.4

### SOURCE
La source est le blablablablabla

### PRIORITY
Critical

### STATUS
On ne s'en sert pas ici, on va plutot y aller avec les resultats de test, l'implementation etc pour y aller d'un status

### VERIFICATION METHOD
Will verify this with a test

### DEPENDENCIES
quoi faire ici

### DESCRIPTION

Une courte description sur une ligne qui va se rammasser dans le requirement graph ou table

### DETAILS

Ici on detail le requirement.

On peut y aller longuement sur plusieurs ligne.

Comme ceci :

``` mermaid
  graph TD;
      A[qwerty] -- NO --> B;
      A -- YES --> C;
      B --> D;
      C --> D;
      D --> E;
```

ou bien ceci :

| Right | Left | Default | Center |
|------:|:-----|---------|:------:|
|   12  |  12  |    12   |    12  |
|  123  |  123 |   123   |   123  |
|    1  |    1 |     1   |     1  |
