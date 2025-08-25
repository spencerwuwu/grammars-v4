#!/usr/bin/env python3
import sys
from typing import Dict, List
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



def get_grammar_mutation(cfg_file, seed_file, 
                         Lexer, Parser,
                         skip_rulenames=[])-> Dict[str, List[str]]:

    # Load cfg
    cfg = get_cfg(cfg_file, verbose=False)

    # Load input, parse into tokens
    with open(seed_file, "r") as f:
        data = f.read()
    input_stream = InputStream(data)
    #input_stream = FileStream(argv[1])
    lexer = Lexer(input_stream)

    input_tokens = []
    for token in lexer.getAllTokens():
        token_name = lexer.symbolicNames[token.type] or f"'{lexer.literalNames[token.type]}'"
        #print(f"Token: {token_name}, Text: '{token.text}', Line: {token.line}, Column: {token.column}")
        input_tokens.append((token_name, token.text))

    # Get parse tree in ANTLR
    input_stream = InputStream(data)
    lexer = Lexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = Parser(stream)
    tree = parser.mimeMessage()

    tokens_input = [t[0].lower() for t in input_tokens]
    labels_input = [t[1] for t in input_tokens]

    def _check_skip(rulename):
        for skip in skip_rulenames:
            if skip.lower() in rulename.lower():
                return True
        return False

    def _in_regions(start, end, regions):
        for r_start, r_end in regions:
            if start >= r_start and end <= r_end:
                return True
        return False

    # Get index ranges for each rule in the parse tree
    def get_rule_indices(node, rule_indices):
        if isinstance(node, ParserRuleContext):
            rule_name = parser.ruleNames[node.getRuleIndex()].lower()
            start_index = node.start.tokenIndex
            end_index = node.stop.tokenIndex
            if rule_name not in rule_indices:
                rule_indices[rule_name] = []
            rule_indices[rule_name].append((start_index, end_index))
            for child in node.getChildren():
                get_rule_indices(child, rule_indices)
    rule_indices = dict()
    get_rule_indices(tree, rule_indices)

    #for rule_name, indices in rule_indices.items():
    #    print(rule_name)
    #    for start_index, end_index in indices:
    #        print("\t", (start_index, end_index), repr("".join(labels_input[start_index:end_index+1])))

    # Get rule sets based on CYK
    cyk_table = cfg.get_cyk_table(tokens_input)
    input_parts = dict()

    skip_regions = []
    for key, v in rule_indices.items():
        if _check_skip(key):
            for start, end in v:
                skip_regions.append((start, end))

    for k, v in cyk_table.items():
        if not v:
            continue
        for cyknode in v:
            rulename = cyknode.value.value # CYKNode -> Variable -> str
            start, end = k
            # NOTE: hacky and not-sure way to skip sampling at certain areas
            # Check if it's fully within "skip_rulenames" ranges
            if _in_regions(start, end, skip_regions):
                continue

            value = repr("".join(labels_input[start:end+1]))

            if rulename == "S" or _check_skip(rulename):
                continue

            rulename = rulename.lower()
            if rulename not in input_parts:
                input_parts[rulename] = set()
            input_parts[rulename].add(value)
            #print(rulename)
        #if has_fit:
        #    print("\t", repr("".join(labels_input[k[0]:k[1]+1])))
    #for rulename, values in input_parts.items():
    #    print(rulename)
    #    for v in values:
    #        print("\t", v)
    #print(cfg.contains(s))
    #print(cfg.get_cnf_parse_tree(s))

    mutation_sets = {}
    cnts = 0
    for rulename, values in input_parts.items():
        if "body" in rulename.lower():
            continue
        mutation_sets[rulename] = [] 
        for start, end in rule_indices.get(rulename, set()):
            pre = "".join(labels_input[:start])
            mid = "".join(labels_input[start:end+1])
            post = "".join(labels_input[end+1:])
            for new_val in values:
                # Delection
                mutation_sets[rulename].append(pre + post)
                # Addition (behind)
                mutation_sets[rulename].append(pre + mid + new_val + post)
                cnts += 2

    print(f"Total mutations: {cnts}")
    
    for rulename, muts in mutation_sets.items():
        print("++", rulename)
        for m in muts:
            print(repr(m))
            print("------")
        print("+++++++++++++++++++++++++")

    return mutation_sets


if __name__ == '__main__':
    seed_file = sys.argv[1]
    skip_rulenames = [
            "#CNF", "ANTLR_new",
            "_opt", "_star", "_plus",
            "BodyContent", "BodyLine"
            ]
    get_grammar_mutation("cfg.txt", seed_file, MimeLexer, MimeParser, skip_rulenames)


