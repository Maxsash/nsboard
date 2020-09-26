NetSquid-BoardGames (0.0.1)
================================

Description
-----------

This is a user contributed _snippet_ for the [NetSquid quantum network simulator](https://netsquid.org).

A snippet for implementing and playing board games using quantum networks and quantum operations. The network contains a TaskMaster node which controls the main memory for the board game. There are two other nodes for players zero and one. Each player receives a qubit from the TaskMaster and can choose to perform any quantum operation on it and then specify which qubit will be sent to the other player. 

Installation
------------

See the [INSTALL file](INSTALL.md) for instruction of how to install this snippet.

Documentation
-------------

To build and see the docs see the [docs README](docs/README.md).

Usage
-----
The user has to specify the size of QuantumMemory that will be used as the board, this initializes the network with three nodes. Each player will get as many turns as the size of the QuantumMemory. At each turn, player can choose to operate on the qubit and then specify the index of qubit that will be sent to the other player. At the end of all the turns, the result after measuring all the qubits in the QuantumMemory will be presented and a score based on the value of qubit and its probability will be calculated. If the score is more than half the size of QuantumMemory, Player One wins; else Player Zero wins. 

Contributor
------------

Yash Shrivastava (Maxsash) | yash@maxsash.com
License
-------

**TEMPLATE**: specify the license applicable to your package.

The NetSquid-SnippetTemplate has the following license:

> Copyright 2020 QuTech (TUDelft and TNO)
>
>   Licensed under the Apache License, Version 2.0 (the "License");
>   you may not use this file except in compliance with the License.
>   You may obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
>   Unless required by applicable law or agreed to in writing, software
>   distributed under the License is distributed on an "AS IS" BASIS,
>   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
>   See the License for the specific language governing permissions and
>   limitations under the License.
