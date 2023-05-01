# Discord Bot to Add Sevices to Robonomics Subscription

## Run
* Create config.yaml
* Create devices/devices
```bash 
mkdir devices
touch devices/devices
```
* Run
```bash
docker build -t discord-bot .
docker run -d --name discord-bot -v devices:/devices discord-bot
```
