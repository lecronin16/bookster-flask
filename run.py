from app import app
from app.models import db, User, Review, Book

if __name__ == '__main__':
    app.run()

@app.shell_context_processor
def shell_context():
    return {"db":db, 'User':User, 'Review': Review, 'Book': Book,}