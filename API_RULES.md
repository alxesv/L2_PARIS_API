# API rules

## REST API must accept and respond with JSON

It is a common practice that APIs should accept JSON requests as the payload
and also send responses back.

JSON is an open and standardized format for data transfer.

It is derived from JavaScript in a way to encode and decode JSON via the
Fetch API or another HTTP client.

Moreover, server-side technologies have libraries that can decode JSON without
any hassle.

## Go with Error Status Codes

Over 100 status codes have already been built by HTTP.

It is a boon for developers to use status codes in their REST API design.

With the status codes, developers can instantly identify the issue, which
reduces the time of writing parsers to address all the different types of
errors.

There’s a status code for everything – from finding out the cause of a denied
session to locating the missing resource.

Developers can quickly implement routines for managing numerous errors based
on status codes.

## Don’t Use Verbs in URLs

If you understood the APIs' basics, you would know that inserting verbs in
the URL isn’t a good idea.

The reason behind this is that HTTP has to be self-sufficient to describe
the purpose of the action.

Let’s take an example when you want endpoint to produce a banner image for
a post; you have to note the :param is a placeholder for a URI parameter.

Your first extinct might be to create this endpoint:

`GET: /articles/:slug/generateBanner/`

The GET method is only able to say here that you just want to retrieve a
banner.

So, using this syntax might be beneficial:

`GET: /articles/:slug/banner/`

Similarly, for the endpoint, it might generate the new article, as shown
in this example.

**Do not use**

`POST: /articles/createNewArticle/`

**Do use**

`POST: /articles/`

## GET method and query parameters should not alter the state

Use PUT, POST and DELETE methods instead of the GET method to alter the state.

**Do not use** GET for state changes:

`GET /users/711?activate`

or

`GET /users/711/activate`

## Use Plural Nouns to Name a Collection

When you have to develop the collection in REST API, just go with plural
nouns.

It makes it easier for humans to understand the meaning of collection without
actually opening it.

Let’s go through this example:

`GET /cars/123`

`POST /cars`

`GET /cars`

It is clear from the example that ‘car’ is referred to as number 123 from the
entire list of "cars".

The usage of a plural noun is merely indicating that this is a collection
of different cars. Now, look at one another example:

`GET /car/123`

`POST /car`

`GET /car`

This example does not clearly show whether there is more than one car in the
system or not.

For a human reader, it might be challenging to understand, as well.

## Use sub-resources for relations

If a resource is related to another resource use sub-resources.

`GET /cars/711/drivers/` Returns a list of drivers for car 711

`GET /cars/711/drivers/4` Returns driver #4 for car 711

## Use HATEOAS

Hypermedia as the Engine of Application State is a principle that hypertext
links should be used to create a better navigation through the API.

```
{
    "id": 711,
    "manufacturer": "bmw",
    "model": "X5",
    "seats": 5,
    "drivers": [
        {
            "id": "23",
            "name": "Stefan Jauker",
            "links": [
                {
                    "rel": "self",
                    "href": "/api/v1/drivers/23"
                }
            ]
        }
    ]
}
```

## Provide filtering, sorting, field selection and paging for collections

### Filtering

Use a unique query parameter for all fields or a query language for filtering.

`GET /cars?color=red` Returns a list of red cars

`GET /cars?seats<=2` Returns a list of cars with a maximum of 2 seats

### Sorting

Allow ascending and descending sorting over multiple fields.

`GET /cars?sort=-manufacturer,+model`

This returns a list of cars sorted by descending manufacturers and ascending
models.

### Field selection

Mobile clients display just a few attributes in a list. They don’t need all
attributes of a resource.

Give the API consumer the ability to choose returned fields.

This will also reduce the network traffic and speed up the usage of the API.

`GET /cars?fields=manufacturer,model,id,color`

### Paging

Use limit and offset.

It is flexible for the user and common in leading databases.

The default should be limit=20 and offset=0

`GET /cars?skip=10&limit=5`

To send the total entries back to the user use the custom
**_HTTP header: X-Total-Count_**.

Links to the next or previous page should be provided in the HTTP header
link as well.

It is important to follow this link header values instead of constructing
your own URLs.

## Version your API

Make the API Version mandatory and do not release an un-versioned API.

Use a simple ordinal number and avoid dot notation such as 2.5.

We are using the url for the API versioning starting with the letter "v“

`/blog/api/v1`

`/blog/api/v2.1`

## Well compiled documentation

Documentation is one of the important but highly ignored aspects of a REST
API structure.

The documentation is the first point in the hands of customers to understand
the product and critical deciding factor whether to use it or not.

One good documentation is neatly presented in a proper flow to make an API
development process quicker.

It is a simple principle – the faster developers understand your API, the
faster they start using it.

Your API documentation must be compiled with precision.

It must include all the relevant information such as the endpoint and
compatible methods, different parameter options, numerous types of data,
and so on.

The documentation should be so robust that it can easily walk a new user
through your API design.

## Handle Errors with HTTP status codes

It is hard to work with an API that ignores error handling.

Pure returning of an HTTP 500 with a stacktrace is not very helpful.

Use HTTP status codes

The HTTP standard provides over 70 status codes to describe the return values. We don’t need them all, but there should
be used at least a mount of 10.

`200 — OK` — Everything is working

`201 — OK` — New resource has been created

`204 — OK` — The resource was successfully deleted

`304 — Not Modified` — The client can use cached data

`400 — Bad Request` — The request was invalid or cannot be served. The exact error should be explained in the error
payload. E.g. „The JSON is not valid“

`401 — Unauthorized` — The request requires an user authentication

`403 — Forbidden` — The server understood the request, but is refusing it or the access is not allowed.

`404 — Not found` — There is no resource behind the URI.

`422 — Unprocessable Entity` — Should be used if the server cannot process the enitity, e.g. if an image cannot be
formatted or mandatory fields are missing in the payload.

`500 — Internal Server Error` — API developers should avoid this error.

If an error occurs in the global catch blog, the stracktrace should be logged and not returned as response.

## Use error payloads

All exceptions should be mapped in an error payload.

Here is an example how a JSON payload should look like:

```
{
  "errors": [
   {
    "userMessage": "Sorry, the requested resource does not exist",
    "internalMessage": "No car found in the database",
    "code": 34,
    "more info": "http://dev.mwaysolutions.com/blog/api/v1/errors/12345"
   }
  ]
}
```

## Use Resource Nesting

Resource objectives always contain some sort of functional hierarchy or are
interlinked to one another.

However, it is still ideal to limit the nesting to one level in the REST API.

Too many nested levels can lose their elegant appeal.

If you take a case of the online store into consideration, we can see “users”
and “orders” are part of stores.

Orders belong to some user; therefore the endpoint structure looks like:

`/users // list all users`

`/users/123 // specific user`

`/users/123/orders // list of orders that belong to a specific user`

`/users/123/orders/0001 // specific order of a specific users order list`

## Allow overriding HTTP method

Some proxies support only POST and GET methods.

To support a REST API with these limitations, the API needs a way to
override the HTTP method.

Use the custom HTTP Header **_X-HTTP-Method-Override_** to overrider the POST
Method.

## Use SSL/TLS

When you have to encrypt the communication with your API, always use SSL/TLS.

Use this feature without asking any questions.

## Secure your API

It is a favorite pastime for hackers to use automated scripts to attack your
API server.

Thus, your API needs to follow proactive security measures to run operations
while safeguarding your sensitive data smoothly.

Foremost, your API must have an HTTP Strict Transport Security (HSTS) policy.

Up next, you should secure your network from middle man attacks, protocol
downgrade attacks, session hijacking, etc.

Just use all the relevant security standards to the security of your API.

Perfectly designed REST API stays on the positive side of technical
constraints along with taking user experience-based solutions.

API is a part of the business strategy; it is a marketing tool for the
organization, thus it is essential to execute APIs in the right manner.

That’s because unstructured API is a liability rather than an asset.