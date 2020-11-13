import aiohttp
import datetime
import asyncio
import json
import aiohttp_jinja2
import jinja2

routes = aiohttp.web.RouteTableDef()
app = aiohttp.web.Application()

@routes.get('/time_call')
async def get_time(request):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return t

@routes.get('/timeout-endpoint/<string:val>')
async def timeout_endpoint(request,val):
    await asyncio.sleep(0.5) # register sleep 500 ms
    return f"{val}"

@routes.post('/a/post-params-echo', methods=['POST'])
def post_params_echo(request):
    param1 = request.rel_url.query['q1']
    param2 = request.rel_url.query['q2']
    params = request.rel_url
    result = json.dumps(params)
    return aiohttp.web.json_response(result)


@routes.get('/echo/<string:val>/')
async def get_string_echo(request,val):
    app.logger.debug('get_string_echo {}'.format(val))
    return aiohttp.web.Response(text="0: " + val)

app.add_routes(routes)
aiohttp.web.run_app(app, host="localhost", port=8000)
