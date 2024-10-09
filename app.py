import glob
import os

from flask import Flask, send_from_directory, request

app = Flask(__name__)

@app.route("/")
def main():
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    # Print the directories
    for directory in directories_list:
        print(directory)
    return send_from_directory(directories_list[0], 'index.html')

# login requests
@app.route("/login")
def login():
    return send_from_directory('login', 'index.html')

@app.route('/login/<path:filename>')
def serve_login_files(filename):
    return send_from_directory('login', filename)

@app.route('/login/images/<path:filename>')
def serve_login_images(filename):
    return send_from_directory('login/images', filename)

@app.route("/<path:filename>")
def main_serve(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    # Print the directories
    for directory in directories_list:
        print(directory)
    return send_from_directory(directories_list[0], filename)


# Route to serve CSS, JS, and other static files from 'vendor' directory
@app.route('/vendor/<path:filename>')
def serve_vendor(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)


# Route to serve CSS files
@app.route('/css/<path:filename>')
def serve_css(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)


# Route to serve JS files
@app.route('/js/<path:filename>')
def serve_js(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)
@app.route('/plotly/<path:filename>')
def serve_plotly(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)

if __name__ == '__main__':
    app.run(debug=True)

