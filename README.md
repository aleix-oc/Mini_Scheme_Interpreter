# Intèrpret Mini Scheme

Utilitzant Python i ANTLR s'ha simulat una petita versió del llenguatge funcional Scheme.

## Installation

Utilitza pip per instal·lar els requirements:

```bash
pip install -r requirements.txt
```
Nota: Cal que ens trobem a un entorn Python up to date.

## Estructura del projecte

Els tres arxius principals de l'intèrpret són:

- `scheme.g4`: La gramàtica del llenguatge

- `scheme.py`: Cos de l'intèrpret

- `visitor.py`: Funcions de visitors de l'AST

A més, hi ha diversos arxius `.scm`, `.inp`i `.out`, els quals s'expliquen a l'ús de l'intèrpret.

## Usage
Un cop ens trobem a un entorn python amb els requirements instal·lats, fem la comanda `make` per poder probar qualsevol codi `.scm` de la següent forma:

```bash
python3 scheme.py programa.scm < input.txt > output.txt
```

Si hi ha qualsevol canvi a la gràmatica, fem `make clean` i tornem a fer `make`.

### Sobre els jocs de prova

Hi ha tres arxius `.scm`:

- `basic`: És el joc de proves més simple, va demanant l'entrada de nombres a l'usuari i realitza avaluacions i operacions sobre ells.

- `fact`: L'entrada d'aquest joc és un nombre, retornarà la llista dels factorials d'aquest nombre fins a 1 havent filtrat els que tenen dígits senars.

- `superior`: Ens demanarà una llista i realitzarà diverses funcions, tant bàsiques com d'ordre superior sobre ella, després ens demana una altra i fa un zip. Per aquest joc tenim dos arxius `.inp`i dos `.out`, que són `llista_petita.*` i `llista_gran.*`.

Cal destacar que sobre els tres programes s'han utilitzat totes les eines disponibles al llenguatge interpretat: let, definicions de constants, recursió...

## Conclusió

Amb aquest interprèt es poden treure dos punts principals sobre Scheme:

Té una lògica molt intuïtiva i facilita la traducció  de la idea al nostre cervell al codi aplicant un paradigma de programació purament funcional i encara més fàcil és aquesta feina amb la seva manera d'expressar condicions, les definicions simples de funcions i constants, etc.

Un punt dolent és la gramàtica, relativament, ja que un programador que escrigui abans de pensar es trobarà amb que no para de tenir errors de sintaxi i veurà un embolic de parentèsis, però si se sap el que es vol fer i s'escriu amb cura veurem que l'ús dels parèntesis per tancar cada expressió quadra perfectament.

***
