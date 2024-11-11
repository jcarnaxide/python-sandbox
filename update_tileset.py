from PIL import Image


PATH_TO_REPOS = "/mnt/c/Users/goldm/repos"
PATH_TO_RES = "/".join([PATH_TO_REPOS, "kenny_isometric_tileset/kenny_isometric_tileset/"])
PATH_TO_LANDSCAPE_TILESET = "/".join([PATH_TO_RES, "resources/landscape.tres"])


def get_image_size(filepath):
    return Image.open(filepath).size


def get_external_resources(tileset_path):
    with open(tileset_path, "r") as file:
        for line in file:
            if line.startswith("[ext_resource"):
                yield line


def get_sub_resources(tileset_path):
    search_str = "[sub_resource"
    with open(tileset_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if line.startswith(search_str):
                sub_index = index + 1
                sub_line = lines[sub_index]
                sub_resource = [line]
                while not sub_line.startswith("\n"):
                    sub_resource.append(sub_line)
                    sub_index += 1
                    sub_line = lines[sub_index]
                yield index, sub_resource


def extract_path_from_external_reosource(res: str):
    search_str = " path=\""
    res_str = "res://"
    path_idx = res.find(search_str)
    path_start = path_idx + len(search_str) + len(res_str)
    path_end = res.find("\"", path_start)
    return res[path_start:path_end]


def extract_id_from_external_resource(res: str):
    search_str = " id=\""
    id_idx = res.find(search_str)
    id_start = id_idx + len(search_str)
    id_end = res.find("\"", id_start)
    return res[id_start:id_end]


def extract_id_from_sub_resource(texture_line: str):
    search_str = "ExtResource(\""
    id_idx = texture_line.find(search_str)
    id_start = id_idx + len(search_str)
    id_end = texture_line.find("\"", id_start)
    return texture_line[id_start:id_end]


if __name__=="__main__":
    id_to_width_and_height = {}
    for res in get_external_resources(PATH_TO_LANDSCAPE_TILESET):
        path = extract_path_from_external_reosource(res)
        res_id = extract_id_from_external_resource(res)

        image_path = "/".join([PATH_TO_RES, path])
        width, height = get_image_size(image_path)
        id_to_width_and_height[res_id] = get_image_size(image_path)

    with open(PATH_TO_LANDSCAPE_TILESET, "r+") as file:
        lines = file.readlines()
        for index, sub_resource in get_sub_resources(PATH_TO_LANDSCAPE_TILESET):
            for offset, line in enumerate(sub_resource):
                if line.startswith("texture ="):
                    res_id = extract_id_from_sub_resource(line)

                if line.startswith("texture_region_size ="):
                    width, height = id_to_width_and_height[res_id]
                    new_line = f"texture_region_size = Vector2i({width}, {height})\n"
                    lines[index+offset] = new_line
        file.seek(0)
        file.truncate()
        file.writelines(lines)
