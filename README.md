# Instagram Scrap Bot
The most advanced Instagram Downloader Bot.

```
This Base Repo is Belong To:
(C) @subinps
Copyright permission under MIT License
License -> https://github.com/subinps/Instagram-Bot/blob/main/LICENSE
```


You can Download almost anything From your Instagram Account.

**What Can Be Downloaded?:**
```
    1. All posts of any Profile. (Both Public and Private,for private profiles you need to be a follower.)
    2. All Posts from your feed.
    3. Stories of any profile (Both Public and Private,for private profiles you need to be a follower.)
    4. DP of any profile (No need to follow)
    5. Followers and Followees List of any Profile.
    6. List of followees who follows back the given username.
    7. List of followees who are not following back the given username.
    8. Stories of your Followees.
    9. Tagged posts of any profile.
    10. Your saved Posts.
    11. IGTV videos.
    12. Highlights from any profiles.
    13. Any Public Post from Link(Post/Reels/IGTV)
```

**Available Commands and Usage**
```
/start - Check wheather bot alive.
/help - To get all available commands.

```
## Deployment

### Generate Database
<details>
    <summary><b>Click Here For More Details</b></summary>

**1. Using ElephantSQL**
- Go to https://elephantsql.com and create account (skip this if you already have **ElephantSQL** account)
- Hit `Create New Instance`
- Follow the further instructions in the screen.
- Hit `Select Region`
- Hit `Review`
- Hit `Create instance`
- Select your database name
- Copy your database url, and fill to `DATABASE_URL` in config

**2. Using Heroku PostgreSQL**
<p><a href="https://dev.to/prisma/how-to-setup-a-free-postgresql-database-on-heroku-1dc1"> <img src="https://img.shields.io/badge/See%20Dev.to-black?style=for-the-badge&logo=dev.to" width="160""/></a></p>

</details>


## 1.For Heroku
    
#### Generate Creds
- Fork this repo first If your going to deploy it to heroku.
- clone this repo to generate the `credentials.json` to get Authentication for Google drive.
    
```sh
git clone https://github.com/Humanpredator/Insta-scrap
cd Insta-scrap
```
 
#### Getting Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Desktop and Create.
- Use the download button to download your credentials.
- Move that file to the root of insta-scrap , and rename it to **client_secrets.json**
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it if it is disabled
- Finally, run the script to generate `credentials.json` file for Google Drive:

```sh
python3 generate_creds.py
```

- After generating `credentials.json` upload this file to your repo before deploying to heroku or else drive upload won't Work.
    
#### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## 2.Deploy On VPS

```sh
git clone https://github.com/Humanpredator/Insta-scrap
cd Insta-scrap
pip3 install -r requirements.txt
```

### Setting up config.env file
- Create config.env file from config_sample.env

```sh
cp config_sample.env config.env
```
- Fill up rest of the fields. Meaning of each field is discussed below:
#### Required Field
- `BOT_TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather)
- `TELEGRAM_API`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org. **NOTE**: DO NOT put this in quotes.
- `TELEGRAM_HASH`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org
- `OWNER_ID`: The Telegram User ID (not username) of the Owner of the bot
- `GDRIVE_FOLDER_ID`: This is the folder ID of the Google Drive Folder to which you want to upload all the posts.
- `DOWNLOAD_STATUS_UPDATE_INTERVAL`: A short interval of time in seconds after which the progress/status message is updated. (I recommend to keep it to `5` seconds at least)  
#### Optional Field
- `DATABASE_URL`: Your Database URL. See [Generate Database](https://github.com/Humanpredator/insta-scrap/tree/master#generate-database) to generate database (**NOTE**: If you use database you can save your Sudo ID permanently using `/addsudo` command).
- `AUTHORIZED_CHATS`: Fill user_id and chat_id (not username) of groups/users you want to authorize. Separate them with space, Examples: `-0123456789 -1122334455 6915401739`.
- `SUDO_USERS`: Fill user_id (not username) of users whom you want to give sudo permission. Separate them with space, Examples: `0123456789 1122334455 6915401739` (**NOTE**: If you want to save Sudo ID permanently without database, you must fill your Sudo Id here).

- `INDEX_URL`: Refer to https://gitlab.com/ParveenBhadooOfficial/Google-Drive-Index The URL should not have any trailing '/'
- `IGNORE_PENDING_REQUESTS`: If you want the bot to ignore pending requests after it restarts, set this to `True`.

#### Generate creds.
- See [Generate creds](https://github.com/Humanpredator/insta-scrap/tree/master#generate-creds) to generate `credentials.json`

```sh
python3 -m bot
```


### Note & caution

```
Contributions are welcomed, But Kanging and editing a few lines wont make you a Developer.
Fork the repo, Do not Import code.    
    1.If you're loggin into your account for first time confirm your login location on IG
    2.Don't Download posts frequently, instagram may temporarily block your account under suspicious activity.Again you     have to reset your IG password to work agin.
    3.If any error occur restart the bot or check your IG account and login again.

```

#### Support
Connect Me On [Telegram](https://t.me/query_realm)

#### About
```
LEGAL DISCLAIMER
    Developer or his team won't be liable for any loss caused by MISUSE of this Script.
    This Bot is Indended to be used only for Educational Purposes.
```
```
Thanks To:
    Instagram-Bot: for base code. --> https://github.com/subinps/Instagram-Bot
    Slam-mirror-bot: For some modules. --> https://github.com/breakdowns/slam-mirrorbot
```
    
