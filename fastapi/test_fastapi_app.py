import json
from io import BytesIO
from pytest import mark
from main import upload_file
from fastapi import UploadFile


@mark.asyncio
async def test_upload_file_with_valid_bag(tmp_path):  # Using tmp_path fixture
    bagfile_content = b"Mock content of the bag file"
    bagfile_path = tmp_path / "test.bag"
    with open(bagfile_path, "wb") as file:
        file.write(bagfile_content)

    start_time = 0.0
    end_time = 10.0
    output_folder = "/output_images/"
    topics_dropdown = "/rgb_image"

    # Create an UploadFile object with the file content
    bagfile = UploadFile(filename=str(bagfile_path), file=BytesIO(bagfile_content))

    # Call the upload_file function within the event loop, passing the UploadFile object
    response = await upload_file(bagfile=bagfile, start_time=start_time,
                                 end_time=end_time, output_folder=output_folder,
                                 topics_dropdown=topics_dropdown)

    assert response.status_code == 200
    data_content = response.body.decode("utf-8")
    data=json.loads(data_content)  # Get the JSON content as a dictionary
    assert data["status"] == "success"
    assert "pid" in data

@mark.asyncio
async def test_upload_file_with_invalid_bag(tmp_path):  # Using tmp_path fixture
    invalid_file_content = b"Invalid file content"
    invalid_file_path = tmp_path / "invalid_file.txt"
    with open(invalid_file_path, "wb") as file:
        file.write(invalid_file_content)

    start_time = 0.0
    end_time = 10.0
    output_folder = "/output_images/"
    topics_dropdown = "/rgb_image"

    # Create an UploadFile object with the  file content
    invalid_file = UploadFile(filename=str(invalid_file_path), file=BytesIO(invalid_file_content))

    # Call the upload_file function within the event loop, passing the UploadFile object
    response = await upload_file(bagfile=invalid_file, start_time=start_time,
                                 end_time=end_time, output_folder=output_folder,
                                 topics_dropdown=topics_dropdown)

    assert response.status_code == 200
    data_content = response.body.decode("utf-8")
    data=json.loads(data_content)  #Get the JSON content as a dictionary
    assert data["status"] == "fail"
    assert data["message"] == "Only bag format is accepted!"