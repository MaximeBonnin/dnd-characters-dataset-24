import asyncio
import aiohttp


async def async_get(
    session: aiohttp.ClientSession,
    char_id: str,
    **kwargs
) -> dict:
    url = f"https://character-service.dndbeyond.com/character/v5/character/{char_id}/"
    #print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    data = await resp.json()
    #print(f"Received data for {char_id}: {resp.status}")
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