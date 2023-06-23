![line](https://happycompany.hb.ru-msk.vkcs.cloud/line.png)
## Structuration
* cogs/
* .gitignore
* config.json
* main.py
* README.md
* requirements.txt

![line](https://happycompany.hb.ru-msk.vkcs.cloud/line.png)
### main.py
Main startup file. Contains bot initialization and `load`, `unload` and `reload` cogs functions. Don't recommended to edit!</sup> \
Bot config placed at `config.json`<sup>check Config</sup> \
Basic commands placed at `commands.py`<sup>help, info, etc.</sup> \
Moderation commands placed at `moderation.py`<sup>mute, ban, etc.</sup> \
Fun & other commands placed at `other.py`<sup>choose, avatar, etc.</sup> \
Command for updating project placed at `compile.py`<sup> just run it</sup>

![line](https://happycompany.hb.ru-msk.vkcs.cloud/line.png)
## Config
```json
{
  "token": "Bot token",
  "openai": "OpenAI token",
  "mongodb": "MongoDB uri",
  "permissions": "Required bot permissions",
  "application_id": "Application id",
  "owners": [
    owners,
    discord,
    id,
    list
  ]
}
```

![line](https://happycompany.hb.ru-msk.vkcs.cloud/line.png)
> ###### *by* HappyFan