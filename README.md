#AutoHaddock
Automatically submits and downloads molecular docking models to the HADDOCK platform.
##Installation
To install AutoHaddock, run the following command:

```pip install autohaddock``` 

##Usage
###Basic Usage:
```python haddock_run.py <credential-file> <structure-dir> <wait-between>```

    * ```credential-file``` -> Path to file (.json) containing email and password to access HADDOCK servers - template included;
    *  ```csv-file``` -> Path to CSV file containing file name of DNA and Protein structure pairs - template included; 
    *  ```structure-dir``` -> Path to structures - files assumed to be on subdirs ```structure-dir/DNA/``` and ```structure-dir/Protein/``` respectively; 
    *  ```wait-between``` -> Wait interval between ab-initio docking submissions - defaults to 2 Hours every 10 submissions:
       *  Note: Smaller intervals will lead to server overload - exponentially increasing wating time; 






##Description
###Features
* Automatically submits molecular docking models to the HADDOCK platform;
* Automatically downloads the first structure of each result; 
  
## Requirements
AutoHaddock requires:
* ---
* ---	
* HADDOCK server ( available at https://haddock-server.org/ )

##Contributing

Contributions are welcome! Please submit pull requests to the main repository.

##License
AutoHaddock is released under the MIT license. See LICENSE for details.