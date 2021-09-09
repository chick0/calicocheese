def is_image(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower()
    image_ext = [
        'png',
        'apng',
        'jpg',
        'jpeg',
        'gif',
        'svg',
        'webp',
        'ico',
        'heif',
    ]

    return ext in image_ext


def is_video(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower()
    image_ext = [
        'avi',
        'wmv',
        'mov',
        'webm',
        'mp4',
    ]

    return ext in image_ext
