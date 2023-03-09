# Send to Kindle web app

This is a personal send-to-kindle web app made with Flask and deployed to
Vercel.

It receives a article's URL, converts the HTML to Epub and sends it to
your Kindle.

## Setup

To run this app locally, type the following commands in your terminal:

Clone the repository:

```
git clone https://github.com/lugrao/send_to_kindle_web_app.git
```

Go to the repo's directory:

```
cd send_to_kindle_web_app
```

Create a Python virtual environment:

```
python3 -m venv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

Install dependencies:

```
python3 -m pip install -r requirements.txt
```

Create a `.env` file with your credentials:

```
echo 'SENDER_ADDRESS = "<your_gmail_address>"
SENDER_PASSWORD = "<your_gmail_app_password>"
RECEIVER_ADDRESS = "<your_send_to_kindle_email_address>"
APP_PASSWORD = "<any_password_for_you_to_use_this_web_app>"' >> .env
```

Run the app:

```
flask --app app run
```

You're good to go. Open the app in your browser, paste some article's URL,
type your password and send the article to your Kindle.

## Deploy to Vercel

You can easily deploy this app to Vercel.

Log in to the Vercel CLI. In the project's root directory, type:

```
vercel
```

Follow the steps.

Once it's all done, you can use the app from the URL Vercel gave you.
