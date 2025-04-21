import json
from pytrends.request import TrendReq
from fastapi import FastAPI

app = FastAPI()

# Setup pytrends
pytrends = TrendReq(hl='en-US', tz=360)

@app.get("/api/daily-trends")
async def daily_trends(region: str = "india"):
    try:
        trends = pytrends.trending_searches(pn=region.lower())
        topics = trends[0:10][0].tolist()
        return {"region": region.upper(), "top_trending_topics": topics}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/related-topics")
async def related_topics(keyword: str):
    if not keyword:
        return {"error": "Please provide a keyword!"}

    try:
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='')
        related = pytrends.related_queries()
        rising = related[keyword]['rising']
        top_ideas = rising.head(10)['query'].tolist()
        return {"keyword": keyword, "related_topic_ideas": top_ideas}
    except Exception as e:
        return {"error": str(e)}
