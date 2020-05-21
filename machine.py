from enigma.machine import EnigmaMachine

class ConfiguredMachine:
    def __init__(self):
        self.machine = EnigmaMachine.from_key_sheet(
            rotors='II IV V',
            reflector='B',
            ring_settings=[1, 20, 11],
            plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

    def reset(self):
        self.machine.set_display('WXC')

    def encode(self, plain_str):
        self.reset()
        return self.machine.process_text(plain_str)

    def batch_encode(self, plain_list):
        encoded = list()
        for s in plain_list:
            encoded.append(self.encode(s))
        return encoded