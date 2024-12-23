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
FR.4.5.6.99

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
stateDiagram-v2
    state essai {
        [*] --> State1
        State1 --> State2 : 'AA BB CC DD EE FF GG HH II JJ KK LL MM NN OO PP'
        State1 --> State3 : 'Transition A'
        State2 --> State4 : 'Transition B mettre du texte pas mal plus long pour voir ce que ca donne comme rendering'
        State3 --> State4 : 'Transition C'
        State4 --> [*]

        state State1 {
            [*] --> SubState1
            SubState1 --> SubState2 : 'Sub Transition'
            SubState2 --> [*]
        }

        state State3 {
            [*] --> InnerState1
            InnerState1 --> InnerState2 : 'Inner Transition Z'
            InnerState2 --> State3A : 'blabla'
            State3A --> InnerState1 : 'Loop Transition Z'
            State3A --> [*]

            state State3A {
            [*] --> InnerState3A1
            InnerState3A1 --> InnerState3A2 : 'Inner Transition Y'
            InnerState3A2 --> aaaaaaa : 'Loop Transition Y'
            aaaaaaa --> bbbbbbbbb
            bbbbbbbbb --> [*]
            }
        }
    }
```


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
