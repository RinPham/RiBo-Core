## Using API

### Request
#### Data structure
Each request to api endpoint contains content below:
|Type|Description|
|---|------------|
| Endpoint | Repository of content (user, patient, auth, geodata…)  |
| Method   | Request method  |
| Header   | ***Type***: Int, please refer this table<br/>***Appid***: String, Required.<br>***Device***: String, Required, Device id, If from browser, please use md5 of useragent.<br>***Agent***: String, Optional<br>***Authorization***: String, Optional. format: token <token_string><br>See more at Login or Logout |
| Body     | Contains request data.   |

#### Request method
|Type|Description|
|---|------------|
|PUT|Updates existing information.|
|POST|Creates new information.|
|GET|Retrieves information.<br>List of repository.|
|DELETE|Removes existing information.|

#### Header type value
|Value|Explain|
|----|-------|
|1|Mobile|
|2|Android phone|
|3|IOS phone|
|4|Window phone|
|5|Android tablet|
|6|IOS tablet|
|7|Mobile web, tablet web|
|8|Desktop web|

### Response
#### Status code
Each request will return a status code, Based on status code, you will decide to show content or show error message.
For more information on proper usage of HTTP status codes see RFC 2616 and RFC 6585.
Below is table of status code may be return from server.

___Successful 2xx___<br>
This class of status code indicates that the client's request was successfully received, understood, and accepted.
```
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
```

___Redirection - 3xx___<br>
This class of status code indicates that further action needs to be taken by the user agent in order to fulfill the request.
```
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT
```

___Client Error - 4xx___<br>
The 4xx class of status code is intended for cases in which the client seems to have erred. Except when responding to a HEAD request, the server SHOULD include an entity containing an explanation of the error situation, and whether it is a temporary or permanent condition.
```
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_432_TOKEN_EXPIRED
```

___Server Error - 5xx___<br>
Response status codes beginning with the digit "5" indicate cases in which the server is aware that it has erred or is incapable of performing the request. Except when responding to a HEAD request, the server SHOULD include an entity containing an explanation of the error situation, and whether it is a temporary or permanent condition.
```
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
```