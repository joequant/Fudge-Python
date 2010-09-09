Introduction 
------------
This is a native python implementation of the Fudge messaging system.

Fudge is a hierarchical, typesafe, binary, self-describing message encoding 
system. See <http://www.fudgemsg.org/display/FDG/Fudge+Messaging+Home>
for more details.             

Usage
-----
The python library follows the other implementations in terms of the overall
structure.  There is an `Envelope` and `Message` objects which represent the
main entry point into the system at this point.

`Context`s will be added along with taxonomies.
                                                                                          

Status
------
Currently the library supports encoding and decoding of primitive types only.

It does not support taxonomies.