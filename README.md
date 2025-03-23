# AI-Powered Telegram Bot for Community Management

A Telegram bot that automates community engagement, announcements, and updates for Systemic Altruism, featuring AI-powered interactions and creative features to enhance user experience.

## Bot Information
- **Bot Name**: CM
- **Telegram Username**: @SACommunityManagementbot

## Features

### Core Features
- **Community Management**: Member onboarding, FAQ responses, and automated replies
- **Admin Controls**: Announcement system and scheduled updates
- **AI-Powered Interactions**: Natural language processing using Huggingface API

### Database & Automation
- User data and message storage
- Automated welcome messages and event reminders
- Scheduled community updates using AsyncIO And also motivational messages everyday generated using AI.

### Creative Features
- **Sentiment Analysis**: Community pulse tracking via APIVerve
- **Gamification**: Leaderboard for community engagement
- **AI-Generated Content**: Contextual and personalized responses

## Project Structure
```
telegram_community_bot/
├── ai/
│   ├── __init__.py
│   └── nlp_processor.py
├── bot/
│   ├── __init__.py
│   ├── commands.py
│   ├── handlers.py
│   └── scheduler.py
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── operations.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Telegram account
- Huggingface API key - I used the "/models/facebook/blenderbot-3B" from huggingface
- Database setup (Firebase/MongoDB/PostgreSQL) - I have used Firebase

### Environment Variables
Create a `.env` file with the following:
```
TELEGRAM_TOKEN=your_telegram_bot_token
HUGGINGFACE_API_KEY=your_huggingface_api_key
APIVERVE_KEY=your_apiverve_key
FIREBASE_CREDENTIALS=json_file_path or paste the content of that file in a string ' ' in single line
```

### Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/itsnishant-306/AI-Powered-Telegram-Bot-for-Community-Management.git
cd AI-Powered-Telegram-Bot-for-Community-Management
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the bot locally:
```bash
python main.py
```

## Bot Commands

- `/start` - Initialize the bot and receive welcome message
- `/help` - View available commands and usage information
- `/about` - Learn about Systemic Altruism
- `/faq` - Access frequently asked questions
- `/leaderboard` - View community engagement leaderboard
- `/sentiment` - for sentiment analysis
- `/announce` - For Admins only for announcements
- Type your questions and anything you'd want to ask, It's AI powered - ready to conquer your doubts.

#### Bot Information
![Screenshot 2025-03-23 185017](https://github.com/user-attachments/assets/be624715-5b24-4dab-a52d-3eb12417c5f8)

### Result to various commands and prompts to check the functionality of the bot
#### /Start | Asking "hello, how are you?" to check NLP usage and AI response
![Screenshot 2025-03-23 185122](https://github.com/user-attachments/assets/1860e823-1311-4181-907c-70f29bbad54d)

#### /help | /about | /faq 
![Screenshot 2025-03-23 185155](https://github.com/user-attachments/assets/844e7230-c05e-42e7-8428-74d2cb6aea33)

#### /announce | Some random question | Automated Scheduled updates and daily motivation message from AI
![Screenshot 2025-03-23 185220](https://github.com/user-attachments/assets/2f50981a-78d5-40d8-a6f4-a44114cecc51)

#### /leaderboard | /sentiment 
![Screenshot 2025-03-23 185248](https://github.com/user-attachments/assets/2eb4e64a-c2db-4e2a-be40-7d7e5679ea20)



## Deployment

This bot is deployed on Render.

### Render Deployment
1. Create a Render account and connect your GitHub repository
2. Create a new Web Service pointing to your repository
3. Set up environment variables in the Render dashboard
4. Deploy the application

### I am currently facing errors in deployment, but goodnews is that bot works perfectly fine. 

## Technical Implementation

### Architecture
- Bot interaction layer (Telegram Bot API)
- Business logic layer (command handlers, message processors)
- AI integration layer (Huggingface API)
- Data persistence layer
- Asynchronous scheduling using aioscheduler

### AI Features
The bot uses Huggingface models to:
- Generate contextual responses to user queries
- Process and understand natural language commands
- Support intelligent community interactions

### Sentiment Analysis
- Uses APIVerve's sentiment analysis to track community mood
- Provides insights into community engagement trends
- Helps administrators understand community response

### Database Structure
- User profiles and engagement metrics
- Chat history and interaction logs
- Scheduled announcements and events

## Future Enhancements
- Multi-language support
- Voice message transcription and processing
- Community voting and polling features
- Integration with additional AI services
- Advanced analytics dashboard

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements
- python-telegram-bot
- Huggingface
- APIVerve
- AsyncIO and aioscheduler
