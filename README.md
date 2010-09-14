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
Currently the library supports encoding and decoding of primitive types 
only (no date/datetime and no FudgeMsg types).

It does not yet support taxonomies.

Licence
-------

  Copyright CERN, 2010.

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements. See the NOTICE file
distributed with this work for additional information
regarding copyright ownership. The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.