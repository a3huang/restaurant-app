from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import re

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def displayhome(self):
        output = ""
        output += "<html><body>"
        output += "<a href='/new'>Add a New Restaurant</a>"
        output += "<h1>Restaurants:</h1>"
        output += "<ul>"
        for line in session.query(Restaurant):
            output += "<li>"
            output += line.name
            output += " <a href='/" + str(line.id) + "/edit'>Edit</a>"
            output += " <a href='/" + str(line.id) + "/delete'>Delete</a></li>"
        output += "</ul>"
        output += "</body></html>"
        return output

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = self.displayhome()
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id_num = self.path.split('/')[1]
                r = session.query(Restaurant).filter_by(id = id_num).one()
                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/"
                output += str(id_num) + "/edit'><h2>Edit Name for %s!</h2><input name='edit_rest'" % r.name
                output += "type='text' placeholder='%s'> <input type='submit' value='Submit'>" % r.name
                output += "<input name='no' type='submit' value='Cancel'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action=' \
                          /new'><h2>Add a New Restaurant!</h2><input name='restaurant' \
                          type='text'> <input type='submit' value='Submit'> <input name='no' \
                          type='submit' value='Cancel'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id_num = self.path.split('/')[1]
                print id_num
                r = session.query(Restaurant).filter(Restaurant.id == id_num).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % r.name
                output += "<form method='POST' enctype='multipart/form-data' action='/"
                output += str(id_num) + "/delete'> <input name='yes' type='submit' value='Yes'>"
                output += "<input name='no' type='submit' value='Cancel'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rest = fields.get('restaurant')

                if rest[0] != '':
                    newRestaurant = Restaurant(name = rest[0])
                    session.add(newRestaurant)

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('edit_rest')

                if name[0] != '':
                    id_num = self.path.split('/')[1]
                    r = session.query(Restaurant).filter(Restaurant.id == id_num).one()
                    r.name = name[0]
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    yes = fields.get('yes')

                if yes:
                    id_num = self.path.split('/')[1]
                    r = session.query(Restaurant).filter(Restaurant.id == id_num).one()
                    name = r.name
                    session.delete(r)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
