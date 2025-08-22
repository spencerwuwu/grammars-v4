#!/usr/bin/env python3
import sys
from pyformlang.cfg import CFG
from pyformlang.cfg.llone_parser import LLOneParser
from pyformlang.regular_expression import Regex

from antlr4 import *
from driver.MimeLexer import MimeLexer
from driver.MimeParser import MimeParser

def get_cfg(cfg_f, verbose=False):
    with open(cfg_f, "r") as f:
        cfg = CFG.from_text(f.read())

    if verbose:
        print(cfg.to_text())

    return cfg

def print_pda(pda):
    for key, val in pda.to_dict().items():
        key = list(key)
        state = key[0]
        readin = key[1]
        stacktop = key[2]
        print(state.value, 
              readin.value, 
              stacktop.value)
        for v in val:
            v = list(v)
            next_state = v[0]
            new_stacktop = v[1]
            print("    |", next_state, new_stacktop)




def main(argv):

    cfg = get_cfg("cfg.txt", verbose=False)

    input_stream = FileStream(argv[1])
    lexer = MimeLexer(input_stream)
    input_tokens = []
    for token in lexer.getAllTokens():
        token_name = lexer.symbolicNames[token.type] or f"'{lexer.literalNames[token.type]}'"
        #print(f"Token: {token_name}, Text: '{token.text}', Line: {token.line}, Column: {token.column}")
        input_tokens.append((token_name, token.text))

    s = [t[0].lower() for t in input_tokens]
    print(s)

    print(cfg.contains(s))

    # Convert into a PDA accepting by final state
    pda_empty_stack = cfg.to_pda()

    print("-------------------------")
    print("-------------------------")

    #pda_final_state = pda_empty_stack.to_final_state()
    #print_pda(pda_final_state)


    return
    stream = CommonTokenStream(lexer)
    parser = MimeParser(stream)
    tree = parser.mimeMessage()


if __name__ == '__main__':
    main(sys.argv)

