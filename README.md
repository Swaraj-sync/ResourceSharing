## 🚀 Features

- 🔁 **Resource Sharing** – Offer unused items to the community
- 📥 **Request System** – Request needed resources with availability and priority
- 🧠 **Smart Matching** – Uses a **Maximum Flow** algorithm for optimal distribution
- 🕒 **Time-Based Scheduling** – Respect time windows for both sharing and requesting
- ⚡ **Priority Awareness** – Requests are weighted based on urgency
- 📊 **User Dashboard** – Monitor your shared and requested resources

---

## 🧠 How It Works

ResourceShare leverages **graph theory** to allocate resources optimally:

```
[Source] → [Resources] → [Requests] → [Sink]
```

- Nodes represent users and items
- Edges reflect availability, compatibility, and priority
- We run a **Maximum Flow** algorithm (via NetworkX) to find the best allocation
- Result: Efficient, fair distribution that maximizes community benefit

---

## 🛠 Tech Stack

| Layer       | Tech                     |
|-------------|--------------------------|
| Backend     | Flask, SQLAlchemy        |
| Algorithms  | NetworkX (Graph Theory)  |
| Auth        | Flask-Login              |
| Database    | PostgreSQL (prod), SQLite (dev) |
| Deployment  | Render                   |

---

## 📦 Installation

### 📋 Prerequisites
- Python 3.8+
- `pip`
- `git`

### ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/your-username/resource-share.git
cd resource-share

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a `.env` file:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///resource_share.db
```

### 🗄️ Initialize Database

```bash
flask shell
>>> from app import db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### 🚀 Run Locally

```bash
flask run
```

Go to `http://127.0.0.1:5000`

---

## 🌐 Deploy on Render

1. Fork this repo
2. Log in to [Render](https://render.com/)
3. Create a new Web Service:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add environment variable `SECRET_KEY`
5. Optionally add a PostgreSQL database on Render

---

## 📁 Project Structure

```
resource-share/
├── app.py              # Main Flask app
├── models.py           # Database models
├── algorithms.py       # Max Flow logic
├── config.py           # Config settings
├── templates/          # HTML templates
├── static/             # CSS and JS
├── requirements.txt    # Python packages
├── Procfile            # For deployment
└── README.md           # You're reading it!
```

---

## 🧪 Contributing

Contributions are welcome!

```bash
# Fork → Clone → Create Branch → Code → Commit → Push → PR
git checkout -b feature-name
git commit -m "Add: new feature"
git push origin feature-name
```

Please include tests and update docs where needed 🙏

---

## 💡 Future Enhancements

- 📆 Calendar View for scheduling
- 🔔 Notification System (Email/SMS)
- 🏷️ Resource Categories
- 🌍 Geo-based Matching
- ⭐ Reputation System
- 📱 React Native Mobile App


## 🙌 Acknowledgements

- Thanks to [NetworkX](https://networkx.org) for powering the optimization
- Inspired by community resilience and circular sharing systems

---

**Built with ❤️ to help communities thrive.**
