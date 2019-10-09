#! -*- coding: utf-8 -*-
import json
import logging
import tornado.web
from tornado.httpserver import HTTPServer

from segment import Segment

PORT = 3333
logging.basicConfig(level='INFO')
segment = Segment(words_path='/data/gump/project-data/machinery_segment/word_tree.json')


class MachinerySegmentHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body.decode()
        sentence = json.loads(data)['sentence']
        ans_dict = dict(code=2100, message=None, data={})
        try:
            if sentence:
                logging.info('seg sentences: {}'.format(sentence))
                result = segment.segment(sentence)
                data = {
                    'sentence': sentence,
                    'seg': list(result)
                }
                ans_dict = dict(code=2000, message='success', data=data)
        except Exception as e:
            ans_dict = dict(code=4000, message=str(e), data={})
        ans_str = json.dumps(ans_dict, ensure_ascii=False)
        self.write(ans_str)


application = tornado.web.Application([
    (r"/machinery_segment/", MachinerySegmentHandler),
])

if __name__ == "__main__":
    myserver = HTTPServer(application)
    myserver.bind(3333)
    myserver.start(num_processes=1)
    logging.info('sentence paraphraser server is running....')
    tornado.ioloop.IOLoop.current().start()
