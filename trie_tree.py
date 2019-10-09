#! -*- coding:utf-8 -*-
"""
采用萃树的方式构建词表
"""
import json


class TrieTree(object):
    def __init__(self, word_list=None):
        self.tree = {}
        if word_list:
            self.add_words(word_list)

    def add_words(self, words_list):
        for word in words_list:
            self.add_word(word)

    def add_word(self, word):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                tree[char] = {}
                tree = tree[char]

    def is_has_word(self, word):
        local_tree = self.tree
        for char in word:
            if char in local_tree:
                local_tree = local_tree[char]
            else:
                return False
        return True

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.tree, f, ensure_ascii=False)

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            word_tree = json.load(f)
        self.tree = word_tree


if __name__ == '__main__':
    data = open('/data/gump/project-data/machinery_segment/vocabulary.txt', 'r', encoding='utf-8').readlines()
    data = [item.strip() for item in data]
    trie = TrieTree(word_list=data)
    trie.save('/data/gump/project-data/machinery_segment/word_tree.json')
    print(trie.is_has_word('螃蟹'))
