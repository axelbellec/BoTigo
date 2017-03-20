# Heroku commands to deploy an app

Create a Procfile that specifies that the app uses a web dyno with `gunicorn` as http server:

```
web: gunicorn botigo:app --log-file -
```

Specify a python runtime into `runtime.txt`:

```
python-x.x.x
```

Authenticate to your Heroku account:

```
$ heroku login
```

Use Conda buildpack from [__`arose13`__](https://github.com/arose13):

```
$ heroku config:set BUILDPACK_URL=https://github.com/arose13/conda-buildpack.git
```

Set environment variables:

```
$ heroku config:set FB_ACCESS_TOKEN=<your_fb_access_token>
$ heroku config:set FB_VERIFY_TOKEN=<your_fb_verify_token>
$ heroku config:set FB_GRAPH_API_VERSION=<your_fb_graph_api_version>
```

Deploying to Heroku:

- Git push to Heroku remote
```
$ git push heroku master
```

- Open the app in a browser
```
$ heroku open
```

App logs:
```
$ heroku logs
```
