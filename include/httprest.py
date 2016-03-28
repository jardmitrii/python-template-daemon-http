import logging
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from urlparse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def options(self):      
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.send_header('Access-Control-Allow-Methods', 'GET')

    def send_headers(self, http_code):
        self.send_response(http_code)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def send_answer(self, msg, http_code=200):
        logging.debug('%s %s' % (http_code, msg))
        self.send_headers(http_code)
        self.wfile.write(json.dumps(msg))
        
    def do_GET(self):
        logging.debug('Method is GET')
        url_dict = urlparse(self.path)
        paths_list = url_dict.path.strip('/').split('/')
        querys_dict = parse_qs(url_dict.query, keep_blank_values=True)
        logging.debug('querys_dict is %s' % str(querys_dict))
        logging.debug('Token is %s' % querys_dict['token'][0])

    def do_GET(self):
        self.make_process()
        
    def do_POST(self):
        self.make_process()
        
    def do_PUT(self):
        self.make_process()

    def do_DELETE(self):
        self.make_process()

    def make_process(self):
        p = Process(target=self.handle_request)
        p.start()
        p.join()

    def handle_request(self):
        branch_dict = { '/user': self.user_branch,
                        '/call': self.call_branch,
                        '/chat': self.chat_branch,
                        '/conference': self.conf_branch
                        }
        logging.debug('Method is %s' % self.command)
        url_dict = urlparse(self.path)
        self.url_path = url_dict.path.rstrip('/')
        if not self.url_path:
            self.send_error(error_msg="Empty URL path")
            return
            
        if self.url_path not in branch_dict:
            self.send_error(error_msg="Wrong URL path")
            return
            
        querys_dict = parse_qs(url_dict.query, keep_blank_values=True)
        logging.debug('querys_dict is %s' % str(querys_dict))
        data = '{}'
        
        if self.command == "GET":
            data = querys_dict.get('data', ['{"1": null}'])[0]

        if self.command == "POST":
            data = self.rfile.read(int(self.headers['Content-Length']))

        logging.debug(u'Data is %s' % data)
        self.param_dict = json.loads(data)
        answer = branch_dict[self.url_path]()
        answer_func = answer[0]
        answer_msg = answer[1]
        answer_func(answer_msg)

    def user_branch(self):
        if self.command == "GET":
            return (self.send_answer, 'Test GET')
        elif self.command == "POST":
            pass
        elif self.command == "PUT":
            pass
        elif self.command == "DELETE":
            pass

        # Заменяем pass на нужный код получения/отправки команд
        # 
        # Если нужно обратиться к данным подгруженным из JSON используем -
        # self.param_dict
        #
        # Если нужно вернуть ошибку делаем (сообщение идет в лог, ответ от сервера согласно ТЗ идет стандартный)
        # return (self.send_error, сообщение)
        #
        # Если нужно вернуть ответ делаем
        # return (self.send_answer, сообщение)
        #
        # В обоих случаях первый параметр идет без  (), то есть передается ссылка на функцию
        # и сообщение может быть как текст, так и dict - {'answer': 'OK'}, так и любой другой объект,
        # который JSON может сдампить
            
    def call_branch(self):
        pass #см user_branch

    def chat_branch(self):
        pass #см user_branch

    def conf_branch(self):
        pass #см user_branch

def runserver(listen_address, listen_port):
    server = HTTPServer((listen_address, listen_port), Handler)
    server.serve_forever()

if __name__ == '__main__':
    print 'HTTP REST module!'
