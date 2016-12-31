#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

from google.appengine.ext import ndb

DEFAULT_NONFICTIONAL_NAME = 'default_nonfictional'
DEFAULT_FICTIONAL_NAME = 'default_fictional'
DEFAULT_MYSTERY_NAME = 'default_mystery'

#BASKET List
NONFICTIONAL=[]
FICTIONAL=[]
MYSTERY=[]

#Functions to get entity keys of the data models
def nonfictional_key(nonfictional_name=DEFAULT_NONFICTIONAL_NAME):
    """Constructs a Datastore key for a Nonfictional entity.

    We use nonfictional_name as the key.
    """
    return ndb.Key('Nonfictional', nonfictional_name)

def fictional_key(fictional_name=DEFAULT_FICTIONAL_NAME):
    """Constructs a Datastore key for a Fictional entity.

    We use fictional_name as the key.
    """
    return ndb.Key('Fictional', fictional_name)

def mystery_key(mystery_name=DEFAULT_MYSTERY_NAME):
    """Constructs a Datastore key for a Mystery entity.

    We use mystery_name as the key.
    """
    return ndb.Key('Mystery', mystery_name)

#Creating three genres data model  
class Nonfictional(ndb.Model):
  author = ndb.StringProperty()
  bookname = ndb.StringProperty()
  price=ndb.FloatProperty()
  cart=ndb.BooleanProperty()

class Fictional(ndb.Model):
  author = ndb.StringProperty()
  bookname = ndb.StringProperty()
  price=ndb.FloatProperty()
  cart=ndb.BooleanProperty()
    
class Mystery(ndb.Model):
  author = ndb.StringProperty()
  bookname = ndb.StringProperty()
  price=ndb.FloatProperty()
  cart=ndb.BooleanProperty()

#HTML code for the menu page
html="""
<html><body>
<h1 align="center"> Romil Chauhan's Book Repository</h1>
<form action="/enter" method="get">
    <ul><a href="/enter">Enter new book info</a> </ul>
</form>
<form action="/search" method="get">
    <ul><a href="/search">Search for the books written by particular author</a></ul>

</form>
<form action="/display" method="get">
    <ul><a href="/display?genre=nonfictional">Nonfictional Books</a></ul>
    <ul><a href="/display?genre=fictional">Fictional Books</a></ul>
    <ul><a href="/display?genre=mystery">Mystery Books</a></ul>
  
</form>
<form action="/shoppingcart" method="post">
    <ul><a href="/shoppingcart">My Shopping Cart</a> </ul>
</form>
</body>
</html>
"""

#HTML code for goto menu button
gotomenu="""
<html><body>

<form action="/" method="get">
            <div><button type="submit" action="/">Go To Menu</button>
</form>

</body>
</html>

"""

#HTML code for enter new book page
newbook="""
<html><body>
<h1 align="center"> Enter new book to book respository</h1>
<form action="/sign" method="post">
            <div><p>Author:</p><br><textarea name="author" rows="3" cols="60"></textarea></div>
            <div><p>Book Name:</p><br><textarea name="bookname" rows="3" cols="60"></textarea></div>
            <div><p>Genre:</p><br><textarea name="genre" rows="3" cols="60"></textarea></div>
            <div><p>Price:</p><br><input name="price" type="number"></input></div>
            <div><input type="submit" value="Enter Book Info"></div>
</form>

</body>
</html>
"""

#HTML code for search book page
searchbook="""
<html><body>
<h1 align="center"> Search for book by author's name in book repository</h1>
<form action="/searchbookinfo" method="get">
            <div><p>Author:</p><br><textarea name="searchauthor" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Enter Author Name"></div>
</form>

</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(html)
        

class NewBook(webapp2.RequestHandler):
    def get(self):
        self.response.write(newbook)
        self.response.write(gotomenu)

class NewBookInfo(webapp2.RequestHandler):
    def post(self):
        """Code for entering new book info"""
        genre=self.request.get('genre')
        
        #Data accessed via Datastore query   
        if (genre=="Nonfictional") or (genre=="nonfictional") or (genre=="NONFICTIONAL"):
            nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
            nonfictional = Nonfictional(parent=nonfictional_key(nonfictional_name))

            nonfictional.author=self.request.get('author')
            nonfictional.bookname=self.request.get('bookname')
            nonfictional.price=float(self.request.get('price'))
            nonfictional.cart=False
            nonfictional.put()
          

        if (genre=="Fictional") or (genre=="fictional") or (genre=="FICTIONAL"):
          fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
          fictional = Fictional(parent=fictional_key(fictional_name))

          fictional.author=self.request.get('author')
          fictional.bookname=self.request.get('bookname')
          fictional.price=float(self.request.get('price'))
          fictional.cart=False
          fictional.put()

        if (genre=="Mystery") or (genre=="mystery") or (genre=="MYSTERY"):
          mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
          mystery = Mystery(parent=mystery_key(mystery_name))

          mystery.author=self.request.get('author')
          mystery.bookname=self.request.get('bookname')
          mystery.price=float(self.request.get('price'))
          mystery.cart=False
          mystery.put()

        else:
            self.response.write("""<html><body><p>No such genre exist</p></body></html>""")

        self.redirect('/enter')
    

class SearchBook(webapp2.RequestHandler):
    def get(self):
        self.response.write(searchbook)
        self.response.write(gotomenu)

class SearchBookInfo(webapp2.RequestHandler):
    def get(self):
        """Code for searching book info by author name"""
        auth=self.request.get('searchauthor')

        nf=False
        f=False
        m=False
        
        #Checking in nonfictional section
        nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
        nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
        nonfictionals = nonfictional_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=addnonfictional" method="post">""")
        for nonfictional in nonfictionals:
            if nonfictional.author:
                
                if not((nonfictional.author.lower()).find(auth.lower())):
                    nf=True
                    self.response.out.write('<b>%s</b> wrote:' % nonfictional.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(nonfictional.bookname))
                    self.response.out.write('Price is: %f' % nonfictional.price)
                    if nonfictional.cart==False:
                        self.response.out.write('<input type="checkbox" name="nonfictional" value="%s"> Add to cart<br>' % cgi.escape(nonfictional.bookname))
                    elif nonfictional.cart==True:
                        self.response.out.write('<input type="checkbox" name="nonfictional" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(nonfictional.bookname))

        if nf==True:
            self.response.out.write('<input type="submit" value="Tick and add above nonfictional books to cart">')
        self.response.write("""</form></body></html>""")

        #Checking in fictional section
        fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
        fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
        fictionals = fictional_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=addfictional" method="post">""")
        for fictional in fictionals:
            if fictional.author:
                
                if not((fictional.author.lower()).find(auth.lower())):
                    f=True
                    self.response.out.write('<b>%s</b> wrote:' % fictional.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(fictional.bookname))
                    self.response.out.write('Price is: %f' % fictional.price)
                    if nonfictional.cart==False:
                        self.response.out.write('<input type="checkbox" name="fictional" value="%s"> Add to cart<br>' % cgi.escape(fictional.bookname))
                    elif nonfictional.cart==True:
                        self.response.out.write('<input type="checkbox" name="fictional" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(fictional.bookname))

        if f==True:
            self.response.out.write('<input type="submit" value="Tick and add above fictional books to cart">')
        self.response.write("""</form></body></html>""")

        #Checking in mystery section
        mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
        mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
        mysterys = mystery_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=addmystery" method="post">""")
        for mystery in mysterys:
            if mystery.author:
                
                if not((mystery.author.lower()).find(auth.lower())):
                    m=True
                    self.response.out.write('<b>%s</b> wrote:' % mystery.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(mystery.bookname))
                    self.response.out.write('Price is: %f' % mystery.price)
                    if nonfictional.cart==False:
                        self.response.out.write('<input type="checkbox" name="mystery" value="%s"> Add to cart<br>' % cgi.escape(mystery.bookname))
                    elif nonfictional.cart==True:
                        self.response.out.write('<input type="checkbox" name="mystery" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(mystery.bookname))

        if m==True:
            self.response.out.write('<input type="submit" value="Tick and add above mystery books to cart">')
        self.response.write("""</form></body></html>""")

        #Note:Here self.redirect is not used because it will erase the searched data and redirect us to search page
        self.response.write("""
        <html><body>
        <form action="/searchbookinfo" method="get">
                    <div><p>Author:</p><br><textarea name="searchauthor" rows="3" cols="60"></textarea></div>
                    <div><input type="submit" value="Enter Author Name"></div>
        </form>

        </body>
        </html>
        """)
        self.response.write(gotomenu)
        

class GenreBooks(webapp2.RequestHandler):
    def get(self):
        """Code for displaying the books of three genres"""

        #Getting the value corresponding to which url is clicked on the menu page
        gen=self.request.get('genre')

        #Nonfictional Section
        if gen=="nonfictional":
            #Data accessed via datastore query    
            nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
            nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
            nonfictionals = nonfictional_query.fetch()

            self.response.write("""<html><body><h1 align="center"> Nonfictional Books</h1><form action="/addandremovecart?checkvar=addnonfictional" method="post">""")
            for nonfictional in nonfictionals:
              if nonfictional.author:
                self.response.out.write('<b>%s</b> wrote:' % nonfictional.author)
              else:
                self.response.out.write(', An anonymous person wrote:')
              self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(nonfictional.bookname))
              self.response.out.write('Price is: %f' % nonfictional.price)
              if nonfictional.cart==False:
                  self.response.out.write('<input type="checkbox" name="nonfictional" value="%s"> Add to cart<br>' % cgi.escape(nonfictional.bookname))
              elif nonfictional.cart==True:
                  self.response.out.write('<input type="checkbox" name="nonfictional" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(nonfictional.bookname))
            self.response.out.write('<input type="submit" value="Submit">')
            self.response.write("""</form></body></html>""")
            
        #Fictional Section
        if gen=="fictional":
            #Data accessed via datastore query    
            fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
            fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
            fictionals = fictional_query.fetch()

            self.response.write("""<html><body><h1 align="center"> Fictional Books</h1><form action="/addandremovecart?checkvar=addfictional" method="post">""")
            for fictional in fictionals:
              if fictional.author:
                self.response.out.write('<b>%s</b> wrote:' % fictional.author)
              else:
                self.response.out.write(', An anonymous person wrote:')
              self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(fictional.bookname))
              self.response.out.write('Price is: %f' % fictional.price)
              if fictional.cart==False:
                  self.response.out.write('<input type="checkbox" name="fictional" value="%s"> Add to cart<br>' % cgi.escape(fictional.bookname))
              elif fictional.cart==True:
                  self.response.out.write('<input type="checkbox" name="fictional" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(fictional.bookname))
            self.response.out.write('<input type="submit" value="Submit">')
            self.response.write("""</form></body></html>""")
            
        #Mystery Section
        if gen=="mystery":
            #Data accessed via datastore query    
            mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
            mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
            mysterys = mystery_query.fetch()

            self.response.write("""<html><body><h1 align="center"> Mystery Books</h1><form action="/addandremovecart?checkvar=addmystery" method="post">""")
            for mystery in mysterys:
              if mystery.author:
                self.response.out.write('<b>%s</b> wrote:' % mystery.author)
              else:
                self.response.out.write(', An anonymous person wrote:')
              self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(mystery.bookname))
              self.response.out.write('Price is: %f' % mystery.price)
              if mystery.cart==False:
                  self.response.out.write('<input type="checkbox" name="mystery" value="%s"> Add to cart<br>' % cgi.escape(mystery.bookname))
              elif mystery.cart==True:
                  self.response.out.write('<input type="checkbox" name="mystery" value="%s" checked="checked"> Added to cart<br>' % cgi.escape(mystery.bookname))
            self.response.out.write('<input type="submit" value="Submit">')
            self.response.write("""</form></body></html>""")
            
        self.response.write(gotomenu)
        
class AddAndRemoveCart(webapp2.RequestHandler):
    def post(self):
        """Adding and removing book to/from the cart"""
        
        cv=self.request.get('checkvar')
        if cv!="bremoveall" and cv!="dremoveall":
            if cv=="addnonfictional":
                nonficts=self.request.get_all('nonfictional')
                nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
                nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
                nonfictionals = nonfictional_query.fetch()
                
                for nonfict in nonficts:
                    for nonfictional in nonfictionals:
                        if nonfictional.bookname==nonfict and nonfictional.cart==False:
                            nonfictional.cart=True
                            nonfictional.put()

            if cv=="addfictional":
                ficts=self.request.get_all('fictional')
                fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
                fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
                fictionals = fictional_query.fetch()
                
                for fict in ficts:
                    for fictional in fictionals:
                        if fictional.bookname==fict and fictional.cart==False:
                            fictional.cart=True
                            fictional.put()

            if cv=="addmystery":
                mysts=self.request.get_all('mystery')
                mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
                mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
                mysterys = mystery_query.fetch()
                
                for myst in mysts:
                    for mystery in mysterys:
                        if mystery.bookname==myst and mystery.cart==False:
                            mystery.cart=True
                            mystery.put()

            if cv=="removenonfictional":
                nonficts=self.request.get_all('rnonfictional')
                nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
                nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
                nonfictionals = nonfictional_query.fetch()
                
                for nonfict in nonficts:
                    for nonfictional in nonfictionals:
                        if nonfictional.bookname==nonfict and nonfictional.cart==True:
                            nonfictional.cart=False
                            nonfictional.put()

            if cv=="removefictional":
                ficts=self.request.get_all('rfictional')
                fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
                fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
                fictionals = fictional_query.fetch()
                
                for fict in ficts:
                    for fictional in fictionals:
                        if fictional.bookname==fict and fictional.cart==True:
                            fictional.cart=False
                            fictional.put()

            if cv=="removemystery":
                mysts=self.request.get_all('rmystery')
                mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
                mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
                mysterys = mystery_query.fetch()
                
                for myst in mysts:
                    for mystery in mysterys:
                        if mystery.bookname==myst and mystery.cart==True:
                            mystery.cart=False
                            mystery.put()

            self.redirect('/shoppingcart')
        else:
            if cv=="bremoveall" or cv=="dremoveall":
                #nonficts=self.request.get_all('rnonfictional')
                nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
                nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
                nonfictionals = nonfictional_query.fetch()
                
                
                for nonfictional in nonfictionals:
                    if nonfictional.cart==True:
                        nonfictional.cart=False
                        nonfictional.put()


                #ficts=self.request.get_all('rfictional')
                fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
                fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
                fictionals = fictional_query.fetch()
                
                
                for fictional in fictionals:
                    if fictional.cart==True:
                        fictional.cart=False
                        fictional.put()


                #mysts=self.request.get_all('rmystery')
                mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
                mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
                mysterys = mystery_query.fetch()
                
                
                for mystery in mysterys:
                    if mystery.cart==True:
                        mystery.cart=False
                        mystery.put()

                if cv=="bremoveall":
                    self.response.out.write('Thanks for buying!')
                elif cv=="dremoveall":
                    self.response.out.write('Emptied the cart!')

                self.response.write(gotomenu)
                    
            

            

        
        
                    
class ShoppingCart(webapp2.RequestHandler):
    def get(self):
        """Displaying my Shopping Cart"""
        tprice=float(0);
        nf=False
        f=False
        m=False
        #Checking in nonfictional section
        nonfictional_name = self.request.get('nonfictional_name', DEFAULT_NONFICTIONAL_NAME)
        nonfictional_query = Nonfictional.query(ancestor=nonfictional_key(nonfictional_name))
        nonfictionals = nonfictional_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=removenonfictional" method="post">""") 
        for nonfictional in nonfictionals:
            if nonfictional.author:
                if nonfictional.cart==True:
                    nf=True
                    self.response.out.write('<b>%s</b> wrote:' % nonfictional.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(nonfictional.bookname))
                    self.response.out.write('Price is: %f<br>' % nonfictional.price)
                    tprice+=float(nonfictional.price)
                    if nonfictional.cart==True:
                        self.response.out.write('<input type="checkbox" name="rnonfictional" value="%s"> Remove from cart<br>' % cgi.escape(nonfictional.bookname))

        if nf==True:
            self.response.out.write('<input type="submit" value="Remove above ticked nonfictional books">')
        self.response.write("""</form></body></html>""")

        #Checking in fictional section
        fictional_name = self.request.get('fictional_name', DEFAULT_FICTIONAL_NAME)
        fictional_query = Fictional.query(ancestor=fictional_key(fictional_name))
        fictionals = fictional_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=removefictional" method="post">""")
        for fictional in fictionals:
            if fictional.author:
                if fictional.cart==True:
                    f=True
                    self.response.out.write('<b>%s</b> wrote:' % fictional.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(fictional.bookname))
                    self.response.out.write('Price is: %f<br>' % fictional.price)
                    tprice+=float(fictional.price)
                    if fictional.cart==True:
                        self.response.out.write('<input type="checkbox" name="rfictional" value="%s"> Remove from cart<br>' % cgi.escape(fictional.bookname))

        if f==True:
            self.response.out.write('<input type="submit" value="Remove above ticked fictional books">')
        self.response.write("""</form></body></html>""")

        #Checking in mystery section
        mystery_name = self.request.get('mystery_name', DEFAULT_MYSTERY_NAME)
        mystery_query = Mystery.query(ancestor=mystery_key(mystery_name))
        mysterys = mystery_query.fetch()

        self.response.write("""<html><body><form action="/addandremovecart?checkvar=removemystery" method="post">""")
        for mystery in mysterys:
            if mystery.author:
                if mystery.cart==True:
                    m=True
                    self.response.out.write('<b>%s</b> wrote:' % mystery.author)
                    self.response.out.write('<blockquote>%s</blockquote>' %
                                      cgi.escape(mystery.bookname))
                    self.response.out.write('Price is: %f<br>' % mystery.price)
                    tprice+=float(mystery.price)
                    if mystery.cart==True:
                        self.response.out.write('<input type="checkbox" name="rmystery" value="%s"> Remove from cart<br>' % cgi.escape(mystery.bookname))

        if m==True:
            self.response.out.write('<input type="submit" value="Remove above ticked fictional books">')
        self.response.write("""</form></body></html>""")

        self.response.out.write('<br>')
        self.response.out.write('Total Price: %f<br>' % tprice)
        self.response.out.write('<br>')
        self.response.out.write('<br>')
        
        #Note:Here self.redirect is not used because it will erase the searched data and redirect us to search page
        self.response.write("""
        <html><body>
        <form action="/addandremovecart?checkvar=bremoveall" method="post">
                    <input type="submit" value="Buy the books">
        </form>
        <form action="/addandremovecart?checkvar=dremoveall" method="post">
                    <input type="submit" value="Empty Cart">
        </form>
        </body>
        </html>
        """)
        self.response.write(gotomenu)                
            
        
            
        


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/enter',NewBook),
    ('/sign',NewBookInfo),
    ('/search',SearchBook),
    ('/searchbookinfo',SearchBookInfo),
    ('/display',GenreBooks),
    ('/addandremovecart',AddAndRemoveCart),
    ('/shoppingcart',ShoppingCart)
], debug=True)
