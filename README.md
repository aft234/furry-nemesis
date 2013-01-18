furry-nemesis
=============

Export Citelighter Facts to a Google Doc

## Setup

 1. Clone the repository and `cd` into the repo.
 2. Create your virtual environment with `virtualenv venv --distribute`.
 3. Activate your virtual environment: `source venv/bin/activate`.
 4. Install all the requirements: `pip install -r requirements.txt`.
 5. Open a new terminal window and install redis if necessary.
 6. Run redis in this new window with `redis-server`.
 7. **If you're doing anything funky**: Edit `start.py` with the redis connection details.
 8. Start the server: `python start.py`.
 9. Open up your browser use the following endpoints:

    - `/connect` - Connect to Google Drive
    - `/export` - Create a new document in Google Drive
    - `/update` - Append content to newly created document in Google Drive
