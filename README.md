# ndLibrarySupport
Nth dimensional Library support.

code for 3D slicer (www.slicer.org) to help load up a package of 3D+ data with appropriate and simplified UI and view settings.
Current view designed for 4D (multi-modal/contrast, not time series). Has some limited tractography support.

Major design goal is to take data in its current form, without any modification of the existing data or its organization, discover and load relavant bits.
To accomplish this, files detailing relevant bits are required in each important directory.
These are always named "lib.conf". They can act as pointers (through use of the Path field) to allow arbitrary re-organization.
For files with incomplete header information, we use nhdr files, and/or the OriginTransform field to move data around the 3D slicer scene

Also included is a simplify class to save the minimal set to a new location, once data is idenfified with appropriate lib.conf files.
We(CIVM) use this to make simple packages for distribution.

Based on earlier c++ work(not officially released). 
Much of the conversion was done by Austin Kao, with finishing work by James Cook.
