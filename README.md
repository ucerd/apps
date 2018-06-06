# COMPSs applications folder

This folder contains all the applications developed by the Workflows and Distributed
Computing grou that can be executed at MareNostrum III. 

Its purpose is to share the applications among all the members of the group to ease
debugging, testing executions or benchmarking executions. Thus, please, when a new
application is uploaded to the folder, recall setting the file permissions to be 
accessible for all the members of the group (recommended `rwxrwxr-x`).

```$ chmod -R 775 *```


## Application's Folder Structure 

Each application has a unique folder that hosts all the versions for that application. 
For instance, the matmul application that has version for PyCOMPSs, COMPSs with files,
COMPSs using objects and COMPSs with byte arrays and has the following tree directory.

```
COMPSs_APPS
  |- matmul
  |    |- python
  |    |    |- version_1
  |    |    |    |- src			Application source code
  |    |    |    |- dist        	Application binary or jar
  |    |    |    |- bin         	External binaries needed by the application
  |    |    |    |- lib         	External libraries needed by the application
  |    |    |    |- launch.sh     	Execution example (must use enqueue_compss)
  |    |    |- ...
  |    |    |- version_n
  |    |    |- launch.sh		Execution example for automatic process
  |    |    |- clean.sh			Cleans the folder for *ALL* versions
  |    |    |- README			Brief description of the application
  |    |- java
  |    |    |- ...
  |    |- c
  |    	  |- ...
  |- ...
```

**REMINDER**: For each language there **must** be **one** launch.sh and **one** clean.sh script
          that executes the **stable** (base) version of that language. This script is used by
          the automatic benchmarking process. 

**REMINDER**: For each version directory there **must** be a launcher script, a src directory with
the source code of that version, and a dist folder with the application binary or jar.


**WARNING**: Addtional binaries commonly used by all versions **must** be placed in the
         application's root folder.

**WARNING**: Additional input data used by all versions **must** be placed in a new folder
         inside the COMPSs_DATASETS with the **same** application name.

