
from flask import Flask, request, jsonify, render_template
import cleaner  # Make sure cleaner.py is in the same directory as this file
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page with the form
    return render_template('index.html')

@app.route('/default_categories')
def default_categories():
    try:
        default_categories = {
            'Documents': {'extensions': ['.doc', '.docx', '.pdf', '.txt'], 'target_dir': 'Documents'},
            'Images': {'extensions': ['.jpg', '.jpeg', '.png', '.gif'], 'target_dir': 'Images'},
            'Videos': {'extensions': ['.mp4', '.mkv', '.mov', '.avi'], 'target_dir': 'Videos'},
            # Add more default categories as needed
        }
        return jsonify(default_categories)
    except Exception as e:
        print(f"Error fetching default categories: {e}")
        return jsonify({"error": "Error fetching default categories"}), 500

@app.route('/sort', methods=['POST'])
def sort_files():
    data = request.get_json()  # Get data from JSON request
    downloads_path = data['downloadsPath']
    categories = data['categories']

    # Convert the categories from the form into the expected format for cleaner.py
    user_categories = {}
    for category in categories:
        categoryName = category['categoryName']
        extensions = category['extensions']
        targetDir = category['targetDir']
        # Assuming extensions are provided as a list of strings
        if categoryName in user_categories:
            # Update existing category
            user_categories[categoryName]['extensions'].extend(extensions)
            user_categories[categoryName]['target_dir'] = targetDir  # Override target directory if provided again
        else:
            # Add new category
            user_categories[categoryName] = {'extensions': extensions, 'target_dir': targetDir}

    # Call the sort_downloads function with the user's preferences
    processed_files = cleaner.sort_downloads(downloads_path, user_categories)

    # Return the list of processed files as JSON
    return jsonify(processed_files)

@app.route('/get_extensions', methods=['POST'])
def get_extensions():
    data = request.get_json()  # Assuming the directory path is sent in a JSON format
    directory_path = data['directoryPath']
    try:
        extensions = list_file_extensions(directory_path)
        return jsonify({"extensions": list(extensions)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def list_file_extensions(directory):
    extensions = set()
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            _, ext = os.path.splitext(filename)
            if ext:
                extensions.add(ext.lower())
    return extensions



if __name__ == '__main__':
    app.run(debug=True)
