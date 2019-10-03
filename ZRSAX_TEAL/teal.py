# Teal Hand Cipher

class Teal:
    def keysetup(self, key):
        s = range(256)
        j = 0
        for c, byte in enumerate(key):
            s[c] = (s[c] + ord(byte)) % 256
            j = (j + ord(byte)) % 256
        for x in range(768):
            j = (s[j] + s[c]) % 256
            s[j] = (s[j] + s[c]) % 256
            output = (s[j] + s[s[j]]) % 256   
        return s, j

    def encrypt(self, chars, key):
        ctxt = []
        c = 0
        s, j = self.keysetup(key)
        for char in chars:
            j = s[j]
            s[j] = (s[j] + s[c]) % 256
            output = (s[j] + s[s[j]]) % 256
            sub = (output + ord(char)) % 256
            ctxt.append(chr(sub))
            c = (c + 1) % 256
        return "".join(ctxt)
    
    def decrypt(self, chars, key):
        ctxt = []
        c = 0
        s, j = self.keysetup(key)
        for char in chars:
            j = s[j]
            s[j] = (s[c] + s[j]) % 256
            output = (s[j] + s[s[j]]) % 256
            sub = (ord(char) - output) % 256
            ctxt.append(chr(sub))
            c = (c + 1) % 256
        return "".join(ctxt)
