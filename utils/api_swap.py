def swap_faces(path1, path2):
    url = "https://your-api.com/face-swap"
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        files = {
            'image1': f1,
            'image2': f2
        }
        response = requests.post(url, files=files)

    if response.status_code == 200:
        result_path = f"{os.path.splitext(path1)[0]}_swapped.jpg"
        with open(result_path, 'wb') as out_file:
            out_file.write(response.content)
        return result_path
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
