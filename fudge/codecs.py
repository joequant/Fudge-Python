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

def enc_name(s):
    """encode a single name string"""
    return struct.pack("!B", len(s)) + s

def _unpack(format, bytes):
    n = struct.calcsize(format)
    return struct.unpack(format, bytes[:n])[0]

def dec_bool(bytes):
    """Decode a single boolean"""
    byte = dec_byte(bytes)
    return byte == 1
        
def dec_byte(bytes):
    """Decode a single unsigned byte"""
    return _unpack('!B', bytes) 

def dec_short(bytes):
    """Decode a single signed short"""
    return _unpack('!h', bytes) 

def dec_int(bytes):
    """Decode a single signed int"""
    return _unpack('!l', bytes)  
    
def dec_long(bytes):
    """Decode a single signed long"""
    return _unpack('!q', bytes) 
    
def dec_float(bytes):
    """Decode a single signed float"""
    return _unpack('!f', bytes) 

def dec_double(bytes):
    """Decode a single signed double"""
    return _unpack('!d', bytes) 
    
def dec_unicode(bytes):
    """Decode a single unicode string"""
    return unicode(bytes) 
        
def dec_name(bytes):
    """Decode a name from field prefix string"""
    length = ord(bytes[0])
    return unicode(bytes[1:length+1])