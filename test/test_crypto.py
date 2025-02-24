#!/usr/bin/python3 -u
"""
SPDX-License-Identifier: BSD-2
"""
import unittest

from tpm2_pytss import *
from .TSS2_BaseTest import TSS2_EsapiTest
from base64 import b64decode
from hashlib import sha256, sha384

rsa_private_key = b"""
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAxU5SokcbkKjsgBGsQhBF70LM2yudAGPUiHbLObvNJSwDcN8L
TNN1Cg1+Q4VWb/jkEFEUMCHce6Rqq3xu+kTsj+J1BVfBIkxcNr7TdDCsgNiA4BX+
kGo4W0Z5y9AGiJNb2jjim+BoYwY67fGNKv2FE3BFdWLSoQcbdDAjStLw3yJ+nhz4
Op6dJRTyu8XWxYJwXziIAHBcNFAM7ipT9Yypv5+wZ8FyQizzUj321DruGzOPPKdy
ISbRYGeyq3s8oSlui+2zIiEOb428+OWzttgwz2jfwJ8NQGXTRp1Iw/L/xottZPkA
Yobff75SOv7or+sHlMpkLjtuftEhdpWnPIjXXwIDAQABAoIBAHFplvgulXqujtsC
zZhf0EM6i5SD2khKGfWjCygRelcemI+9tbogZksz/FsFfuz4DOgQIuGT5S+xD5uo
+AWlrrD6Q7ehfKOhbvQM9nD4NYAOcu3b1qreU6yrswDjf43r3kVuo1tkP7yD7UWu
ri2C8oZ854AVIOtssWw062RsIgavw5yYG7igUVehOxQPRfP6YezYI8qTYwUy1T2i
SQMcRzT5Q8KZnfPzJFse255X55Zf5reKDEruFtIQtHZl+FeL4wjb2xSQfIXV4KFa
zRGVRuNyBKLVG8TVwLZdmL4zRWG3gHoFcVCCaIOunhHbN8lqjDj35XOKqt7BBzNx
UrOrX4kCgYEA66V3YzEc0qTdqlTza2Il/eM/XoQStitQLLykZ/+yPWAgDr0XXAtg
atVctFU61sejXsd8zBxuBk2KrZ2dbrnzxszytiA2+pFzsY8g4XwA5+7Zs8yRrMAI
S6jNuuOBjseK8PfuEaO8wNbJGYxoEJtOvBl1M/U5HreaJsahnnuFmA0CgYEA1lkW
D+Xj/SEGZY2aPVGKYvtWYzzHBm2JKLh2GpG5RZheTqwFXo6XeG2G63ZkupH/pQOg
QXMIk4Lb/y6XapulmnLXprTQRFv+6b7sLA8u5DAAWmjbrRNU+iEuxkaDnaoHjxxK
SxCcg4jQPbNmC/YRh5DOaeNJm+19HGd+gj2HhhsCgYBdoyCvv8JOScjzeFJJ53Rl
ULnLmvu8e7WeMU+7K7XuAZZ7hNQVdUfY6/OsjPmWgzn93ZNPoDRwOLvUhX8bkrS1
2JbRnDd8lfO9KLzOHPJXN2g2tCFm3d/uAKPPkbvXup8RZdOqGsBUeITsrAhmIPDG
ee9CuDz8YcTVh7SNP1Q0uQKBgF88CZ9apudKiwsH1SW1WuULgqBo2oyykiQzgNXh
NQ4E2rHdoC0Y8ZeiIjXvzmVOhOUOLV+m+oJ/u7svOjs1mGh86e+5mmck8KduGoSg
4lakNSP2PtQxKKpRn/ScU9HzP5SIH0ImyUNvwAYJ9ScPV06COhO11nifFd1O5lh7
egFNAoGAUb6hqU4FE8DO8raO+dwTZBZqrlOldF7/L8aK2Xp98jkwtUIU0WLlo3AX
BWUSCMWPt/jlmVdZPb8jFkGTlkrpy8dSlZQ1oja8nlaxjXuSy57dYRVkDUGLfvsJ
1fG6ahkXCMzRx03YPkp2Yi/ZyRIdvlwKugQNPxx+qSWCauBvUY4=
-----END RSA PRIVATE KEY-----
"""

rsa_public_key = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxU5SokcbkKjsgBGsQhBF
70LM2yudAGPUiHbLObvNJSwDcN8LTNN1Cg1+Q4VWb/jkEFEUMCHce6Rqq3xu+kTs
j+J1BVfBIkxcNr7TdDCsgNiA4BX+kGo4W0Z5y9AGiJNb2jjim+BoYwY67fGNKv2F
E3BFdWLSoQcbdDAjStLw3yJ+nhz4Op6dJRTyu8XWxYJwXziIAHBcNFAM7ipT9Yyp
v5+wZ8FyQizzUj321DruGzOPPKdyISbRYGeyq3s8oSlui+2zIiEOb428+OWzttgw
z2jfwJ8NQGXTRp1Iw/L/xottZPkAYobff75SOv7or+sHlMpkLjtuftEhdpWnPIjX
XwIDAQAB
-----END PUBLIC KEY-----
"""

rsa_public_key_bytes = b'\xc5NR\xa2G\x1b\x90\xa8\xec\x80\x11\xacB\x10E\xefB\xcc\xdb+\x9d\x00c\xd4\x88v\xcb9\xbb\xcd%,\x03p\xdf\x0bL\xd3u\n\r~C\x85Vo\xf8\xe4\x10Q\x140!\xdc{\xa4j\xab|n\xfaD\xec\x8f\xe2u\x05W\xc1"L\\6\xbe\xd3t0\xac\x80\xd8\x80\xe0\x15\xfe\x90j8[Fy\xcb\xd0\x06\x88\x93[\xda8\xe2\x9b\xe0hc\x06:\xed\xf1\x8d*\xfd\x85\x13pEub\xd2\xa1\x07\x1bt0#J\xd2\xf0\xdf"~\x9e\x1c\xf8:\x9e\x9d%\x14\xf2\xbb\xc5\xd6\xc5\x82p_8\x88\x00p\\4P\x0c\xee*S\xf5\x8c\xa9\xbf\x9f\xb0g\xc1rB,\xf3R=\xf6\xd4:\xee\x1b3\x8f<\xa7r!&\xd1`g\xb2\xab{<\xa1)n\x8b\xed\xb3"!\x0eo\x8d\xbc\xf8\xe5\xb3\xb6\xd80\xcfh\xdf\xc0\x9f\r@e\xd3F\x9dH\xc3\xf2\xff\xc6\x8bmd\xf9\x00b\x86\xdf\x7f\xbeR:\xfe\xe8\xaf\xeb\x07\x94\xcad.;n~\xd1!v\x95\xa7<\x88\xd7_'

rsa_private_key_bytes = b"\xeb\xa5wc1\x1c\xd2\xa4\xdd\xaaT\xf3kb%\xfd\xe3?^\x84\x12\xb6+P,\xbc\xa4g\xff\xb2=` \x0e\xbd\x17\\\x0b`j\xd5\\\xb4U:\xd6\xc7\xa3^\xc7|\xcc\x1cn\x06M\x8a\xad\x9d\x9dn\xb9\xf3\xc6\xcc\xf2\xb6 6\xfa\x91s\xb1\x8f \xe1|\x00\xe7\xee\xd9\xb3\xcc\x91\xac\xc0\x08K\xa8\xcd\xba\xe3\x81\x8e\xc7\x8a\xf0\xf7\xee\x11\xa3\xbc\xc0\xd6\xc9\x19\x8ch\x10\x9bN\xbc\x19u3\xf59\x1e\xb7\x9a&\xc6\xa1\x9e{\x85\x98\r"

ecc_private_key = b"""
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMJI9ujmlT/qftbXWlMwOSpkxiWLAbyIMWEFPOqTbXYMoAoGCCqGSM49
AwEHoUQDQgAEgO/tHxp/YOuP4wAV3w66C8JNiSHOKSAYtlNKSN4ZDI//wn0f7zBv
Uc7FqaRPA9LL6k6C1YfdOi/yvTB7Y4Tgaw==
-----END EC PRIVATE KEY-----
"""

ecc_public_key = b"""-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEgO/tHxp/YOuP4wAV3w66C8JNiSHO
KSAYtlNKSN4ZDI//wn0f7zBvUc7FqaRPA9LL6k6C1YfdOi/yvTB7Y4Tgaw==
-----END PUBLIC KEY-----
"""

ecc_public_key_bytes = b"\x80\xef\xed\x1f\x1a\x7f`\xeb\x8f\xe3\x00\x15\xdf\x0e\xba\x0b\xc2M\x89!\xce) \x18\xb6SJH\xde\x19\x0c\x8f\xff\xc2}\x1f\xef0oQ\xce\xc5\xa9\xa4O\x03\xd2\xcb\xeaN\x82\xd5\x87\xdd:/\xf2\xbd0{c\x84\xe0k"

ecc_private_key_bytes = b"\xc2H\xf6\xe8\xe6\x95?\xea~\xd6\xd7ZS09*d\xc6%\x8b\x01\xbc\x881a\x05<\xea\x93mv\x0c"

rsa_cert = b"""
-----BEGIN CERTIFICATE-----
MIIFqzCCA5OgAwIBAgIBAzANBgkqhkiG9w0BAQsFADB3MQswCQYDVQQGEwJERTEh
MB8GA1UECgwYSW5maW5lb24gVGVjaG5vbG9naWVzIEFHMRswGQYDVQQLDBJPUFRJ
R0EoVE0pIERldmljZXMxKDAmBgNVBAMMH0luZmluZW9uIE9QVElHQShUTSkgUlNB
IFJvb3QgQ0EwHhcNMTMwNzI2MDAwMDAwWhcNNDMwNzI1MjM1OTU5WjB3MQswCQYD
VQQGEwJERTEhMB8GA1UECgwYSW5maW5lb24gVGVjaG5vbG9naWVzIEFHMRswGQYD
VQQLDBJPUFRJR0EoVE0pIERldmljZXMxKDAmBgNVBAMMH0luZmluZW9uIE9QVElH
QShUTSkgUlNBIFJvb3QgQ0EwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoIC
AQC7E+gc0B5T7awzux66zMMZMTtCkPqGv6a3NVx73ICg2DSwnipFwBiUl9soEodn
25SVVN7pqmvKA2gMTR5QexuYS9PPerfRZrBY00xyFx84V+mIRPg4YqUMLtZBcAwr
R3GO6cffHp20SBH5ITpuqKciwb0v5ueLdtZHYRPq1+jgy58IFY/vACyF/ccWZxUS
JRNSe4ruwBgI7NMWicxiiWQmz1fE3e0mUGQ1tu4M6MpZPxTZxWzN0mMz9noj1oIT
ZUnq/drN54LHzX45l+2b14f5FkvtcXxJ7OCkI7lmWIt8s5fE4HhixEgsR2RX5hzl
8XiHiS7uD3pQhBYSBN5IBbVWREex1IUat5eAOb9AXjnZ7ivxJKiY/BkOmrNgN8k2
7vOS4P81ix1GnXsjyHJ6mOtWRC9UHfvJcvM3U9tuU+3dRfib03NGxSPnKteL4SP1
bdHfiGjV3LIxzFHOfdjM2cvFJ6jXg5hwXCFSdsQm5e2BfT3dWDBSfR4h3Prpkl6d
cAyb3nNtMK3HR5yl6QBuJybw8afHT3KRbwvOHOCR0ZVJTszclEPcM3NQdwFlhqLS
ghIflaKSPv9yHTKeg2AB5q9JSG2nwSTrjDKRab225+zJ0yylH5NwxIBLaVHDyAEu
81af+wnm99oqgvJuDKSQGyLf6sCeuy81wQYO46yNa+xJwQIDAQABo0IwQDAdBgNV
HQ4EFgQU3LtWq/EY/KaadREQZYQSntVBkrkwDgYDVR0PAQH/BAQDAgAGMA8GA1Ud
EwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggIBAGHTBUx3ETIXYJsaAgb2pyyN
UltVL2bKzGMVSsnTCrXUU8hKrDQh3jNIMrS0d6dU/fGaGJvehxmmJfjaN/IFWA4M
BdZEnpAe2fJEP8vbLa/QHVfsAVuotLD6QWAqeaC2txpxkerveoV2JAwj1jrprT4y
rkS8SxZuKS05rYdlG30GjOKTq81amQtGf2NlNiM0lBB/SKTt0Uv5TK0jIWbz2WoZ
gGut7mF0md1rHRauWRcoHQdxWSQTCTtgoQzeBj4IS6N3QxQBKV9LL9UWm+CMIT7Y
np8bSJ8oW4UdpSuYWe1ZwSjZyzDiSzpuc4gTS6aHfMmEfoVwC8HN03/HD6B1Lwo2
DvEaqAxkya9IYWrDqkMrEErJO6cqx/vfIcfY/8JYmUJGTmvVlaODJTwYwov/2rjr
la5gR+xrTM7dq8bZimSQTO8h6cdL6u+3c8mGriCQkNZIZEac/Gdn+KwydaOZIcnf
Rdp3SalxsSp6cWwJGE4wpYKB2ClM2QF3yNQoTGNwMlpsxnU72ihDi/RxyaRTz9OR
pubNq8Wuq7jQUs5U00ryrMCZog1cxLzyfZwwCYh6O2CmbvMoydHNy5CU3ygxaLWv
JpgZVHN103npVMR3mLNa3QE+5MFlBlP3Mmystu8iVAKJas39VO5y5jad4dRLkwtM
6sJa8iBpdRjZrBp5sJBI
-----END CERTIFICATE-----
"""

ecc_cert = b"""
-----BEGIN CERTIFICATE-----
MIICWzCCAeKgAwIBAgIBBDAKBggqhkjOPQQDAzB3MQswCQYDVQQGEwJERTEhMB8G
A1UECgwYSW5maW5lb24gVGVjaG5vbG9naWVzIEFHMRswGQYDVQQLDBJPUFRJR0Eo
VE0pIERldmljZXMxKDAmBgNVBAMMH0luZmluZW9uIE9QVElHQShUTSkgRUNDIFJv
b3QgQ0EwHhcNMTMwNzI2MDAwMDAwWhcNNDMwNzI1MjM1OTU5WjB3MQswCQYDVQQG
EwJERTEhMB8GA1UECgwYSW5maW5lb24gVGVjaG5vbG9naWVzIEFHMRswGQYDVQQL
DBJPUFRJR0EoVE0pIERldmljZXMxKDAmBgNVBAMMH0luZmluZW9uIE9QVElHQShU
TSkgRUNDIFJvb3QgQ0EwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAAQm1HxLVgvAu1q2
GM+ymTz12zdTEu0JBVG9CdsVEJv/pE7pSWOlsG3YwU792YAvjSy7zL+WtDK40KGe
Om8bSWt46QJ00MQUkYxz6YqXbb14BBr06hWD6u6IMBupNkPd9pKjQjBAMB0GA1Ud
DgQWBBS0GIXISkrFEnryQDnexPWLHn5K0TAOBgNVHQ8BAf8EBAMCAAYwDwYDVR0T
AQH/BAUwAwEB/zAKBggqhkjOPQQDAwNnADBkAjA6QZcV8DjjbPuKjKDZQmTRywZk
MAn8wE6kuW3EouVvBt+/2O+szxMe4vxj8R6TDCYCMG7c9ov86ll/jDlJb/q0L4G+
+O3Bdel9P5+cOgzIGANkOPEzBQM3VfJegfnriT/kaA==
-----END CERTIFICATE-----
"""

ssh_ecc_public = b"ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOhMD+1HRoFoPTyGrldrZf0iZh2HjMzpm8oNioTIVDDpxHVb1+fW31P+iz8aUAdO25Nr01aWfPPrF869Zd5d9Yw="
ssh_ecc_private = b"""
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAaAAAABNlY2RzYS
1zaGEyLW5pc3RwMjU2AAAACG5pc3RwMjU2AAAAQQToTA/tR0aBaD08hq5Xa2X9ImYdh4zM
6ZvKDYqEyFQw6cR1W9fn1t9T/os/GlAHTtuTa9NWlnzz6xfOvWXeXfWMAAAAqE5gSiZOYE
omAAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOhMD+1HRoFoPTyG
rldrZf0iZh2HjMzpm8oNioTIVDDpxHVb1+fW31P+iz8aUAdO25Nr01aWfPPrF869Zd5d9Y
wAAAAhAMBHdu575J/t4f/y9jqaPawioLJTCqQcd2MWdLcAbhPlAAAACndob0BzdmFsYW4B
AgMEBQ==
-----END OPENSSH PRIVATE KEY-----
"""

rsa_three_exponent = b"""
-----BEGIN PUBLIC KEY-----
MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAlxQ6vHpzuhFpXRkI0Xyg
nK1OR94kJlU+8On+JM1CjLpMORSAUJ+/SazftAUahmgjJ/7cnXN4P4SIDzEHGll0
wvrJS9d7ladGHYP09kjXyZex3NXUahqmn6kFAHhbdHHIDsMr1cO021gCUDKuJV3X
3T2rqtc+0ZbFhg/Rp70WSAD84kaYP5jaBDNvK3t7DhGvMvkXY6SmFt045yHyDGfg
YE1bW8Ji+NxLIXJ/PmUBOFUaV6//32ywiDM6Sri89k/AV/gFRcTVHKgVrvkkFo9M
62I2eXz60GrWEs7HHDH4JrsUSDzwvQkYflnMOtbDRkhWs8JOI9/Su/T6rcYRbgiz
XQIBAw==
-----END PUBLIC KEY-----
"""

ecc_bad_curve = b"""
-----BEGIN PUBLIC KEY-----
MEAwEAYHKoZIzj0CAQYFK4EEAA8DLAAEAH/ZAcztuiVJUsbprwXEyeHDzNscA7bn
wF24s98qYmAu3ENjz6XPl/xv
-----END PUBLIC KEY-----
"""

dsa_private_key = b"""
-----BEGIN DSA PRIVATE KEY-----
MIIBuwIBAAKBgQDWcNPSloGagE3WyinH+/vhAT0rxwyoaI7EmQguggD8z/Dq477C
F1kIWNS53jyM3e6K7iIDGqrg/StsHjM1bvp0kzAJuZqOrAmP8tqns1CbAVn9WMIc
aHw/fVvpZ4XbZ1TmvZNXtNwYil77Q1GDtw9zdqRWeyjbY10dsHjByxXUeQIVAKcD
S5p35NOrm1XX3B0ySCLVPsajAoGASLqlBGsJ4ANh5X/rxdMHMAVrDzH/XprpvqLC
qVNOrBQvoE977aNQWuZ8J+1hjGhV7BDjLoULRg6J+rH3c6YcY27ALmB1uMalrjU1
1c4XOxFQ28eFqBpVyXj1HON3Wv4IJoBxLp5+R5HfAX+N9+b6KS2ltwyozK4aBzGN
kgWTlfcCgYEAoSeNK9IG0FRNxBJAOK3wMSQlDCqUB3ZdMYw9h8AUM19E1VWHbs6v
64UzSjiUBmpttqPCQVmgJKRRrPbikVHOzMC8asEH0uIjxyxicfkhpOoSinD/9/0A
fhqkWGROM1oBkrLWlD2DNwVglcwsZlRacrXg5ubEQ18+gn3+xvLrQ0ACFEXN6I9P
0SKQIMmGu3B02XkbI5dH
-----END DSA PRIVATE KEY-----
"""

dsa_public_key = b"""
-----BEGIN PUBLIC KEY-----
MIIBtzCCASsGByqGSM44BAEwggEeAoGBANZw09KWgZqATdbKKcf7++EBPSvHDKho
jsSZCC6CAPzP8OrjvsIXWQhY1LnePIzd7oruIgMaquD9K2weMzVu+nSTMAm5mo6s
CY/y2qezUJsBWf1YwhxofD99W+lnhdtnVOa9k1e03BiKXvtDUYO3D3N2pFZ7KNtj
XR2weMHLFdR5AhUApwNLmnfk06ubVdfcHTJIItU+xqMCgYBIuqUEawngA2Hlf+vF
0wcwBWsPMf9emum+osKpU06sFC+gT3vto1Ba5nwn7WGMaFXsEOMuhQtGDon6sfdz
phxjbsAuYHW4xqWuNTXVzhc7EVDbx4WoGlXJePUc43da/ggmgHEunn5Hkd8Bf433
5vopLaW3DKjMrhoHMY2SBZOV9wOBhQACgYEAoSeNK9IG0FRNxBJAOK3wMSQlDCqU
B3ZdMYw9h8AUM19E1VWHbs6v64UzSjiUBmpttqPCQVmgJKRRrPbikVHOzMC8asEH
0uIjxyxicfkhpOoSinD/9/0AfhqkWGROM1oBkrLWlD2DNwVglcwsZlRacrXg5ubE
Q18+gn3+xvLrQ0A=
-----END PUBLIC KEY-----
"""

ecc_encrypted_key = b"""
-----BEGIN EC PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-256-CBC,3E4AA4A32C548CBB67F0D619538BE10B

kjWZRRxDAcydDyuX3p3ZIaPqa2QtI7hA0neoLbSrbdJ0mNjN63epDJYAvQpIxYv9
QuvaxyX7VW4guemvj/ZvHu3HuKr0TlvBqVtsGqIJbi3eCFvmll//qo1AG0mDAopL
I8/rxsxXVofKhAfCeJ4gP6LOlr6uLQKdf0wYxzcYEZI=
-----END EC PRIVATE KEY-----
"""


class CryptoTest(TSS2_EsapiTest):
    def test_public_from_pem_rsa(self):
        pub = types.TPM2B_PUBLIC()
        crypto.public_from_encoding(rsa_public_key, pub.publicArea)

        self.assertEqual(pub.publicArea.type, types.TPM2_ALG.RSA)
        self.assertEqual(pub.publicArea.parameters.rsaDetail.keyBits, 2048)
        self.assertEqual(pub.publicArea.parameters.rsaDetail.exponent, 0)
        self.assertEqual(bytes(pub.publicArea.unique.rsa.buffer), rsa_public_key_bytes)

    def test_private_from_pem_rsa(self):
        priv = types.TPM2B_SENSITIVE()
        crypto.private_from_encoding(rsa_private_key, priv.sensitiveArea)

        self.assertEqual(priv.sensitiveArea.sensitiveType, types.TPM2_ALG.RSA)
        self.assertEqual(
            bytes(priv.sensitiveArea.sensitive.rsa.buffer), rsa_private_key_bytes
        )

    def test_loadexternal_rsa(self):
        pub = types.TPM2B_PUBLIC.from_pem(rsa_public_key)
        self.assertEqual(pub.publicArea.nameAlg, TPM2_ALG.SHA256)
        self.assertEqual(
            pub.publicArea.objectAttributes,
            (TPMA_OBJECT.DECRYPT | TPMA_OBJECT.SIGN_ENCRYPT | TPMA_OBJECT.USERWITHAUTH),
        )
        self.assertEqual(
            pub.publicArea.parameters.rsaDetail.symmetric.algorithm, TPM2_ALG.NULL
        )
        self.assertEqual(
            pub.publicArea.parameters.rsaDetail.scheme.scheme, TPM2_ALG.NULL
        )

        priv = types.TPM2B_SENSITIVE.from_pem(rsa_private_key)

        # test without Hierarchy
        handle = self.ectx.load_external(priv, pub)
        self.assertNotEqual(handle, 0)

        # negative test
        with self.assertRaises(TypeError):
            self.ectx.load_external(TPM2B_PUBLIC(), pub)

        with self.assertRaises(TypeError):
            self.ectx.load_external(priv, priv)

        with self.assertRaises(ValueError):
            self.ectx.load_external(priv, pub, 7467644)

        with self.assertRaises(TypeError):
            self.ectx.load_external(priv, pub, object)

        with self.assertRaises(TypeError):
            self.ectx.load_external(priv, pub, session1=76.5)

        with self.assertRaises(TypeError):
            self.ectx.load_external(priv, pub, session2=object())

        with self.assertRaises(TypeError):
            self.ectx.load_external(priv, pub, session3=TPM2B_PUBLIC())

    def test_public_from_pem_ecc(self):
        pub = types.TPM2B_PUBLIC()
        crypto.public_from_encoding(ecc_public_key, pub.publicArea)

        self.assertEqual(pub.publicArea.type, types.TPM2_ALG.ECC)
        self.assertEqual(
            pub.publicArea.parameters.eccDetail.curveID, types.TPM2_ECC.NIST_P256
        )
        self.assertEqual(
            bytes(pub.publicArea.unique.ecc.x.buffer), ecc_public_key_bytes[0:32]
        )
        self.assertEqual(
            bytes(pub.publicArea.unique.ecc.y.buffer), ecc_public_key_bytes[32:64]
        )

    def test_private_from_pem_ecc(self):
        priv = types.TPM2B_SENSITIVE()
        crypto.private_from_encoding(ecc_private_key, priv.sensitiveArea)

        self.assertEqual(priv.sensitiveArea.sensitiveType, types.TPM2_ALG.ECC)
        self.assertEqual(
            bytes(priv.sensitiveArea.sensitive.ecc.buffer), ecc_private_key_bytes
        )

    def test_loadexternal_ecc(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)
        self.assertEqual(pub.publicArea.nameAlg, TPM2_ALG.SHA256)
        self.assertEqual(
            pub.publicArea.objectAttributes,
            (TPMA_OBJECT.DECRYPT | TPMA_OBJECT.SIGN_ENCRYPT | TPMA_OBJECT.USERWITHAUTH),
        )
        self.assertEqual(
            pub.publicArea.parameters.eccDetail.symmetric.algorithm, TPM2_ALG.NULL
        )
        self.assertEqual(
            pub.publicArea.parameters.eccDetail.scheme.scheme, TPM2_ALG.NULL
        )
        self.assertEqual(pub.publicArea.parameters.eccDetail.kdf.scheme, TPM2_ALG.NULL)

        priv = types.TPM2B_SENSITIVE.from_pem(ecc_private_key)

        self.ectx.load_external(priv, pub, types.ESYS_TR.RH_NULL)

    def test_loadexternal_public_rsa(self):
        pub = types.TPM2B_PUBLIC.from_pem(rsa_public_key)
        self.ectx.load_external(None, pub, types.ESYS_TR.RH_NULL)

    def test_public_to_pem_rsa(self):
        pub = types.TPM2B_PUBLIC.from_pem(rsa_public_key)
        pem = crypto.public_to_pem(pub.publicArea)

        self.assertEqual(pem, rsa_public_key)

    def test_public_to_pem_ecc(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)
        pem = crypto.public_to_pem(pub.publicArea)

        self.assertEqual(pem, ecc_public_key)

    def test_public_to_pem_bad_key(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)
        pub.publicArea.type = TPM2_ALG.NULL

        with self.assertRaises(ValueError) as e:
            pem = crypto.public_to_pem(pub.publicArea)
        self.assertEqual(str(e.exception), f"unsupported key type: {TPM2_ALG.NULL}")

    def test_topem_rsa(self):
        pub = types.TPM2B_PUBLIC.from_pem(rsa_public_key)
        pem = pub.to_pem()

        self.assertEqual(pem, rsa_public_key)

    def test_topem_ecc(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)
        pem = pub.to_pem()

        self.assertEqual(pem, ecc_public_key)

    def test_public_getname(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)
        priv = types.TPM2B_SENSITIVE.from_pem(ecc_private_key)
        handle = self.ectx.load_external(priv, pub, types.ESYS_TR.RH_NULL)
        ename = self.ectx.tr_get_name(handle)
        oname = pub.get_name()

        self.assertEqual(ename.name, oname.name)

        pub.publicArea.nameAlg = TPM2_ALG.ERROR
        with self.assertRaises(ValueError) as e:
            pub.get_name()
        self.assertEqual(str(e.exception), "unsupported digest algorithm: 0")

    def test_nv_getname(self):
        nv = TPMS_NV_PUBLIC(
            nvIndex=0x1000000,
            nameAlg=TPM2_ALG.SHA1,
            attributes=TPMA_NV.AUTHREAD | TPMA_NV.AUTHWRITE,
            dataSize=123,
        )
        oname = nv.get_name()
        nv2b = TPM2B_NV_PUBLIC(nvPublic=nv)

        handle = self.ectx.nv_define_space(b"1234", nv2b)

        ename = self.ectx.tr_get_name(handle)

        self.assertEqual(ename.name, oname.name)

    def test_public_from_pem_rsa_pem_cert(self):
        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(rsa_cert, pub)

    def test_public_from_pem_rsa_der_cert(self):
        sl = rsa_cert.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(der, pub)

    def test_public_from_pem_ecc_pem_cert(self):
        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(ecc_cert, pub)

    def test_public_from_pem_ecc_der_cert(self):
        sl = ecc_cert.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(der, pub)

    def test_public_from_pem_rsa_der(self):
        sl = rsa_public_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(der, pub)

    def test_public_from_pem_ecc_der(self):
        sl = ecc_public_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        pub = TPMT_PUBLIC()
        crypto.public_from_encoding(der, pub)

    def test_public_from_pem_bad_der(self):
        der = b"" * 1024
        pub = TPMT_PUBLIC()
        with self.assertRaises(ValueError) as e:
            crypto.public_from_encoding(der, pub)
        self.assertEqual(str(e.exception), "Unsupported key format")

    def test_private_from_pem_rsa_der(self):
        sl = rsa_private_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        sens = TPM2B_SENSITIVE()
        crypto.private_from_encoding(der, sens.sensitiveArea)

    def test_private_from_pem_ecc_der(self):
        sl = ecc_private_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        sens = TPM2B_SENSITIVE()
        crypto.private_from_encoding(der, sens.sensitiveArea)

    def test_private_from_pem_bad_der(self):
        der = b"" * 1024
        pub = TPM2B_PUBLIC()
        with self.assertRaises(ValueError) as e:
            crypto.private_from_encoding(der, pub)
        self.assertEqual(str(e.exception), "Unsupported key format")

    def test_kdfa(self):
        ekey = b"a\xe2\xb8{@f\xc0\x94\xa3Pt\x08\xf5\xaf\x01[\xce\x85t\x843\xf8\xb3\x03%q\xe5\x84x\xdc`\x81E \xf5\xa9\xe8\x9f\xc8\xc9\x96U\xbe\x1b\x07\xd9\x8f\x97*~\xf7\x9bX\x99\xbe\x86\xe7\x10g$\x9cUQT\x97\x00\x9a\x97\xfd\xf0]\xec.\xedw\xb4\xf5\x8a/)\x18D\x13W6?`{!f\xf5\xa7\xd9>E\xf7\xd66\x11j\x8aZ\x06\xe1\nJJ\x99\xb4\x9e\x15\xea\xed\xb0\x98i\xcd\xa5cI4Pq\xae\xe8\x0c6\xbae\xb1t\xe1ku\x94\x06,\xe6'\x1b\xedn\xf2T\xf7\xbd\xb4\xfeu\x7f\xacD\x9e\xcb[rHN\xf4g1C\xb3\xd9ML\xd2:\x06\xea\xb1I\x98\xa7\xe2\xa0\x99\x8b\x82\xb9n\xad\xb6\x1cZ\xa8>!\xb9\x81\xf9\x03w\x88F\n\x19\xb1^\xd8\x801\xd6\x9dF\xf3\xc3\x05\x91\x92L\xc1\xd0\xaei;\x18n\xad=v'e\xa7\xcc6\xa7\xa2\"PB\x9f\xfb\xad\xebA\x00\x8d\xee\x99\x10\xafA\xc3\xc9\xe6\xd7\xaaIe\xdf/:\xf3C{"
        key = crypto.kdfa(
            TPM2_ALG.SHA256,
            b"key data",
            b"label data",
            b"contextU data",
            b"contextV data",
            2048,
        )
        self.assertEqual(key, ekey)

        with self.assertRaises(ValueError) as e:
            key = crypto.kdfa(
                TPM2_ALG.SHA256,
                b"key data",
                b"label data",
                b"contextU data",
                b"contextV data",
                123,
            )
        self.assertEqual(str(e.exception), "bad key length 123, not a multiple of 8")

        with self.assertRaises(ValueError) as e:
            key = crypto.kdfa(
                TPM2_ALG.LAST + 1,
                b"key data",
                b"label data",
                b"contextU data",
                b"contextV data",
                2048,
            )
        self.assertEqual(
            str(e.exception), f"unsupported digest algorithm: {TPM2_ALG.LAST + 1}"
        )

    def test_kdfe(self):
        ekey = b"@|\x8bb\x92\x1c\x85\x06~\xc5d!\x14^\xb44\x01\xaf\xa2\xac(\xb98T3\x91m\x83L\xa9\xdcX"
        key = crypto.kdfe(
            TPM2_ALG.SHA256,
            b"z data",
            b"use data",
            b"partyuinfo data",
            b"partyvinfo data",
            256,
        )
        self.assertEqual(key, ekey)

        with self.assertRaises(ValueError) as e:
            key = crypto.kdfe(
                TPM2_ALG.SHA256,
                b"z data",
                b"use data",
                b"partyuinfo data",
                b"partyvinfo data",
                123,
            )
        self.assertEqual(str(e.exception), "bad key length 123, not a multiple of 8")

        with self.assertRaises(ValueError) as e:
            key = crypto.kdfe(
                TPM2_ALG.LAST + 1,
                b"z data",
                b"use data",
                b"partyuinfo data",
                b"partyvinfo data",
                256,
            )
        self.assertEqual(
            str(e.exception), f"unsupported digest algorithm: {TPM2_ALG.LAST + 1}"
        )

    def test_get_alg(self):
        alg = crypto._get_alg(TPM2_ALG.AES)
        self.assertEqual(alg, crypto.AES)

        nalg = crypto._get_alg(TPM2_ALG.LAST + 1)
        self.assertEqual(nalg, None)

    def test_symdef_to_crypt(self):
        symdef = TPMT_SYM_DEF_OBJECT(algorithm=TPM2_ALG.AES)
        symdef.mode.sym = TPM2_ALG.CFB
        symdef.keyBits.sym = 128

        (alg, mode, bits) = crypto.symdef_to_crypt(symdef)
        self.assertEqual(alg, crypto.AES)
        self.assertEqual(mode, crypto.modes.CFB)
        self.assertEqual(bits, 128)

        symdef.mode.sym = TPM2_ALG.LAST + 1
        with self.assertRaises(ValueError) as e:
            crypto.symdef_to_crypt(symdef)
        self.assertEqual(
            str(e.exception), f"unsupported symmetric mode {TPM2_ALG.LAST + 1}"
        )

        symdef.algorithm = TPM2_ALG.LAST + 1
        with self.assertRaises(ValueError) as e:
            crypto.symdef_to_crypt(symdef)
        self.assertEqual(
            str(e.exception), f"unsupported symmetric algorithm {TPM2_ALG.LAST + 1}"
        )

    def test_ssh_key_ecc(self):
        eccpub = TPM2B_PUBLIC.from_pem(ssh_ecc_public)
        self.assertEqual(eccpub.publicArea.type, types.TPM2_ALG.ECC)
        self.assertEqual(
            eccpub.publicArea.parameters.eccDetail.curveID, types.TPM2_ECC.NIST_P256
        )

        eccsens = TPM2B_SENSITIVE.from_pem(ssh_ecc_private)
        self.assertEqual(eccsens.sensitiveArea.sensitiveType, types.TPM2_ALG.ECC)

    def test_topem_encodings(self):
        pub = types.TPM2B_PUBLIC.from_pem(ecc_public_key)

        pem = pub.to_pem(encoding="PEM")
        self.assertTrue(pem.startswith(b"-----BEGIN PUBLIC KEY-----"))

        der = pub.to_pem(encoding="der")
        self.assertTrue(der.startswith(b"0Y0\x13\x06\x07"))

        ssh = pub.to_pem(encoding="ssh")
        self.assertTrue(ssh.startswith(b"ecdsa-sha2-nistp256"))

        with self.assertRaises(ValueError) as e:
            pub.to_pem(encoding="madeup")
        self.assertEqual(str(e.exception), "unsupported encoding: madeup")

    def test_rsa_exponent(self):
        pub = TPMT_PUBLIC.from_pem(rsa_three_exponent)
        self.assertEqual(pub.parameters.rsaDetail.exponent, 3)

        key = crypto.public_to_key(pub)
        nums = key.public_numbers()
        self.assertEqual(nums.e, 3)

    def test_ecc_bad_curves(self):
        with self.assertRaises(ValueError) as e:
            pub = TPMT_PUBLIC.from_pem(ecc_bad_curve)
        self.assertEqual(str(e.exception), "unsupported curve: sect163r2")

        pub = TPMT_PUBLIC.from_pem(ecc_public_key)
        pub.parameters.eccDetail.curveID = TPM2_ECC.NONE
        with self.assertRaises(ValueError) as e:
            pub.to_pem()
        self.assertEqual(str(e.exception), "unsupported curve: 0")

    def test_unsupported_key(self):
        sl = dsa_private_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        der = b64decode(b64)

        with self.assertRaises(RuntimeError) as e:
            priv = TPMT_SENSITIVE.from_pem(der)
        self.assertEqual(str(e.exception), "unsupported key type: _DSAPrivateKey")

        with self.assertRaises(RuntimeError) as e:
            pub = TPMT_PUBLIC.from_pem(dsa_public_key)
        self.assertEqual(str(e.exception), "unsupported key type: _DSAPublicKey")

    def test_from_pem_with_symmetric(self):
        sym = TPMT_SYM_DEF_OBJECT(algorithm=TPM2_ALG.AES)
        sym.keyBits.aes = 128
        sym.mode.aes = TPM2_ALG.CFB
        pub = TPMT_PUBLIC.from_pem(ecc_public_key, symmetric=sym)

        self.assertEqual(pub.parameters.asymDetail.symmetric.algorithm, TPM2_ALG.AES)
        self.assertEqual(pub.parameters.asymDetail.symmetric.keyBits.aes, 128)
        self.assertEqual(pub.parameters.asymDetail.symmetric.mode.aes, TPM2_ALG.CFB)

    def test_from_pem_with_scheme(self):
        scheme = TPMT_ASYM_SCHEME(scheme=TPM2_ALG.ECDSA)
        scheme.details.ecdsa.hashAlg = TPM2_ALG.SHA256
        pub = TPMT_PUBLIC.from_pem(ecc_public_key, scheme=scheme)

        self.assertEqual(pub.parameters.asymDetail.scheme.scheme, TPM2_ALG.ECDSA)
        self.assertEqual(
            pub.parameters.asymDetail.scheme.details.ecdsa.hashAlg, TPM2_ALG.SHA256
        )

    def test_public_from_private(self):
        pub = TPMT_PUBLIC.from_pem(rsa_private_key)
        self.assertEqual(pub.type, types.TPM2_ALG.RSA)
        self.assertEqual(pub.parameters.rsaDetail.keyBits, 2048)
        self.assertEqual(pub.parameters.rsaDetail.exponent, 0)
        self.assertEqual(pub.unique.rsa, rsa_public_key_bytes)

        pub = TPMT_PUBLIC.from_pem(ecc_private_key)
        self.assertEqual(pub.type, types.TPM2_ALG.ECC)
        self.assertEqual(pub.parameters.eccDetail.curveID, types.TPM2_ECC.NIST_P256)
        self.assertEqual(pub.unique.ecc.x, ecc_public_key_bytes[0:32])
        self.assertEqual(pub.unique.ecc.y, ecc_public_key_bytes[32:64])

    def test_public_from_private_der(self):
        sl = rsa_private_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        rsader = b64decode(b64)

        pub = TPMT_PUBLIC.from_pem(rsader)
        self.assertEqual(pub.type, types.TPM2_ALG.RSA)
        self.assertEqual(pub.parameters.rsaDetail.keyBits, 2048)
        self.assertEqual(pub.parameters.rsaDetail.exponent, 0)
        self.assertEqual(pub.unique.rsa, rsa_public_key_bytes)

        sl = ecc_private_key.strip().splitlines()
        b64 = b"".join(sl[1:-1])
        eccder = b64decode(b64)

        pub = TPMT_PUBLIC.from_pem(eccder)
        self.assertEqual(pub.type, types.TPM2_ALG.ECC)
        self.assertEqual(pub.parameters.eccDetail.curveID, types.TPM2_ECC.NIST_P256)
        self.assertEqual(pub.unique.ecc.x, ecc_public_key_bytes[0:32])
        self.assertEqual(pub.unique.ecc.y, ecc_public_key_bytes[32:64])

    def test_encrypted_key(self):
        pub = TPMT_PUBLIC.from_pem(ecc_encrypted_key, password=b"mysecret")
        self.assertEqual(pub.type, TPM2_ALG.ECC)

        priv = TPMT_SENSITIVE.from_pem(ecc_encrypted_key, password=b"mysecret")
        self.assertEqual(priv.sensitiveType, TPM2_ALG.ECC)

        with self.assertRaises(ValueError):
            TPMT_PUBLIC.from_pem(ecc_encrypted_key, password=b"passpass")

    def test_keyedhash_from_secret(self):
        secret = b"secret key"
        scheme = TPMT_KEYEDHASH_SCHEME(scheme=TPM2_ALG.HMAC)
        scheme.details.hmac.hashAlg = TPM2_ALG.SHA256
        (sens, pub) = TPM2B_SENSITIVE.keyedhash_from_secret(secret, scheme=scheme)

        self.assertEqual(pub.publicArea.type, TPM2_ALG.KEYEDHASH)
        self.assertEqual(pub.publicArea.nameAlg, TPM2_ALG.SHA256)
        self.assertEqual(
            pub.publicArea.parameters.keyedHashDetail.scheme.scheme, TPM2_ALG.HMAC
        )
        self.assertEqual(
            pub.publicArea.parameters.keyedHashDetail.scheme.details.hmac.hashAlg,
            TPM2_ALG.SHA256,
        )
        self.assertEqual(sens.sensitiveArea.sensitiveType, TPM2_ALG.KEYEDHASH)
        self.assertEqual(sens.sensitiveArea.sensitive.bits, secret)

    def test_keyedhash_from_secret_unseal(self):
        secret = b"sealed secret"
        seed = b"\xF1" * 32
        (sens, pub) = TPM2B_SENSITIVE.keyedhash_from_secret(
            secret, objectAttributes=TPMA_OBJECT.USERWITHAUTH, seed=seed
        )

        handle = self.ectx.load_external(sens, pub, types.ESYS_TR.RH_NULL)
        sealdata = self.ectx.unseal(handle)

        self.assertEqual(sens.sensitiveArea.seedValue, seed)
        self.assertEqual(sealdata, secret)

    def test_keyedhash_from_secret_bad(self):
        secret = b"1234"

        with self.assertRaises(ValueError) as e:
            TPMT_SENSITIVE.keyedhash_from_secret(secret, nameAlg=TPM2_ALG.NULL)
        self.assertEqual(str(e.exception), "unsupported digest algorithm: 16")

        with self.assertRaises(ValueError) as e:
            TPMT_SENSITIVE.keyedhash_from_secret(secret, seed=b"bad seed")
        self.assertEqual(str(e.exception), "invalid seed size, expected 32 but got 8")

    def test_symcipher_from_secret(self):
        secret = b"\xF1" * 32

        sens, pub = TPM2B_SENSITIVE.symcipher_from_secret(secret)

        self.assertEqual(sens.sensitiveArea.sensitiveType, TPM2_ALG.SYMCIPHER)
        self.assertEqual(sens.sensitiveArea.sensitive.bits, secret)

        self.assertEqual(pub.publicArea.type, TPM2_ALG.SYMCIPHER)
        self.assertEqual(pub.publicArea.parameters.symDetail.sym.keyBits.sym, 256)
        self.assertEqual(
            pub.publicArea.parameters.symDetail.sym.algorithm, TPM2_ALG.AES
        )
        self.assertEqual(pub.publicArea.parameters.symDetail.sym.mode.sym, TPM2_ALG.CFB)

        self.ectx.load_external(sens, pub, ESYS_TR.RH_NULL)

    def test_symcipher_from_secret_bad(self):
        with self.assertRaises(ValueError) as e:
            TPMT_SENSITIVE.symcipher_from_secret(b"\xFF" * 17)
        self.assertEqual(
            str(e.exception), "invalid key size, expected 128, 192 or 256 bits, got 136"
        )

        with self.assertRaises(ValueError) as e:
            TPMT_SENSITIVE.symcipher_from_secret(b"\xFF" * 32, algorithm=TPM2_ALG.SM4)
        self.assertEqual(str(e.exception), "invalid key size, expected 128, got 256")

        with self.assertRaises(ValueError) as e:
            TPMT_SENSITIVE.symcipher_from_secret(b"\xFF" * 32, seed=b"1234")
        self.assertEqual(str(e.exception), "invalid seed size, expected 32 but got 4")

    def test_verify_signature_hmac(self):
        secret = b"secret key"
        scheme = TPMT_KEYEDHASH_SCHEME(scheme=TPM2_ALG.HMAC)
        scheme.details.hmac.hashAlg = TPM2_ALG.SHA256
        (sens, pub) = TPM2B_SENSITIVE.keyedhash_from_secret(
            secret,
            scheme=scheme,
            objectAttributes=(TPMA_OBJECT.SIGN_ENCRYPT | TPMA_OBJECT.USERWITHAUTH),
        )

        handle = self.ectx.load_external(sens, pub, types.ESYS_TR.RH_NULL)

        msg = b"sign me please"
        h = sha256(msg)
        sigdig = h.digest()
        sig = self.ectx.sign(
            handle,
            sigdig,
            TPMT_SIG_SCHEME(scheme=TPM2_ALG.NULL),
            TPMT_TK_HASHCHECK(tag=TPM2_ST.HASHCHECK, hierarchy=TPM2_RH.NULL),
        )
        crypto.verify_signature(sig, secret, msg)

    def test_verify_signature_ecc(self):
        template = TPM2B_PUBLIC.parse(
            "ecc:ecdsa_sha256",
            objectAttributes=(
                TPMA_OBJECT.USERWITHAUTH
                | TPMA_OBJECT.SIGN_ENCRYPT
                | TPMA_OBJECT.SENSITIVEDATAORIGIN
            ),
        )
        handle, public, _, _, _ = self.ectx.create_primary(
            TPM2B_SENSITIVE_CREATE(), template
        )

        msg = b"sign me please"
        h = sha256(msg)
        sigdig = h.digest()
        sig = self.ectx.sign(
            handle,
            sigdig,
            TPMT_SIG_SCHEME(scheme=TPM2_ALG.NULL),
            TPMT_TK_HASHCHECK(tag=TPM2_ST.HASHCHECK, hierarchy=TPM2_RH.NULL),
        )

        crypto.verify_signature(sig, public, msg)

    def test_verify_singature_rsapss(self):
        template = TPM2B_PUBLIC.parse(
            "rsa2048:rsapss-sha384:null",
            objectAttributes=(
                TPMA_OBJECT.USERWITHAUTH
                | TPMA_OBJECT.SIGN_ENCRYPT
                | TPMA_OBJECT.SENSITIVEDATAORIGIN
            ),
        )
        handle, public, _, _, _ = self.ectx.create_primary(
            TPM2B_SENSITIVE_CREATE(), template
        )

        msg = b"sign me please"
        h = sha384(msg)
        sigdig = h.digest()
        sig = self.ectx.sign(
            handle,
            sigdig,
            TPMT_SIG_SCHEME(scheme=TPM2_ALG.NULL),
            TPMT_TK_HASHCHECK(tag=TPM2_ST.HASHCHECK, hierarchy=TPM2_RH.NULL),
        )

        crypto.verify_signature(sig, public, msg)

    def test_verify_singature_rsassa(self):
        template = TPM2B_PUBLIC.parse(
            "rsa2048:rsassa-sha256:null",
            objectAttributes=(
                TPMA_OBJECT.USERWITHAUTH
                | TPMA_OBJECT.SIGN_ENCRYPT
                | TPMA_OBJECT.SENSITIVEDATAORIGIN
            ),
        )
        handle, public, _, _, _ = self.ectx.create_primary(
            TPM2B_SENSITIVE_CREATE(), template
        )

        msg = b"sign me please"
        h = sha256(msg)
        sigdig = h.digest()
        sig = self.ectx.sign(
            handle,
            sigdig,
            TPMT_SIG_SCHEME(scheme=TPM2_ALG.NULL),
            TPMT_TK_HASHCHECK(tag=TPM2_ST.HASHCHECK, hierarchy=TPM2_RH.NULL),
        )

        sig.verify_signature(public, msg)

    def test_verify_signature_bad(self):
        badalg = TPMT_SIGNATURE(sigAlg=TPM2_ALG.NULL)
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(badalg, b"", b"")
        self.assertEqual(str(e.exception), "unsupported signature algorithm: 16")

        hsig = TPMT_SIGNATURE(sigAlg=TPM2_ALG.HMAC)
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(hsig, str("not bytes"), b"1234")
        self.assertEqual(
            str(e.exception), "bad key type for 5, expected bytes, got str"
        )

        hsig.signature.hmac.hashAlg = TPM2_ALG.NULL
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(hsig, b"key", b"1234")
        self.assertEqual(str(e.exception), "unsupported digest algorithm: 16")

        badecc = TPMT_SIGNATURE(sigAlg=TPM2_ALG.ECDSA)
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(badecc, str("bad"), b"1234")
        self.assertEqual(
            str(e.exception), "bad key type for 24, expected ECC public key, got str"
        )

        ecckey = TPM2B_PUBLIC.from_pem(ecc_public_key)
        badecc.signature.ecdsa.hash = TPM2_ALG.NULL
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(badecc, ecckey, b"1234")
        self.assertEqual(str(e.exception), "unsupported digest algorithm: 16")

        badrsa = TPMT_SIGNATURE(sigAlg=TPM2_ALG.RSAPSS)
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(badrsa, str("bad"), b"1234")
        self.assertEqual(
            str(e.exception), "bad key type for 22, expected RSA public key, got str"
        )

        badrsa.signature.rsapss.hash = TPM2_ALG.NULL
        rsakey = TPM2B_PUBLIC.from_pem(rsa_public_key)
        with self.assertRaises(ValueError) as e:
            crypto.verify_signature(badrsa, rsakey, b"1234")
        self.assertEqual(str(e.exception), "unsupported digest algorithm: 16")

        badrsa.signature.rsapss.hash = TPM2_ALG.SHA256
        with self.assertRaises(crypto.InvalidSignature):
            crypto.verify_signature(badrsa, rsakey, b"1234")

        badrsa.sigAlg = TPM2_ALG.RSASSA
        with self.assertRaises(crypto.InvalidSignature):
            crypto.verify_signature(badrsa, rsakey, b"1234")


if __name__ == "__main__":
    unittest.main()
