from aiohttp import web
from requests_oauthlib import OAuth2Session
import json
import logging
import sys, os
import asyncio, functools
import uuid, hmac, hashlib, binascii
from urllib import parse

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

auth_config = dict(
    auth_url   = "https://discordapp.com/api/oauth2/authorize",
    token_url  = "https://discordapp.com/api/oauth2/token",
    base_url   = "https://discordapp.com/api",
    client_id  = "200765429059158016",
    secret     = "nsRQVHHAvpecsibSStc2PPwGcwkI_UIx", #TODO: Move secret to config
    user_agent = "DiscordBot (https://github.com/jano017/AdaptBot, 0.1)",
    scope      = "identify connections guilds"
)

app = web.Application()

class Session(object):
    _store = {}
    def _destruct(self, id):
        print("Session "+str(id)+" timed out")
        del self._store[id]

    def __init__(self, id=None, timeout=3600):
        if id == None:
            self.__dict__ = {}
            self.id = uuid.uuid4()
            self.state = binascii.b2a_hex(os.urandom(16))
            self._destroy = asyncio.get_event_loop().call_later(
                timeout,
                self._destruct, self.id)
            self._store[self.id] = self
        elif uuid.UUID(id) not in self._store:
            raise ValueError(str(id) + " not in store")
        else:
            self.__dict__ = self._store[uuid.UUID(id)].__dict__
            self.refresh(timeout)
        print(self._store)

    def refresh(self, timeout):
        self._destroy.cancel()
        self._destroy = asyncio.get_event_loop().call_later(
            timeout,
            self._destruct, self.id
        )

    @staticmethod
    def authenticated(handler):
        @functools.wraps(handler)
        async def wrapper(request):
            if "authorization" not in request.headers:
                return web.Response(
                    status = 401,
                    body = json.dumps({"reason": "no session"}).encode("utf-8")
                )
            try:
                session = Session(request.headers["authorization"].lstrip("Basic "))
            except ValueError:
                return web.Response(
                    status = 401,
                    body = json.dumps({"reason": "invalid session"}).encode("utf-8")
                )
            return await handler(request, session)
        return wrapper

    @staticmethod
    def api_call(handler):
        @Session.authenticated
        @functools.wraps(handler)
        async def wrapper(request, session):
            data = await request.json()
            if "signature" not in data:
                return web.Response(
                    status = 401,
                    body = json.dumps({"reason": "Signature missing"})
                )
            if hmac.compare_digest(
                hmac.new(session.state, json.dumps(data.get("body", {})).encode('utf-8'), hashlib.sha256).hexdigest(),
                data["signature"]):
                    return web.Response(
                        body = json.dumps(await handler(data.get("body", {}), session)).encode('utf-8')
                        )
        return wrapper



async def index(request):
    with open('www/index.html', 'rb') as fh:
        return web.Response(
            body = fh.read()
        )


async def login(request):
    session = Session()
    session.auth = OAuth2Session(
        auth_config["client_id"],
        redirect_uri     = "http://localhost:5000/oauth", #TODO: Change to production url
        scope            =  auth_config["scope"],
        )
    session.auth.headers["User-Agent"] = auth_config["user_agent"]
    auth_url, state = session.auth.authorization_url(
        auth_config["auth_url"],
        state = session.id
    )
    return web.Response(
        status = 303,
        headers = {"Location": auth_url}
    )


@Session.api_call
async def user(request, session):
    print(request)
    return session.user

async def token(request):
    session = Session(request.GET["state"])
    token = session.auth.fetch_token(
        auth_config["token_url"],
        code = request.GET["code"],
        client_secret = auth_config["secret"]
    )
    print(token)
    session.user = session.auth.get(
        auth_config["base_url"] + "/users/@me"
    ).json()
    print(str(session.auth.get(auth_config["base_url"] + "/oauth2/applications/@me").json()))
    with open('www/pass_state.html') as fh:
        return web.Response(
            status = 200,
            body = fh.read().format(
                session = str(session.id),
                hmac_key = session.state.decode('utf-8')
            ).encode('utf-8')
    )

@Session.authenticated
async def logout(request, session):
    session._destruct()

if __name__ == '__main__':
    app.router.add_route("GET", "/"      ,  index)
    app.router.add_route("GET", "/login" ,  login)
    app.router.add_route("GET", "/oauth" ,  token)
    app.router.add_route("GET", "/logout", logout)
    app.router.add_route("POST", "/user", user)
    app.router.add_static("/static/", "lib/")
    web.run_app(app, port=5000)
