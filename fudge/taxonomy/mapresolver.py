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

"""A simple example of a TaxonomyResolver.

""" 

class TaxonomyResolver:
    """
    A Simple dict based taxonomy resolver .
    
    All taxonomies are passed at creation time. 
    
    A resolver should support `resolve_taxonomy(id)` method
    """
    def __init__(self, taxonomy_dict=None):
        """Create a new Taxonomy Resolver.
        
        Arguments:
            taxonomy_dict: A dict of short -> Taxonomy objcts
                (default:None)
        """
        self._taxonomy_dict = {}
        if taxonomy_dict:
            self._taxonomy_dict = dict(taxonomy_dict)
    
    def resolve_taxonomy(self, taxonomy_id):
        """Return the taxonomy for a given ID
        
        Arguments:
            taxonomy_id : the id of the Taxonomy we look for
            
        Returns:
            A `Taxonomy` if one exists for that id
            
        Raises:
            KeyError : If there is no taxonomy for a given ID
        """
        return self._taxonomy_dict[taxonomy_id]
        
    def __len__(self): 
        return len(self._taxonomy_dict)