from cloud_photo_gallery_backend import create_app

#export PYTHONPATH=/home/harshal/learn   -use this to setup python module path 
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)