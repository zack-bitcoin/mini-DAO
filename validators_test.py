import bitcoin as b
from pyethereum import utils

def hash_list(l):
    def g(x):
        if type(x) in [int, long]: x=utils.int_to_big_endian(x)
        return x
    y=map(lambda x: g(x), l)
    y=[utils.zpad(x, 32) for x in y]
    y=''.join(y)
    #save for pretty print z="".join("{:02x}".format(ord(c)) for c in y)
    return b.sha256(y)
def mk_acc(n):
    out={"priv":b.sha256("brainwallet"+str(n))}
    out["pub"]=b.privtopub(out["priv"])
    out["addr"]=int(utils.privtoaddr(out["priv"]), 16)
    return(out)
def mk_sig(hash, priv): return list(b.ecdsa_raw_sign(hash, priv))
def mk_mk_sig(msghash): return (lambda p: mk_sig(msghash, p["priv"]))
def add(a, b): return a+b
def add_validator(location, addr, balance, accs, new_market_cap, new_size, c, nonce):
    f=mk_mk_sig(hash_list([addr, location, balance, nonce, 1337]))
    c.update(addr, location, balance, new_market_cap, new_size, reduce(add, map(f, accs)))
def test(c):
    accs=map(mk_acc, [1,2,3])
    balance = 10000000
    add_validator(1, accs[1]["addr"], balance, accs[0:1], 2*balance, 2, c, 0)
    add_validator(2, accs[2]["addr"], balance, accs[0:2], 3*balance, 3, c, 1)

