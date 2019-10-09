#! -*- coding: utf-8 -*-
"""
采用最大正向匹配算法做机械分词
"""
import re

from trie_tree import TrieTree

PUNCTUATION = re.compile('[，。？！,.?!]|\s')
EN = re.compile('[a-zA-Z]+')


class Segment(object):
    def __init__(self, words_path=None):
        self.tree = TrieTree()

        if words_path:
            self.load_word_tree(words_path)
        else:
            self.build_word_tree()

    def load_word_tree(self, path):
        self.tree.load(path)

    def build_word_tree(self):
        pass

    def segment(self, sentence, seg_len=4):
        sentence = re.sub(PUNCTUATION, '', sentence)
        en = re.findall(EN, sentence)
        if en:
            sentence = re.sub(EN, '*', sentence)
        part = sentence[:seg_len]

        while True:
            seg_words, position = self.part_segment(part, en)
            if seg_words == '*':
                seg_words = en[0]
                en.pop(0)
            yield seg_words

            sentence = sentence[position:]
            part = sentence[:seg_len]

            if not sentence:
                break

    def part_segment(self, part_sentence, en):
        position = len(part_sentence)
        while True:
            if self.tree.is_has_word(part_sentence) or part_sentence == '*' or len(part_sentence) == 1:
                break

            position -= 1
            part_sentence = part_sentence[:position]

        return part_sentence, position


if __name__ == '__main__':
    seg = Segment(words_path='/data/gump/project-data/machinery_segment/word_tree.json')
    seg_result = seg.segment(sentence='身陷囹圄')
    print(list(seg_result))




