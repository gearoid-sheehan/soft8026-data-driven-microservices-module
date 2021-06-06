db = db.getSiblingDB("analytics_db");
db.analytics_tb.drop();

db.analytics_tb.insert([
    {
        "id":40000,
        "Largest Post Title": "jsdsndaklsdnklasdnas",
        "Comment Count": "25",
        "Average No Comments": "77",
        "SourceKey": "RedditPost"
    }
]);