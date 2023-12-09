import json


class SaveToJsonException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


FILENAME_HISTORY = "data.json"


def create_file_json():
    data_from_file = []
    with open(FILENAME_HISTORY, "w") as file:
        json.dump(data_from_file, file)


def delete_history():
    try:
        with open(FILENAME_HISTORY, "w") as file:
            file.write(json.dumps([], indent=4, ensure_ascii=False))
            print("\nИстория прогноза погоды удалена.")
    except Exception:
        raise SaveToJsonException(
            "Проблема с удалением данных. Приносим свои извинения."
        )


def read_json():
    try:
        with open(FILENAME_HISTORY, "r+") as file:
            data_from_file = json.load(file)
        return data_from_file
    except FileNotFoundError:
        create_file_json()
    except Exception:
        raise SaveToJsonException("Проблемы с чтением данных. Приносим свои извинения.")


def write_to_json(data: dict) -> None:
    list_to_json = read_json()
    try:
        with open(FILENAME_HISTORY, "w+") as file:
            if list_to_json is None or list_to_json == "":
                list_to_json = []
            list_to_json.append(data)
            json.dump(
                list_to_json,
                file,
                indent=4,
                ensure_ascii=True,
            )
    except Exception:
        raise SaveToJsonException(
            "Проблемы с сохранением в базу данных. Приносим свои извинения."
        )
