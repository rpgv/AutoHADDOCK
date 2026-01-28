# AutoHaddock
Automatically submits and downloads molecular docking models to the HADDOCK platform.
## Installation
To install AutoHaddock, run the following command:

```git clone https://github.com/rpgv/AutoHADDOCK.git``` 

```cd AutoHaddock/ ``` 

```pip install selenium``` 

## Usage
### Basic Usage:
```python haddock_run.py <creds> <docking_pairs> <structures> <wait>```
-  ```creds``` -> Path to file (.json) containing email and password to access HADDOCK servers - template included;
- ```docking_pairs``` -> Path to CSV file containing file name of DNA and Protein structure pairs - template included;   
- ```structure-dir``` -> Path to structures - subdirs ```structure-dir/DNA/``` and ```structure-dir/Protein/``` are assumed to exist; 
- ```wait``` -> Wait interval between ab-initio docking submissions - defaults to 2 Hours every 10 submissions:
   - Note: Smaller intervals will lead to server overload - exponentially increasing wating time; 

Example:
```cd AutoHaddock```

```python haddock_run.py templates/mycreds.json templates/docking_pairs template/Structures 70```


---
```python haddock_downloader.py <creds> <docking_pairs> <structures> <wait>```

- ```result_links``` -> Path to CSV file containing Links to HADDOCK results - template included;
- ```wait``` -> Wait interval between downloads - allows docking to finish in the meantime;


## Important Note

* Haddock is very specific with PDB formatting; 
* I highly advise using pdb_tools (https://github.com/haddocking/pdb-tools) to prepare structures:
* Usual modfications:
  * Remove 'selaltoc';
  * Renumber both residues and atoms; 
  * Splitting chains if often useful; 
  * Guaranteeing ATOM / HETATM congruency; 
  * Remove HEADER and Waters (if present);
  * Remove PDB Master line after editions;



## Description
### Features
* Automatically submits molecular docking models to the HADDOCK platform;
* Automatically downloads the first structure of each result; 
  
## Requirements
AutoHaddock requires:
* python>=3.10
* selenium==4.36.0
* pandas==2.3.2
* HADDOCK server access ( available at https://wenmr.science.uu.nl/haddock2.4/submit/1 )

## Contributing

Contributions are welcome! Please submit pull requests to the main repository.

## License
AutoHaddock is released under the MIT license. See LICENSE for details.
