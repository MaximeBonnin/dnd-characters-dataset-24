import asyncio
import aiohttp
import backoff


@backoff.on_exception(backoff.expo,
                      aiohttp.ClientError,
                      max_tries=8,
                      giveup=lambda e: e.status == 404)
async def async_get(session, char_id, **kwargs):
    url = f"https://character-service.dndbeyond.com/character/v5/character/{char_id}/"
    async with session.get(url, **kwargs) as resp:
        if resp.status == 429:  # HTTP 429 is the status code for Too Many Requests
            raise aiohttp.ClientError
        data = await resp.json()
        return (char_id, resp.status, data)


async def get_chars_by_id(char_ids, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for c in char_ids:
            tasks.append(async_get(session=session, char_id=c, **kwargs))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    char_ids = range(25755028, 25755029)
    response_list = asyncio.run(get_chars_by_id(char_ids)) 
    print(response_list[0])