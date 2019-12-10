#!/usr/bin/env python
'''
Module to make extra options available for other modules

DEFINED EXIT :: none
'''


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt(
        'operations', '-pa', '--panda',
        action='store_const', const='misc.op_show_panda', dest='operation',
        help='Save the panda bears')

    # Group: misc
    opts.opt(
        'misc', '-y', '--yes',
        action='store_true', dest='misc_yes',
        help='Prevents prompting the user for confirmation')

    opts.opt(
        'misc', '-k', '--insecure',
        action='store_true', dest='misc_insecure',
        help='Ignore SSL errors when connecting to API')

    opts.opt(
        'misc', '-v', '--verbose',
        action='store_true', dest='misc_verbose',
        help='Provide more verbose output from searches')


##
# HOOK FUNCTIONS
##

def op_show_panda(d42):
    '''Display a panda?'''
    # Loading modules here that are not required for anything else. This is a non-essential function.
    import base64
    import random
    import zlib

    the_blob = 'eJy91E0OgyAQBeC9p5idbdLIBbrgICSDF+gJJpy9/GhtnSfQxvS50Gj8eCpi7WkZqlfHEAKlxL3/3RoJpQpiC0MtD' \
            'lk1qaZpqyUda8rqoQ6wvdVHYWxvdVJEbau3Fiy2s7opVOz/1uN2lsWGhPgUy8QP4kfztTUr6Z4Xikl94Llp6WJFEXVe' \
            'U8raFePl0ZQFaun/cQaSn/zUpsA6UTCOMZSezzHHWsI5NQquX3NkMpUTDx2ljQrME5awFZFLumd0pQxfHQu/Xpk7oJA' \
            'lK6Gm55KQAsRBn5a1wYaCGLEmbEnGkG96Hyj9MGUOCJhWa+K1z6HE2ifVsJJJ'
    a_blob = 'eJyVVTuO3DAM7X0KdrIDmOwDTLFVsMViLyBAvsFeQIcPvzKldYKElgayyMfPo+QBeJDWGuKJ5xkTkbe21YptTrjwQn' \
            '6Rn5giilkQ5L5DKr/qtFfR1gXSZUoSIXccyUzVK4TVvbCrSMWD2Cx/g7DBdaImkgp6gpDuFTVkxNfBrmn/GoFUPRWDB' \
            'QLjifEOFJyp6/ybUMwYpkhssDd8vbAdU1UdbRV9YWa2FDeFdv1LRUtN0W2YBY9SRwFkzbu9SO7QW+fhiSWOdWBpaAF7' \
            'cEcGu+kmifJyER6r58LLSwbUHe1gAPx0NzuU3DVsj4KlRrUHXHCoS54E5NlUN5ACSj5ik2AR1KkhiSAajsW9tFrt4Jq' \
            'rt4/3X28An/784EcuiMTwtMnj7wzTNkJhf/25isYKpkjgjcjvkzdDVuO0MhmxpKG14izQFk2rydwxiZsbqbxoK7cRT0' \
            '9HDw4yvGekmZACNkuXH4RDNYbKDiBjKRKV6FsHeSpfKK8mcl09OFhuCGAVhGZuqzrSCvjiYoQWVJd0NfAmFdTm8Jz67' \
            'IOs4O70VrKKnz5/Ty56V20QzvhG44CZBCPfPBianPP5+0nTGjPzgoobvcDi4hgqOu88904F28hmCjc+uKzOofP5GLZT' \
            'dXxF9E7lMt1ueV9oMed3g9L+hGS/K/CPcv9vWEb/iosq+FvR/gPlJQjsN2YfbL8='
    blob_1 = 'eJylmM1O4zAQgO88hd14KeRQLiCRKGqiSs2yLK5QAMUHDhVbVlv1uK1Ucciz78w4cZ1snB8YQePGmS/j8cx4VM6/Jm' \
            'fttwtWyvQzAGbLejSgps7C0RZovRlIGPUpuwE4KEA+Dai5wIxbeX2AunwSwHnoNqIJKFoAGAt/XDacOfU3QmztWJgNA' \
            'fy21UFWtfeG/YCGvhA7p/NaAWYB16ISRHVmhAHUdtzoiwT+54MA9v5NRU2WwyywRK/ArwDZIEBoAQK9ej7KAj6vA1I2' \
            'wZW8xjh069u7ADbc4wsfCDCnb+n0GofDAEAIdPjcawCuA2911rVaHISx5fsDuNFjzPd9MMBdGeqRGGaoqlQF4XdS3Er' \
            'Kp8KxjmY2akVJn6nCaya5eLPDebNRHQCONgTJgt4vSRC6NMV1jzOLDgCPwIGxRybkaqJyHHg4cYs3Xp79OqHtXBA77b' \
            'Rcx6Fnry6rvNMJEFkutkWS1eu6WFTauMtdAC5WXnbzXwDGfm70004LyJOPlJbXDdOaC3AerihlZrYAcpRegEmuE8IO1' \
            'Goj3AArvddVJK++e773A1GZyHoArCHEKJoecAPaDpg13lw3GoY2gGrXr6QfUOnPrG6B8XA2HFCYBxk7JtXeqbZH3T0S' \
            'pJ9SRYQFCnYPr/FQAOlDGsCffHoW3vM2X+X59rJV39VkVV9iWE2woKgWV58BcFLdHQ6HWSBHLaEw49lx8/72vlWxPww' \
            'AKlhTd7qtCO/kKfoHAcjkR0z8X4hQciRAh0qpwNje1h8OiIyGVGIcQNcAUzgWSo4ElMFuOgNu62e9gEIDpqfaNe91QW' \
            'uLo6r8Ea+2Be0HrAGUJfBYLZ8+g/KbB/v6c5gFazo84vBou0B5zhW0LiEqT7VKf5a4XWA70apZe3K6iQb3HjRbnLKQk' \
            'U+qIOR64NB3l/VI6aN0qQHL0YDyxRjOuJbU9dgAgNx1rKAXsMQ+C6qqs9NzA3QipXTlEFJjARe6lmBJget2MxJwJ+84' \
            '1YI5T8SSAinEHBsEOEDWyH0ZRhFqSSRMeCDOCbV6aQMUH+KBrrfwKI/LPch4wJh8klmWYINmqt2JcbJAiHN0WpJRK7n' \
            'ikw04n7/SGfGB9uxR/5vpUsrDwwAUvOqvuGAsKacXMbwUEiTFLPkGG5pJvJIROZglVR0QwGOKlzZCStwkeJbNMTfhXZ' \
            'DPCu4qPQ/q/mVS1AHeEW4z9pjQvNyISznHd19giYL5FCYvdc0nDGNZcxdwNiV+nAt9PqI2i2lI7QV03gw2BW9obH0bA' \
            'ay0c6wGRU/QR2SN4RI2AAU9ceWTsj+h81UrFbMIZ2FEOvVj3i5p5SA8ld/T6Or1pDMvrJ9mOlrdYfJlwD9I3MX0'
    blob_2 = 'eJydmEtv2zgQgO/5FaQ0XbkByhw2ARJCkIwUmy2aMAgEFNGRcF2jQQ65ZAFhYfC37wxfImXJdZdIbD04n+bF4cicLw' \
            '3N/NCLU3CcLd5h6TD/AyAyAtMLjGUA5xLlahOHnNVjGWBSYT/Y6QDDDqQTgtH6OGDm4SnBeeUIwDl+mcASwizAsCOIa' \
            'ozwEsCwYbOIkGwE6HnAjm0B3Ayh543wgGoewHpwAOQ8ziiBOjRHARXKQ0PiNB5mAGHUswB2Q3ICwtgcmBEB805kMB1i' \
            'VnoxjBXcMbSiLEfCq54DVEuAjokKdiLThJ2qwUeh6zvGLv9ihfNFGN/1KYAL1LwoPzAGFKfMDwWrTjDBoKqwkYyiyOp' \
            'E/Cnm5VSBCaCrTAvA2UsnxjhCyeZGPQPg5xIfUnL5Du0o/7Z2ocjlJZ8DcMXIWez6IBcA+kw+SkzDWMHm7Ucm+PwBNv' \
            'ildrPyHmDEP0kkcvdbZyqVuq/iE8AWp9zHS4n5paZo7lQxGj5RgADGzu3e4SVclGylC+1kLsHpLqT3mzwwwWfcnwB/+' \
            'Iv7ofUVhV3cdHX0j//OjECAcoD9duNqtdlCaTBqgk6aLtlNwoNlQjgLbsNP5SbjUnz+fvPIciE3wnYg4i5FTvRJq6oO' \
            '75v+eRA9vELjn5YBuAyCwowAzguS76ng8t4HoGvCzGGQqxXmV0DojGwBzXpFIooMc0F8KrbwQhuyEesQ0+vrL8PKYur' \
            'EL04DDMSPYSAFzJeHlRievcz6MUuqjvIBic/4fJloQOmhtWb0vLGKrFwJoUmtUqrDP4rrDTy1D+JrmzhRCiHkMHA2XA' \
            'NPk9iE1JFOczqrisHffuyjBpULAtWwPqljPcUwZhHnK7uvqi6bYQGXwUTVxmN7v8fkCxnjrenRlnHGvQU01kacjS6o0' \
            '0qoSAUsblqPi7jHqUQ4d1Ma50SBLhTerSZVgbO8W8NURPmGCN3j27dbmNsXEg2Bh2ZAJssY3ULaF9fwJOcAzVUC4KFd' \
            'cRuyj11ND1m1SSJlg406SPRDqEFpKTKdj8F8hxKr2n0famkVS5G2HWeLhK5fAkCfbKwOoFNn0hzZmmK/CIDbPgJ2YRc' \
            'ZAVnzPQdIqmpolvhUg6OANJJ3hwD+awCPPkh6yrGynwDwiHQ/cKu2Ppi43K1LOb4xHMotASjGsfqFdnBq9hLAvGAl2/' \
            'xtbd98s5d+DwCT8dLzi9ffALyrUq4njA1sm+MuSAC666c6ANwA/9evml+bIPjVIYHK7P2y+CQKrZoF3A7Lr40RYB5w0' \
            'k6IouzKlrLo6TMtie4jlLb8PXz6HOLrColxpT4CrKdrpWp832B7sdItLTvs+RlzRQGXv6J4aMVCobzIAXssRXRPWpbt' \
            'Q/Z2NXL6aLdAk+zioncqIzE8TQYwDXH5fuyEmFuNl7SkUY0aL1i9uC2OOQBv+ubHpg2uAsEtAM+oUd1a1DmRrhpnb+M' \
            'S7CwogAbbdUdX93SPHgju9YYSpLVHZn2rfHFl2TtT7UqnXXlNXAJwRZ+ua7b3eKeKGo+KaEGiAd52k0g32gnJ5XiESC' \
            'rie3v4ibsfJnhc5B5Q2apRkXNkKCBumsTzuiiotEhjvVf5BSZ5DsBzfKeog3Ma41Ty3rIXf2q7R1HXG38J8ICfkvRx+' \
            '6sMbQX902VBzYu76l77Y3+D4z937BG5'
    blob_3 = 'eJydmFtr2zAUx9/3KSRbm9uwubCVdTEiDoOVQKc8uAsRow9mS8dKHrpBA6UP+uw7kqy7nMtUaFxH/5+OzkU+LsbREH1' \
            '8Z+94FcsRQpX9Q5wMkHqE4ssTAEokTRD26n8AyOgPGzACMHr6vwB0tAHjgN3uKH0SRoTmZBhv0IaQNT8RgNGUROMUwN' \
            'MKFowBNycAmBR8lL86pVXWdCcAnPmUM8bak7fA3cYlgBngA5eFIXK1ETnRAh5gP4w5RwTp0fcuxFlAJ0O53KweTUivU' \
            'TJGAHgymVx/cAuX6lcqd3WW5AHEkoxYrhO0Dm3IAPboG3W39k3IAIqJ8sOk6PN6Qr56JqQA395BsHzUi9o0me0BePog' \
            'oZdf/RujAOHpP5FoPLjLbR7gy1EV6/3xOQMQgfwAgGQAScjzyqIYA+AmArSR9FpJq9eo1ACa+CCOe3g2XVekGtzHFAC' \
            'nTow3UfqAGSrVrt4gdEnIRl6mYYwJRQBQbsF4tcLD7jJ5EPsBdUHk4HibK91WFvqXDCA1wkVzizbfhknTL8aAXDENyk' \
            '0awjXZygnPhDwZfQ6AsSodlujtI4fcwimD9wCUL3pNKM931Twirb2jegQgGXXBBhcuz7yAlj9I4U0bB8hBi9ZA7lfvr' \
            '66uVi/z6EGxH6At6UXRtu1vVAKrK8/Drw8DhtGq0KQdhwUMxRz3ePA06r0aScGvArmPEHFt5VfQgHRKVjzkZgpwXzWG' \
            'oG/UdVPDiBEiAgQ79D/1TBHrg30kgOflsxaqO00fbcYz0gJm/ubuViXZqqf7y0/YQtr4CbdWFgA5x8gNkfWGOfyMOLI' \
            'Z24KQZ813KLYp7jDDgmYJTp76QEANKjPKzXrBbzGND6naVw+AmdsBHM0tw52CdNBl3UGrtLAIvkw7LpUH9aDX8RWqPZ' \
            'JNGm70BVvwZ8gGurpK9CaVIVt80ygUoOj5grmB72QXOQoIh1T6YqmnCwkoXsjngwDOrOHN2dk5dhAiD+PuIOBCTr7l4' \
            'IsCivncADvdN7ZHbAFdagmHTHJ+6OAnMzkDoDIjWHZkXh6yTlRBzRKOBOjMEok83v8oALuCg3Nd2dLmxClgSPf+nV+x' \
            '/rU6oOpRwFuvZryShxexbbCEfNA8hAD+KG96AP/MwKDQ/j+jFkCWu94CzItKCNDFIXDTNPBs5P1u3hFngbFCAsQHHwA' \
            '8zHQYpJw/4QWHfKKyI2AawPlUv0owDbjUT921BkzJkjO7CQi9iYBZX0+CnqeUiaW2oPoVY4H8znnB29Iv8nKvr+7vZR' \
            '/dzawPINGJNINqgHnFwTOt39Af6pMNfb5+m2RsJmwUIMsFQCrlO7MiNQBcluoCTjt9qDN4s5oUfhgvMGuAUnkGCxf2v' \
            '+KP/JAW6xlMmvo2SqSmuSgcQOgYVsGpbgFqxADsfX1n+wj/yaaWcUvQHEC93gYHfy30oMP8ptd/23qImu06818TyMT0' \
            'ph1H90hj4x96yevJ'
    blobby = 'eJxVU8luwjAQvfMVEzhEimJb7aGHiiJRiQNSoVKhJ8w4V/5h5G/vbCbpSHjJPL95swAw2xhCKEVWPfASVwtvn9i27/' \
            'Ch13sWmxYI9uojrHW9XteKysKg1YwYe9kvcIAzHOEbfuQ6xRmTADJvjchJ3OGgNEa+KFWKKjZmpWHMGB2VknzR4+l0g' \
            'hGj7pYJPzdYEoIIHAc1IH/SkMixQVwNB9DvRJkI61GV4WTSEmxFigGzgktAgKunJEH3ABiKeU1fNh1Ho0Qxozubbocx' \
            'LmtrEJaGIWqghnpYQUaUvmFN2Q7RivJwFFllaDPRFAmIhiHDkEI2r6M6XfvdhkBxFEIaIA+aJXStCY2LCm0KERU3JWt' \
            'NaDkADPIjkrBMTOYx2KNllV3P7S5xGebvPQF6pp9VUao1q8IG8xQEl6z3vMZUbveS46QDM/b5ietM4KS1RE+AUKrdm+' \
            'qu9conSedRYTqd+o1p514xWdHj5fd43X9+HexdEcKGMjKsPF2tZoVHraKSzf8ndKr/xl1dLe/Cw2PzAm/wqqNU//sXI' \
            'ZfkS1/4AxFM0C8='
    blobber = 'eJyVlMEOwiAMhu8+BTc0ZuUuupOPsGMT4tGL+gDEZxcKA7ZRJiyBrqxff8pAiJ1mutqhDYNB1pNwARKaRKjjhLBMI' \
            'j/VILI8F8ZHsUSz4X3yHBplKv4GcYsrdPk56wtW17shGgPMamOkSjbuEQ0PI2kTEW7UzmGgDBMsvpuJWmu8uMbypNOC' \
            'UWHSRQ6bC7AiWp5I0h0F1RwWR+/wdsEsiIojxlJYkUqXa4eznTdqsTNSglmfhlTa+m5gsiOz8vd4bH67pvNqqR8LOzi' \
            'yPTLEkC9Aj8UNYP+wT61TGBaBrsD3x+vphrfWe73iNUbmV/Q+bSLp7Ea2iY45QN99Cz8H3Bf9'

    if d42.opts.misc_verbose:
        r = random.randint(1, 3)
        if r == 1:
            blob = blob_1
        elif r == 2:
            blob = blob_2
        else:
            blob = blob_3
    elif d42.opts.misc_yes:
        r = random.randint(1, 3)
        if r == 1:
            blob = a_blob
        elif r == 2:
            blob = blobby
        else:
            blob = blobber
    else:
        blob = the_blob

    print(zlib.decompress(base64.b64decode(blob)))
