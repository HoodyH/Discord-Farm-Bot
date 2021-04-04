import aiohttp


def valid_image_url(url: str):
    image_extensions = ['png', 'jpg', 'jpeg', 'gif']
    for image_extension in image_extensions:
        if url.endswith('.' + image_extension):
            return True
    return False


# download the image into file like obj from a link
async def download_image(url: str, fp):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                fp.write(await resp.read())
