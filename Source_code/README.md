## Getting Started

First, run the flask backend:

```bash
# Enter into the API directory to run backend
cd api
pip install -r requirements.txt
pip install flask python-dotenv
FLASK_APP=api.py
FLASK_ENV=development
flask run

```
Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) with your browser to see the result.

Then, run the nextjs/react frontennd:

```bash
# On the main directory

npm install
npm run dev


```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

