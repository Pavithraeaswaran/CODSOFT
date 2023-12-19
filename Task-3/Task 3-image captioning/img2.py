<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Captioning App</title>
</head>
<body>
    <h1>Image Captioning App</h1>
    
    <form method="post" enctype="multipart/form-data">
        <label for="photo">Choose a photo:</label>
        <input type="file" name="photo" accept=".jpg, .jpeg, .png" required>
        <button type="submit">Upload and Caption</button>
    </form>

    {% if image_path %}
        <img src="{{ image_path }}" alt="Uploaded Image">
        <p>{{ caption }}</p>
    {% endif %}
</body>
</html>