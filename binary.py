def repr(bytes):
    return "b'\\x" + '\\x'.join((f'{b:02x}' for b in bytes)) + "'"

def from_bytes(bytes):
    return int.from_bytes(bytes, byteorder='little')

def read_block(bytes, offset, size):
    assert len(bytes) >= offset + size
    return bytes[offset:offset+size]

def read_block_until_end(bytes, offset):
    assert len(bytes) >= offset
    return bytes[offset:]

def read_until_zero(bytes, address):
    result = b''
    i = address
    while bytes[i] != 0:
        result += read_block(bytes, i, 1)
        i += 1
    return result

def read_byte(bytes, offset):
    return from_bytes(read_block(bytes, offset, 1))

def read_word(bytes, offset):
    return from_bytes(read_block(bytes, offset, 2))

def write_word(bytes, offset, data):
    bytes[offset] = data & 0xff
    bytes[offset+1] = (data >> 8) & 0xff

def read_dword(bytes, offset):
    return from_bytes(read_block(bytes, offset, 4))

def read_qword(bytes, offset):
    return from_bytes(read_block(bytes, offset, 8))

def write_dword(bytes, offset, data):
    bytes[offset] = data & 0xff
    bytes[offset+1] = (data >> 8) & 0xff
    bytes[offset+2] = (data >> 16) & 0xff
    bytes[offset+3] = (data >> 24) & 0xff

def update_byte(bytes, offset, value):
    return bytes[:offset] + value.to_bytes(1, 'little') + bytes[offset+1:]

def update_word(bytes, offset, value):
    return bytes[:offset] + value.to_bytes(2, 'little') + bytes[offset+2:]

def update_dword(bytes, offset, value):
    return bytes[:offset] + value.to_bytes(4, 'little') + bytes[offset+4:]

def update_block(bytes, offset, block):
    return bytes[:offset] + block + bytes[offset+len(block):]

def write_block(bytes, offset, block):
    assert len(bytes) >= offset+len(block)
    bytes[offset:offset+len(block)] = block

def read_virtual(info, bytes, address, size):
    for section in info['sections'].values():
        if section['address'] <= address < section['address-end']:
            if address - section['address'] >= section['raw-size']:
                return b'\x00'*size
            else:
                return read_block(bytes, section['raw-offset'] + address - section['address'], size)
    else:
        return None

def read_virtual_until_zero(info, bytes, address):
    result = b''
    for section in info['sections'].values():
        if section['address'] <= address < section['address-end']:
            i = section['raw-offset'] + address - section['address']
            while i < section['raw-offset'] + section['raw-size'] and bytes[i] != 0:
                result += read_block(bytes, i, 1)
                i += 1
            return result
    else:
        return None

def write_virtual(info, bytes, address, block):
    for section in info['sections'].values():
        if section['address'] <= address < section['address-end']:
            assert address - section['address'] + len(block) <= section['raw-size']
            return write_block(bytes, section['raw-offset'] + address - section['address'], block)
    else:
        assert False

def read_directory(info, bytes, directory):
    return read_virtual(info, bytes, info['directories'][directory]['address'], info['directories'][directory]['size'])

def read_section(info, bytes, section):
    size = max(info['sections'][section]['raw-size'], info['sections'][section]['address-end'] - info['sections'][section]['address'])
    return read_block(bytes, info['sections'][section]['raw-offset'], info['sections'][section]['raw-size']) + b'\0'*(size - info['sections'][section]['raw-size'])


class Pipe(object):
    def __init__(self, bytes):
        self.bytes = bytes
        self.offset = 0

    def read_block(self, size):
        result = read_block(self.bytes, self.offset, size)
        self.offset += size
        return result        

    def read_block_until_end(self):
        result = read_block_until_end(self.bytes, self.offset)
        self.offset += len(result)
        return result

    def read_until_zero(self):
        result = read_until_zero(self.bytes, self.offset)
        self.offset += len(result) + 1
        return result

    def read_byte(self):
        result = read_byte(self.bytes, self.offset)
        self.offset += 1
        return result

    def read_word(self):
        result = read_word(self.bytes, self.offset)
        self.offset += 2
        return result

    def read_dword(self):
        result = read_dword(self.bytes, self.offset)
        self.offset += 4
        return result

    def eof(self):
        return self.offset >= len(self.bytes)
