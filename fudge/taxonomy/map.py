#
# Copyright CERN, 2010.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

class Taxonomy(object):
    """
    A map based taxonomy.  
    
    Useful when the taxonomy is generated
    dynamically  or a a building block from loading taxonomies
    from storage. 
    """
    

    def __init__(self, taxonomy_map = None):
        """ Create a new Taxonomy

        Arguments:
           taxomomy_map:  A map of short -> string with the 
           mapping of ordinal to name."""
        self._by_name = {}
        if taxonomy_map:
            self._by_ordinal = dict(taxonomy_map) 
            
            for key, value in self._by_ordinal.iteritems():
                self._by_name[value] = key
        else:
            self._by_ordinal = {} 
     
    def get_name(self, ordinal):
        """Return the name for a given ordinal.
         
        Arguments:
            ordinal : the ordinal to look up (short)
             
        Returns:
            The name as a unicode string
             
        Raises:
            KeyError : If the ordinal is not in the taxomomy"""      
        try:
            return self._by_ordinal[ordinal] 
        except KeyError:
            return None
            
    def get_ordinal(self, name):
        """Return the ordinal for a given name.

        Arguments:
            name : the name to look up (unicode string)

        Returns:
            The ordinal as a short

        Raises:
            KeyError : If the name is not in the taxomomy"""      
        try:
            return self._by_name[name] 
        except KeyError:
            return None
            
    def __len__(self):
        """Return the number of elements in the map.""" 
        return len(self._by_ordinal)
       