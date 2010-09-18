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
import unittest


from fudge.taxonomy.mapresolver import *
from fudge.taxonomy.map import Taxonomy

class TestMapTaxomomy(unittest.TestCase):
    def test_no_resolver(self):
        tr = TaxonomyResolver()
        
        self.assertEquals(0, len(tr)) 
        self.assertRaises(KeyError, tr.resolve_taxonomy, 0)
        
    def test_simple_resolver(self):
        t1 = Taxonomy({1: u'foo', 2: u'bar'})
        t2 = Taxonomy({3: u'foo', 4: u'bar'}) 
        
        tr = TaxonomyResolver({1 : t1, 255: t2})
        self.assertEquals(t1, tr.resolve_taxonomy(1)) 
        self.assertEquals(t2, tr.resolve_taxonomy(255))                  
        self.assertEquals(2, len(tr))