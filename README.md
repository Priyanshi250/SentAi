# Customer Feedback Analyzer with Gen Ai

The **Customer Feedback Analyzer** is a powerful web application that helps businesses analyze customer feedback using AI. It can identify sentiment, key themes, and suggest improvements based on uploaded CSV files containing customer reviews

## Features
- 📂 Upload CSV files with customer feedback data.
- 🔍 Choose your analysis focus:
  - Sentiment Analysis (Positive, Neutral, Negative)
  - Theme Identification (e.g., pricing, service, product qualitY.
  - Improvement Suggestions
  - All of the Above
- 🧠 AI-driven insights powered by Google's Gemini 2.0 API.(You Can use any Models of your intrest) 
  Create this Api key from Google studio [Link](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj39qiyioeMAxVohf0HHe5bJRsQmuEJegQIHRAB&url=https%3A%2F%2Faistudio.google.com%2Fapp%2Fapikey&usg=AOvVaw1WWenMsZaHnCnN4FhYRAe9&opi=89978449).

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/customer-feedback-analyzer.git
cd customer-feedback-analyzer
```

### 2. Install Dependencies (I have used Pycharm easy Venv & less Hassel)
Create a virtual environment and install the required packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` File
Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

> **⚠️ Important:** Keep your `.env` file private and never share your API key publicly.

---

## Usage

1. Run the app with the following command:
   ```bash
   streamlit run main.py
   ```
2. In the Streamlit interface:
   - Upload a CSV file containing customer feedback.
   - Select the column that holds the review data.
   - Choose your analysis focus (e.g., Sentiment Analysis, Theme Identification, etc.).
   - Click **"Analyze Feedback"** to generate insights.

For additional guidance on building Streamlit apps with LLMs, refer to the [Streamlit LLM Quickstart Guide](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/llm-quickstart).
---

## Future Improvements
- 📊 Add visualizations for sentiment distribution and key themes use can use matplot or pyplot 
- 📝 Support for additional data formats (e.g., Excel) and also change the temprature of the model.
- 🔄 Improved error handling and user guidance.
- Also make a report to save it as pdf 

---

## Contributing
Contributions are welcome! If you'd like to improve the app or add features, please fork the repo and submit a pull request. Caio

###App
![Project Screenshot](
/Screenshot_app.jpg)


## Contact
For questions or suggestions, feel free to reach out via [your contact details].
Happy Coding!!!
