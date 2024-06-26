import re
import binascii
import hexdump

class EMVDecoder:
    TAGS = {
        '9F02': 'Amount, Authorized (Numeric)',
        '5F2A': 'Transaction Currency Code',
        '82': 'Application Interchange Profile',
        # Add more tags based on EMV Book 3 specifications
    }

    def __init__(self):
        pass

    @staticmethod
    def validate_hex(data: str) -> bool:
        """Validate if the input string is a valid hex string."""
        hex_pattern = re.compile(r'^[0-9A-Fa-f]+$')
        return bool(hex_pattern.fullmatch(data))

    @staticmethod
    def parse_tlv(data: str):
        """Parse TLV encoded data."""
        index = 0
        tlv_dict = {}

        while index < len(data):
            tag = data[index:index + 4]
            index += 4
            length = int(data[index:index + 2], 16)
            index += 2
            value = data[index:index + (length * 2)]
            index += (length * 2)
            tlv_dict[tag] = value

        return tlv_dict

    @staticmethod
    def decode_hex(hex_data: str) -> str:
        """Decode hex data to ASCII."""
        return binascii.unhexlify(hex_data).decode('ascii', errors='ignore')

    def decode_emv_data(self, hex_data: str):
        """Decode EMV data from hex string."""
        if not self.validate_hex(hex_data):
            raise ValueError("Invalid Hexadecimal data")

        tlv_dict = self.parse_tlv(hex_data)
        decoded_data = {}

        for tag, value in tlv_dict.items():
            tag_description = self.TAGS.get(tag, 'Unknown Tag')
            decoded_value = self.decode_hex(value)
            decoded_data[tag] = {
                'description': tag_description,
                'value': value,
                'decoded_value': decoded_value
            }

        return decoded_data

    def pretty_print(self, decoded_data: dict):
        """Pretty print the decoded EMV data."""
        for tag, info in decoded_data.items():
            print(f"Tag: {tag} ({info['description']})")
            print(f"  Value: {info['value']}")
            print(f"  Decoded: {info['decoded_value']}")
            print()

if __name__ == "__main__":
    emv_data = "9F02060000000001005F2A020840"  # Sample EMV TLV data
    decoder = EMVDecoder()

    try:
        decoded = decoder.decode_emv_data(emv_data)
        decoder.pretty_print(decoded)
    except ValueError as e:
        print(e)
