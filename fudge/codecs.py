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

"""A bunch of encode/decode routines for types."""

import struct

from fudge import INDICATOR


def enc_indicator(val=None):
    """Encode a Fudge Indicator Type.

    This is a null-length type."""
    return ''

def enc_bool(val):
    """Encode a boolean as either a \0x00 or \0x01"""
    return struct.pack('!?', val)
    #if b:
    #    return '\x01'
    #return '\x00'

def enc_byte(val):
    """encode a single unsignd byte"""
    return struct.pack('!B', val)

def enc_short(val):
    """Encode a single signed int16"""
    return struct.pack("!h", val)

def enc_int(val):
    """Encode a single signed int32"""
    return struct.pack("!l", val)

def enc_long(val):
    """Encode a single signed int64"""
    return struct.pack("!q", val)

def enc_float(val):
    """Encode a single float"""
    return struct.pack("!f", val)

def enc_double(val):
    """Encode a single double"""
    return struct.pack("!d", val)

def enc_unicode(val):
    """encode a single unicode string"""
    utf8 = val.encode("utf-8")
    fmt = "!%ss"%len(utf8)
    return struct.pack(fmt, utf8)

def enc_str(val):
    """Encode a non-unicode string i.e a byte[]."""
    return str(val)

def _unpack(fmt, encoded):
    """A simple wrapper around struct.unpack

    Arguments:
        fmt: The format string (see struct docs for details)
        encoded: The encoded array"""
    length = struct.calcsize(fmt)
    return struct.unpack(fmt, encoded[:length])[0]

def dec_indicator(encoded):
    """decode a Fudge Indicator.
    
    Returns:
       A Singleton INDICATOR object"""
    assert len(encoded) == 0
    return INDICATOR

def dec_bool(encoded):
    """Decode a single boolean"""
    return _unpack('!?', encoded)

def dec_byte(encoded):
    """Decode a single unsigned byte"""
    return _unpack('!B', encoded)

def dec_short(encoded):
    """Decode a single signed short"""
    return _unpack('!h', encoded)

def dec_int(encoded):
    """Decode a single signed int"""
    return _unpack('!l', encoded)

def dec_long(encoded):
    """Decode a single signed long"""
    return _unpack('!q', encoded)

def dec_float(encoded):
    """Decode a single signed float"""
    return _unpack('!f', encoded)

def dec_double(encoded):
    """Decode a single signed double"""
    return _unpack('!d', encoded)

def dec_unicode(encoded):
    """Decode a single unicode string"""
    fmt = '!%ss'%len(encoded)
    utf8 = struct.unpack(fmt, encoded)[0]
    return unicode(utf8, "utf-8")

def dec_str(encoded):
    """Decode a non-unicode string i.e. byte[].

    """
    return str(encoded)

# Header helpers

def enc_name(encoded):
    """encode a single name string"""
    return struct.pack("!B", len(encoded)) + encoded

def dec_name(encoded):
    """Decode a name from field prefix string"""
    length = ord(encoded[0])
    return unicode(encoded[1:length+1])

# Arrays
def enc_array(encode_fn, encoded):
    """Encode an array, usually of numbers.  We use a type \
    specific encode function"""

    # TODO(jamesc) - Slow but correct...
    out = ''
    for val in encoded:
        out = out + encode_fn(val)
    return out

def dec_array(decode_fn, width, encoded):
    assert len(encoded)%width == 0

    out = []
    num_elements = len(encoded)/width
    for val in range(0, num_elements):
        out.append(decode_fn(encoded[val*width:val*width+width]))
    return out
