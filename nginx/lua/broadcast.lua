local _M = {}
local http = require("resty.http")
local cjson = require "cjson"

function _M.broadcast_request()
    -- Prepare to forward the request
    local http_client = http.new()

    local upstream_servers_json = ngx.shared.upstream_servers:get("list")
    if not upstream_servers_json then
        ngx.log(ngx.ERR, "Failed to retrieve upstream servers list!")
        ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
        ngx.say(cjson.encode({ error = "Upstream servers not configured." }))
        return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
    end

    local upstream_servers = cjson.decode(upstream_servers_json)
    local results = {}

    ngx.req.read_body()
    -- Prepare the request parameters
    local method = ngx.req.get_method()
    local headers = ngx.req.get_headers()
    local args = ngx.req.get_uri_args()
    local body_data = ngx.req.get_body_data() -- Will be nil for GET requests
    
    for _, server in ipairs(upstream_servers) do
        local res, err = http_client:request_uri(server,{
            method = method,
            args = args,
            headers = headers,
            body = body_data,
        })

        if not res then
            ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
            ngx.say(cjson.encode({ error = "Failed to connect to " .. server .. ": " .. err }))
            return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
        end

        if res.status >= 400 then
            ngx.status = res.status
            ngx.header.content_type = "application/json"
            ngx.say(res.body)
            return ngx.exit(res.status)
        else
            results[#results + 1] = { status = res.status, body = res.body }
        end
    end

    ngx.status = results[1].status
    ngx.header.content_type = "application/json"
    ngx.say(results[1].body)
    return
end

return _M