"""Zefira application v1.0 """

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import os.path
import datetime
import uimodules

from tornado.options import define, options
from data_manag import DataManagement

define("port", default = 8000, help= "run on given port", type=int)

"""*************************************************************************
Application: Clase principal que inicializa los handlers e inicia la conexion 
con la base de datos. Ademas, asigna los modulosUI, los paths para los archivos
estaticos, templates, y otras settings de seguridad y cookies.

************************************************************************"""


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/publish", PublishHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/box", BoxHandler),
            (r"/signup", SignUpHandler),
            (r"/clientes", ClientesHandler),
            (r"/empresas", EmpresasHandler),
            (r"/cbox", CBoxHandler),
            (r"/companies", CompaniesHandler),
            (r"/error", ErrorHandler)
            ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            ui_modules={
                "Benefit" : uimodules.BenefitModule,
                "BenefitCo": uimodules.BenefitCoModule,
                "Company" : uimodules.CompaniesModule},            
            debug = True,
            cookie_secret = "0azgrztWSuenSRWevq9GAOp/4bDtSET0q8YII0ZfLDc=",
            login_url = "/login",
            xsrf_cookies = True,
            autoescape = None,
        )
        
        self.dataManager = DataManagement("zefira")
        
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def data_manager(self):
        return self.application.dataManager
    
    def get_current_user(self):
        user_id  = self.get_secure_cookie("username")
        password = self.get_secure_cookie("password")
        branch = self.get_secure_cookie("branch")
        
        user = self.application.dataManager.fetch_user(user_id, password, branch)
        if user:
            return user
        else:
            self.set_status(404)

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "user_creation_error.html",
            page_title = "Zefira | Error Page"
            )
class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render(
            "index.html",
            page_title = "Zefira v-1.0 | Home",
            header_text = "Bienvenidos a Zefira",
            
            )
class PublishHandler(BaseHandler):
    @tornado.web.authenticated
    
    def get(self):
        self.render(
                "publish.html",
                page_title = " Zefira Publish Test",
                header_text = "Publica",
                message = True,
            )
    def post(self):
        
        if self.data_manager.publish_benefit(self.request.arguments, self.current_user):
            self.redirect("/cbox")
        else:
            self.redirect("/error")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html",
                    page_title ="Zefira | Login",
                    header_text= "Ingresa a Zefira",  
                    )
    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.set_secure_cookie("password", self.get_argument("password"))
        self.set_secure_cookie("branch", self.get_argument("branch"))
        if self.get_argument("branch") == "companies":
            self.redirect("/cbox")
        else:
            self.redirect("/box")

class LogoutHandler(BaseHandler):
    def get(self):
        
        self.clear_cookie("username")
        self.clear_cookie("password")
        self.clear_cookie("branch")
        self.redirect("/")
        

class ClientesHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "clientes.html",
            page_title="Zefira | Clientes",
            header_text = "Zefira Clientes"
            )

class EmpresasHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "empresas.html",
            page_title="Zefira | Empresas",
            header_text=" Zefira Empresas"
            )



class BoxHandler(BaseHandler):
    @tornado.web.authenticated
    
    def get(self): 
        interests = self.current_user['interests']
        
        benefits = self.data_manager.fetch_benefits_usr(
            interests, self.current_user)
        
        self.render(
                "box.html",
               page_title = "Zefira | Inicio",
               header_text = "Box",
               user = self.current_user['username'],
               benefits = benefits
               )

    def post(self):
        
        benefit_id  = self.get_argument("benefit_id")
        self.current_user['session']['benefits'].append(
                        self.data_manager.reserve_fnc_users(benefit_id,self.current_user))
        self.redirect("/box")
              
class CBoxHandler(BaseHandler):
    @tornado.web.authenticated

    def get(self):
        benefits_published = self.current_user['benefits']
        if len(benefits_published) == 0 or benefits_published == None : 
            benefits_deref = None
            
        else:
            benefits_deref = self.data_manager.fetch_benefits_cmp(
                                            benefits_published)
        
        self.render(
            "cbox.html",
            page_title= "Zefira | Companies Box",
            header_text = "Companies Box",
            user = self.current_user['username'],
            benefits = benefits_deref
            )
        
class SignUpHandler(BaseHandler):
    
    def post(self):
        """
        Necesitas arreglar esta vaina, porque mientras mas complicados se hagan 
        los beneficios peor va a ser. Para eso  vas a tener que utiliza el la propiedad 
        self.request.arguments que devuelve una lista de todos los argumentos pasados 
        en el formulario. pasale esto a una funcion y deja que la funcion haga el trabajo.
        """
        import base64, uuid
        branch = self.get_argument("branch")
        if branch  == "companies":
            
            new_user = {
                '_id':"comp"+base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
                'username': self.get_argument('username'),
                'password': self.get_argument('password'),
                'info' : {
                    'name': self.get_argument('name'),
                    'description': self.get_argument('description'),
                    'email' : self.get_argument('email')
                    },
                'benefits' : []
                }
                  
        else:
            new_user = {
                '_id':"user"+base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
                'username' : self.get_argument('username'),
                'password': self.get_argument('password'),
                'info':{'email': self.get_argument('email')},
                'interests': [],
                'reserves' : [],
                'session' : {'benefits': []}
                }
        
        self.set_secure_cookie("username", self.get_argument("username"))
        self.set_secure_cookie("password", self.get_argument("password"))
        self.set_secure_cookie("branch", self.get_argument("branch"))
        self.redirect(self.data_manager.create_user(new_user,branch))
            
            

class CompaniesHandler(BaseHandler):
    @tornado.web.authenticated
    
    def get(self):
        user_companies = self.current_user['interests']
        companies = self.data_manager.fetch_companies(user_companies)
        self.render(
            "copres.html",
            page_title = "Zefira | Lista Empresas",
            header_text = "Empresas en Zefira",
            user = self.current_user['username'],
            companies = companies,
            )

    def post(self):
        company_id = self.get_argument("company_id")
        self.data_manager.follow_fnc_company(company_id, self.current_user)
        self.redirect("/companies")
        

                 
def main():
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()




