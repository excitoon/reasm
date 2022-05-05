def from_bytes(bytes):
    return int.from_bytes(bytes, byteorder='little')


def read_block(bytes, offset, size):
    assert len(bytes) >= offset + size
    return bytes[offset:offset+size]


def read_block_until_end(bytes, offset):
    assert len(bytes) >= offset
    return bytes[offset:]


def read_byte(bytes, offset):
    return from_bytes(read_block(bytes, offset, 1))


def read_word(bytes, offset):
    return from_bytes(read_block(bytes, offset, 2))


def write_word(bytes, offset, data):
    bytes[offset] = data & 0xff
    bytes[offset+1] = (data >> 8) & 0xff


def read_dword(bytes, offset):
    return from_bytes(read_block(bytes, offset, 4))


def write_dword(bytes, offset, data):
    bytes[offset] = data & 0xff
    bytes[offset+1] = (data >> 8) & 0xff
    bytes[offset+2] = (data >> 16) & 0xff
    bytes[offset+3] = (data >> 24) & 0xff


def read_virtual(info, bytes, address, size):
    for section in info['sections'].values():
        if section['address'] <= address <= section['address-end']:
            return read_block(bytes, section['raw-offset'] + address - section['address'], size)
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
    return None


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
