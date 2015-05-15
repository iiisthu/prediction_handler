import SimpleHTTPServer
import SocketServer
import os
from urlparse import urlparse
import normalization_test as nt

PORT = 8000
CURRENT_PATH = os.getcwd()
PADDLE_PATH = '/home/users/wangguosai/paddle_api_cmd_1_1_0-ts'
SCALER = 'ts_yq01-ps-global-42-train-scaler.data'
 

class PredictionHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def predict(self, data, result_path):
        scaler_file = SCALER
        output_file = 'data'
        nt.normalization(data, scaler_file, output_file)
        
        os.chdir(PADDLE_PATH + '/predict')
        #os.system('cat ' + CURRENT_PATH + '/' + output_file)
        os.system('cat ' + CURRENT_PATH + '/' + output_file \
             + "| ./predict myModel/ 0 | awk '{print $20}' > " + result_path)
        os.chdir(CURRENT_PATH)

 
    def do_GET(self):
        """Serve a GET request."""
        #print self.path
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        print query_components
        
        result_path = CURRENT_PATH + '/prediciton_result.txt'
        self.predict(query_components['data'], result_path)
        f = self.send_file(result_path)
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
    
    
    
    def send_file(self, path):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        #path = self.translate_path(self.path)
        #path = 'D:/test.txt'
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise
                
Handler = PredictionHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)



print "serving at port", PORT
httpd.serve_forever()
