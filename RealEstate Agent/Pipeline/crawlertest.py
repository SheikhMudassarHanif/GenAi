# Install with pip install firecrawl-py
import asyncio
from firecrawl import AsyncFirecrawlApp, ScrapeOptions
from sympy import pretty_print
from langchain_core.tools import tool

# @tool
async def WebSearch()->str:
    """This searches about the address on the google and returns the top results"""
    app = AsyncFirecrawlApp(api_key='')
    response = await app.search(
        query='Find commerical properties in lawyers Rd charlotte,NC listed on crexi'
            ,
        limit=3,
        scrape_options=ScrapeOptions(formats=['links', 'markdown'])
    )
    print(response)
    return response

asyncio.run(WebSearch())