import os, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "cat_model.pkl")

def train_example():
    texts = [
    # tech
    "Apple launches new iPhone with AI features",
    "Microsoft announces Windows 12 update",
    "Google unveils new search AI model",
    "AI improves medical diagnosis accuracy",
    "Tesla develops self-driving car update",
    "Amazon introduces smart home devices",
    "New chip boosts computer performance",
    "Meta rolls out VR headset",
    "Scientists advance quantum computing",
    "Robotics startup raises funding",
    "Samsung reveals foldable phone upgrade",
    "Apple develops mixed reality headset",
    "AI chatbot passes university exam",
    "Google launches new cloud platform",
    "Tesla unveils next-gen battery",
    "SpaceX rocket carries satellites into orbit",
    "Scientists create faster AI chips",
    "Microsoft invests in gaming studio",
    "Cybersecurity firm detects major breach",
    "5G networks expand worldwide",

    # finance
    "Stock markets rally after earnings",
    "Bitcoin price surges to record high",
    "Federal Reserve raises interest rates",
    "Investors worried about inflation",
    "Oil prices fall amid global slowdown",
    "Banks tighten lending rules",
    "Gold prices hit new highs",
    "Global recession fears grow",
    "Housing market shows signs of recovery",
    "Unemployment rates fall in US",
    "Central Bank introduces digital currency",
    "Stock market drops after weak jobs data",
    "Investors shift focus to renewable energy",
    "Cryptocurrency exchange faces regulation",
    "Major bank reports record profits",
    "Bond yields rise amid uncertainty",
    "Insurance companies see higher claims",
    "Corporate earnings beat expectations",
    "Startups attract venture capital",
    "Currency markets show volatility",

    # sports
    "Local team wins the championship game",
    "Cristiano Ronaldo scores a hat-trick",
    "Olympics postponed due to pandemic",
    "Tennis star wins grand slam",
    "Basketball finals attract global viewers",
    "India beats Pakistan in cricket match",
    "Formula 1 driver claims victory",
    "Athletics world record broken",
    "FIFA announces World Cup venues",
    "NBA star retires after long career",
    "World Cup final draws record audience",
    "Boxing champion defends his title",
    "Marathon runner sets new record",
    "National team qualifies for tournament",
    "NBA finals game goes into overtime",
    "Football star suffers serious injury",
    "Swimmer wins multiple gold medals",
    "Tennis rivalry intensifies at Wimbledon",
    "Hockey league announces expansion",
    "Golf tournament ends in dramatic finish",

    # politics
    "Government passes new tax law",
    "President meets with world leaders",
    "Elections scheduled for next month",
    "Parliament debates climate bill",
    "Senator proposes healthcare reform",
    "Prime Minister addresses the nation",
    "Political tensions rise in Middle East",
    "Supreme Court issues major ruling",
    "Protests erupt over government policy",
    "Diplomatic talks held at UN",
    "Government launches new education policy",
    "Lawmakers debate immigration reform",
    "Senate passes defense spending bill",
    "President signs international trade deal",
    "Protests spread across major cities",
    "Opposition party gains momentum",
    "Elections see record voter turnout",
    "Minister resigns after corruption scandal",
    "Leaders hold talks on climate action",
    "Court overturns controversial law",

    # world
    "Scientists publish climate change findings",
    "Earthquake hits Japan, many casualties",
    "UN summit addresses global security",
    "Wildfires spread across Australia",
    "Floods displace thousands in India",
    "Hurricane causes devastation in US",
    "Refugee crisis worsens in Europe",
    "Global warming impacts Arctic ice",
    "Pandemic continues to affect travel",
    "Humanitarian aid sent to Africa",
    "Volcano eruption forces evacuations",
    "Heatwave grips Europe this summer",
    "Global summit discusses food security",
    "Typhoon causes flooding in Philippines",
    "Scientists warn of rising sea levels",
    "Refugees seek shelter after conflict",
    "International aid sent to earthquake zone",
    "Severe drought affects African countries",
    "Peace talks resume between nations",
    "Wildlife populations decline worldwide"
    ]


    labels = (
        ["tech"]*20 +
        ["finance"]*20 +
        ["sports"]*20 +
        ["politics"]*20 +
        ["world"]*20
    )

    v = TfidfVectorizer(max_features=3000, ngram_range=(1,2))
    X = v.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, labels)
    model = {"vectorizer": v, "clf": clf}
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH,"rb") as f:
            return pickle.load(f)
    return train_example()

def categorizer_agent(state: dict, params: dict = None) -> dict:
    model = load_model()
    v = model["vectorizer"]
    clf = model["clf"]

    articles = state.get("articles", [])
    for a in articles:
        text = (a.get("summary") or a.get("title") or "")[:2000]
        if text.strip():
            pred = clf.predict(v.transform([text]))[0]
            a["category"] = pred
        else:
            a["category"] = "uncategorized"

    state["articles"] = articles
    return state
