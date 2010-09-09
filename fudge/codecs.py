# 
# Copyright CERN, 2010
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
             
import struct
            
"""A bunch of encode/decode routines for types."""

def enc_bool(b):
    """Encode a boolean as either a \0x00 or \0x01"""
    if b:
        return '\x01'
    return '\x00'
                
def enc_byte(b):                                  
    """encode a single unsignd byte"""
    return struct.pack('!B', b)
    
def enc_short(s):                  
    """Encode a single signed int16"""
    return struct.pack("!h", s)
    
def enc_int(i):                    
    """Encode a single signed int32"""
    return struct.pack("!l", i)
    
def enc_long(l):   
    """Encode a single signed int64"""
    return struct.pack("!q", l)

def enc_float(f):                  
    """Encode a single float"""
    return struct.pack("!f", f)

def enc_double(d):          
    """Encode a single double"""
    return struct.pack("!d", d) 
    
def enc_unicode(s):
    """encode a single unicode string"""
    return s