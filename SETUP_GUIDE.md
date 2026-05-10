# 🤖 Facebook Auto-Responder Setup Guide
### Stack: Groq AI (free) + Render (free hosting) + Facebook Messenger

---

## 📁 Files You Need

Make sure you have these 4 files in one folder:

| File | Purpose |
|------|---------|
| `app.py` | The bot server code |
| `requirements.txt` | Python libraries |
| `knowledge.txt` | Your business info (edit this!) |
| `Procfile` | Tells Render how to start the bot |

---

## STEP 1 — Edit Your Knowledge Base

Open `knowledge.txt` and **replace the sample content** with your actual business info.

Include things like:
- Business name & description
- Products/services and prices
- How to order & payment methods
- Shipping info
- Business hours & location
- FAQs

> 💡 The more detail you add, the smarter the bot's answers will be!

---

## STEP 2 — Get Your FREE Groq API Key

1. Go to **https://console.groq.com**
2. Sign up for a free account
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Copy and save the key (starts with `gsk_...`)

> ✅ Groq's free tier is very generous — plenty for a Facebook page bot.

---

## STEP 3 — Upload Code to GitHub

Render deploys from GitHub, so you need to upload your files there.

1. Go to **https://github.com** and sign up (free)
2. Click **"New repository"** (green button)
3. Name it: `fb-messenger-bot`
4. Set it to **Private**
5. Click **"Create repository"**
6. On the next page, click **"uploading an existing file"**
7. Drag and drop all 4 files:
   - `app.py`
   - `requirements.txt`
   - `knowledge.txt`
   - `Procfile`
8. Click **"Commit changes"**

---

## STEP 4 — Deploy to Render (Free Hosting)

1. Go to **https://render.com** and sign up (free, no credit card needed)
2. Click **"New +"** → select **"Web Service"**
3. Click **"Connect a repository"** and link your GitHub account
4. Select your `fb-messenger-bot` repository
5. Fill in the settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `fb-messenger-bot` |
   | **Region** | Singapore (closest to PH) |
   | **Branch** | `main` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
   | **Instance Type** | `Free` |

6. Scroll down to **"Environment Variables"** and add these:

   | Key | Value |
   |-----|-------|
   | `GROQ_API_KEY` | your key from Step 2 (gsk_...) |
   | `PAGE_ACCESS_TOKEN` | (get this in Step 6 below) |
   | `VERIFY_TOKEN` | make up any secret word e.g. `mybot2024secret` |

7. Click **"Create Web Service"**
8. Wait 2-3 minutes for it to deploy
9. Copy your URL — it looks like: `https://fb-messenger-bot.onrender.com`

---

## STEP 5 — Set Up Facebook Developer App

### 5a. Create a Facebook App

1. Go to **https://developers.facebook.com**
2. Log in with your Facebook account
3. Click **"My Apps"** → **"Create App"**
4. Select **"Other"** → **"Next"**
5. Select **"Business"** → **"Next"**
6. Enter App name: `My Page Bot` → Click **"Create App"**

### 5b. Add Messenger to Your App

1. On the App Dashboard, find **"Messenger"** and click **"Set up"**
2. Scroll to **"Access Tokens"**
3. Click **"Add or Remove Pages"** and connect your Facebook Page
4. Click **"Generate Token"** next to your Page
5. Copy this token — this is your **PAGE_ACCESS_TOKEN**

> ⚠️ Go back to Render → your service → "Environment" and paste this as the value for `PAGE_ACCESS_TOKEN`, then click Save. Render will restart the app automatically.

---

## STEP 6 — Connect the Webhook

1. In the Facebook App Dashboard, go to **Messenger → Settings**
2. Scroll to **"Webhooks"** and click **"Add Callback URL"**
3. Enter:

   | Field | Value |
   |-------|-------|
   | **Callback URL** | `https://your-app-name.onrender.com/webhook` |
   | **Verify Token** | the same word you set as `VERIFY_TOKEN` in Render |

4. Click **"Verify and Save"**

   > ✅ If it says "Complete" — your webhook is connected!
   > ❌ If it fails — double-check that your Render app is running (visit the URL in your browser, it should say "Facebook Messenger Bot is running!")

5. Under **"Webhook fields"**, click **"Add Subscriptions"** and check:
   - ✅ `messages`
   - ✅ `messaging_postbacks`

6. Click **"Save"**

---

## STEP 7 — Go Live & Test!

### Make the App Live
1. In the Facebook App dashboard, click **"App Mode"** (top right) — switch from **Development** to **Live**
2. You may be asked to fill in a Privacy Policy URL — you can use a free generator at https://www.privacypolicygenerator.info

### Test It
1. Go to your Facebook Page
2. Click **"Send Message"** (or message it from another account)
3. Type a question like: *"What are your products?"* or *"How do I order?"*
4. Your bot should reply within a few seconds! 🎉

---

## 🔄 How to Update Your Knowledge Base

Whenever you want to update the bot's answers:

1. Go to your GitHub repository
2. Click on `knowledge.txt`
3. Click the pencil ✏️ icon to edit
4. Make your changes and click **"Commit changes"**
5. Render will automatically redeploy in ~2 minutes

---

## ⚠️ Important Notes

- **Render free tier sleeps** after 15 minutes of no traffic. The first message after sleep may take 30-60 seconds to respond (the bot is "waking up"). Subsequent messages are fast.
- To prevent sleeping, you can use **UptimeRobot** (free) to ping your bot URL every 10 minutes.
- The bot only responds to **text messages** in Messenger (not comments on posts).
- Keep your `PAGE_ACCESS_TOKEN` and `GROQ_API_KEY` **secret** — never share them publicly.

---

## 🆘 Troubleshooting

| Problem | Fix |
|---------|-----|
| Webhook verification fails | Make sure Render app is live (visit the URL). Check VERIFY_TOKEN matches exactly. |
| Bot doesn't reply | Check PAGE_ACCESS_TOKEN is correct. Check Render logs for errors. |
| Bot gives wrong answers | Update knowledge.txt with more specific info. |
| Slow first response | Normal — Render free tier wakes up. Use UptimeRobot to fix. |

---

## 🎯 Quick Checklist

- [ ] Edited `knowledge.txt` with my business info
- [ ] Got Groq API key from console.groq.com
- [ ] Uploaded 4 files to GitHub
- [ ] Deployed on Render with 3 environment variables
- [ ] Created Facebook Developer App
- [ ] Got Page Access Token and added it to Render
- [ ] Set up and verified the webhook
- [ ] Switched App to Live mode
- [ ] Tested by sending a message to my Page

---

*Need help? Something not working? Just ask! 😊*
