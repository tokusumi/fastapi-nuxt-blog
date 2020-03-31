import os
import shutil
from starlette.testclient import TestClient
from fastapi import FastAPI, UploadFile, File
from app.images import process


def test_hash_imagefilename():
    parent_path = '/image/dir/'
    image_filenames = ['image.jpg', 'image.png', 'image.jpeg']
    for image_filename in image_filenames:
        hashed_filename = process.hash_image_filename(image_filename, parent_path)
        assert hashed_filename.startswith(parent_path), 'Parent directory is modified'

        filename, ext = hashed_filename.rsplit('/', 1)[-1].rsplit('.', 1)
        true_name, true_ext = image_filename.rsplit('.', 1)
        assert ext == true_ext, 'Extension is modified'
        assert filename != true_name, 'Filename is not modified'


def activate_app(parent_path, output):
    app = FastAPI()

    @app.post("/")
    async def upload(file: UploadFile = File(...)):
        out_path = await process.mock_save_image(file, parent_path)
        assert out_path == output
    return app


class TestUploadImage:
    def setup_method(self, method):
        self.filename = "test.jpg"
        self.file_path = os.path.join(os.path.dirname(__file__), "test.jpg")
        self.parent_path = os.path.join(os.path.dirname(__file__), 'temp_out')
        self.output = os.path.join(self.parent_path, self.filename)
        self.app = activate_app(self.parent_path, self.output)

    def teardown_method(self, method):
        shutil.rmtree(self.parent_path)
        # pass

    def test_uploadimage(self):
        assert not os.path.exists(self.parent_path)
        os.makedirs(self.parent_path)
        assert os.path.exists(self.parent_path)
        assert os.path.exists(self.file_path)

        client = TestClient(self.app)
        with open(self.file_path, "rb") as f:
            res = client.post("/", files={"file": f})
        assert res.status_code == 200
        assert os.path.exists(self.output)
