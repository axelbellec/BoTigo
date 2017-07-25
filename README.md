<div>
  <div align="center">
    <img src="misc/BoTigo.png" alt="logo"/>
  </div>
<div>

<div align="center">
    <a href="https://www.codacy.com/app/axel-bellec/BoTigo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=axelbellec/BoTigo&amp;utm_campaign=Badge_Grade">
    	<img src="https://api.codacy.com/project/badge/Grade/e4d6711d1d5f43f8ac36a25f1944c1ee"/>
    </a>
	<a href="https://opensource.org/licenses/MIT">
		<img src="http://img.shields.io/:license-mit-ff69b4.svg?style=flat-square" alt="mit"/>
	</a>
</div>


# BoTigo

Facebook Messenger Bot.

## Installation

```
$ pip install requirements.txt
```

## Development

```sh
$ docker-compose up -d
$ docker exec -it botigo_server_1 bash
```

Then you can launch the app :
```sh
$ python manage.py runserver
```

Using `ngrok`:

```
$ ngrok http -host-header=rewrite 127.0.0.1:5000
```

## Heroku deployment

See [Heroku setup instructions](https://github.com/axelbellec/BoTigo/blob/master/heroku_setup.md).
