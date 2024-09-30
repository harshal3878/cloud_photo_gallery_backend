from cloud_photo_gallery_backend import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)