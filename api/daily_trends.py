import json
from pytrends.request import TrendReq

def handler(request):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Daily trends endpoint
    if request.path == '/api/daily-trends':
        region = request.args.get('region', 'india')  # Default is 'india'
        try:
            trends = pytrends.trending_searches(pn=region.lower())
            topics = trends[0:10][0].tolist()
            return json.dumps({
                "region": region.upper(),
                "top_trending_topics": topics
            })
        except Exception as e:
            return json.dumps({"error": str(e)}), 500

    # Related topics endpoint
    elif request.path == '/api/related-topics':
        keyword = request.args.get('keyword')
        if not keyword:
            return json.dumps({"error": "Please provide a keyword!"}), 400

        try:
            pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='')
            related = pytrends.related_queries()
            rising = related[keyword]['rising']
            top_ideas = rising.head(10)['query'].tolist()
            return json.dumps({
                "keyword": keyword,
                "related_topic_ideas": top_ideas
            })
        except Exception as e:
            return json.dumps({"error": str(e)}), 500

    return json.dumps({"error": "Invalid route"}), 404
