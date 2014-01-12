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


from fudgemsg.taxonomy.map import *

class TestMapTaxomomy(unittest.TestCase):

    def test_simple(self):
        t = Taxonomy({ 1 : u'foo', 2 : u'bar'})
        self.assertEquals(u'foo', t.get_name(1))
        self.assertEquals(1, t.get_ordinal(u'foo'))

        self.assertEquals(u'bar', t.get_name(2))
        self.assertEquals(2, t.get_ordinal(u'bar'))

        self.assertEquals(2, len(t))

    def test_not_exists(self):
        t = Taxonomy({1 : u'foo'})

        self.assertEquals(None, t.get_name(2))
        self.assertEquals(None, t.get_ordinal(u'bar')) 

    def test_empty_map(self):
        t = Taxonomy()

        self.assertEquals(0, len(t))

        self.assertEquals(None, t.get_name(2))
