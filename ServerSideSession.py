from flask.sessions import SessionInterface, SessionMixin
from uuid import uuid4
uuid = uuid4

# !!! WARNING !!!
# This session management implementation intentionally contains vulnerabilities.
# DON'T USE IT!

class VolatileServerSideSessionInterface(SessionInterface):
    cookie_name = "vsessid"
    sessions = dict()

    def open_session(self, app, request):
        sid = request.cookies.get(self.cookie_name)
        if not sid:
            sid = str(uuid())

        if sid not in self.sessions:
            self.sessions[sid] = VolatileServerSideSession(sid)

        return self.sessions[sid]

    def save_session(self, app, session, response):
        if not session.sid:
            response.delete_cookie(self.cookie_name)
        elif session.new:
            response.set_cookie(self.cookie_name, session.sid)
            session.new = False

class VolatileServerSideSession(dict, SessionMixin):
    def __init__(self, sid):
        self.sid = sid
        self.new = True
