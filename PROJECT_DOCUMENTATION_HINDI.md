# GetAI Life - प्रोजेक्ट की पूरी जानकारी (Complete Project Documentation)

## 📋 प्रोजेक्ट क्या है? (What is this Project?)

**GetAI Life** एक **AI Tools Directory Platform** है जहाँ:
- Users AI tools खोज सकते हैं (जैसे ChatGPT, DALL-E, etc.)
- AI tools को categories में organize किया गया है
- Users अपने favorite tools को bookmark कर सकते हैं
- AI-powered chatbots (Healthcare और Finance) available हैं
- Latest AI news और research papers देख सकते हैं
- Users अपने tools submit कर सकते हैं

**सरल भाषा में**: यह एक website है जहाँ आप सभी AI tools एक जगह देख सकते हैं, उन्हें bookmark कर सकते हैं, और AI chatbots से बात कर सकते हैं।

---

## 🏗️ प्रोजेक्ट की Architecture (Technical Architecture)

### Framework और Technology Stack:

1. **Backend**: Django 4.2.1 (Python web framework)
2. **Database**: SQLite3 (Development) / PostgreSQL (Production ready)
3. **AI/ML**: 
   - OpenAI GPT-3.5-turbo (Chatbot के लिए)
   - LangChain (AI chain processing के लिए)
4. **Web Scraping**: Selenium (Tools और News scrape करने के लिए)
5. **Caching**: Redis (Fast data access के लिए)
6. **Authentication**: Django AllAuth (Google login support)
7. **Frontend**: HTML, CSS, JavaScript, Bootstrap

---

## 📁 प्रोजेक्ट Structure (File Structure)

```
getai-life-main/
├── app_modules/          # Main application modules
│   ├── core/            # Core functionality
│   └── llm/             # AI/LLM related features (Chatbots)
├── scrap_data/          # Data scraping और tools management
├── users/               # User authentication और management
├── config/              # Django settings और configuration
├── templates/           # HTML templates
├── staticfiles/         # CSS, JS, Images
├── media/               # User uploaded files
└── requirements.txt     # Python dependencies
```

---

## 🗄️ Database Models (Database Structure)

### 1. **User Model** (`users/models.py`)
- Email-based authentication
- Google OAuth support
- Email verification system
- Fields: `email`, `username`, `auth_provider`, `is_verify`

### 2. **Data Model** (`scrap_data/models.py`) - Main AI Tools
- **Fields**:
  - `title`: Tool का नाम
  - `category`: Tool की category (Design, Code, etc.)
  - `tag`: Multiple tags
  - `description`: Tool की description
  - `image`: Tool की image
  - `webpage`: Tool की website URL
  - `is_featured`: Featured tool है या नहीं
  - `click_count`: कितनी बार click हुआ

### 3. **Category Model**
- Tool categories (Design, Code, Writing, etc.)
- Category images

### 4. **Tags Model**
- Tags for filtering tools

### 5. **Favourite Model**
- User के bookmarked tools
- Many-to-Many relationship with Data

### 6. **News Model**
- AI-related news articles
- Fields: `title`, `description`, `image`, `webpage`, `click_count`

### 7. **Research Model**
- Research papers/articles
- Fields: `title`, `subject`, `webpage`, `click_count`

### 8. **ToolSubmit Model**
- Users द्वारा submit किए गए tools
- Fields: `full_name`, `tool_name`, `email`, `website`, `category`, `description`, `interested`

### 9. **Banner Model**
- Homepage banner content

---

## 🚀 Main Features (मुख्य Features)

### 1. **AI Tools Directory** (`/`)
- सभी AI tools की list
- Category-wise filtering
- Search functionality
- Tag-based filtering
- Pagination (40 items per page)
- Infinite scroll
- Bookmark functionality (login required)
- Click tracking

### 2. **News Section** (`/news/`)
- Latest AI news
- Search functionality
- Click tracking

### 3. **Research Section** (`/research/`)
- AI research papers
- Search functionality
- Click tracking

### 4. **Tool Submission** (`/submit/`)
- Users अपने tools submit कर सकते हैं
- Form fields: Name, Tool Name, Email, Website, Category, Description

### 5. **User Authentication**
- **Registration**: Email और password से
- **Login**: Email/Username और password से
- **Google OAuth**: Google account से login
- **Email Verification**: Email verify करना जरूरी है
- **Password Reset**: Forgot password functionality

### 6. **Bookmark System**
- Login करने के बाद tools को bookmark कर सकते हैं
- Bookmarked tools `/bookmark/` page पर देख सकते हैं

### 7. **AI Chatbots** (API Endpoints)
- **Healthcare Chatbot**: Doctor-like AI assistant
- **Finance Chatbot**: Financial advisor AI assistant
- Conversation memory (Redis cache में store होता है)

### 8. **Web Scraping**
- GPTE.ai से tools scrape करने की functionality
- Google News scrape करने की functionality

### 9. **Profile Picture Generator** (API)
- E-card/profile picture generate करने का API
- Image processing with PIL/Pillow

---

## 🔌 API Endpoints (API Routes)

### LLM/Chatbot APIs (`/api/v1/llm/`)

1. **Start Chat** (`POST /api/v1/llm/start-chat/`)
   - Chatbot शुरू करने के लिए
   - Parameters: `chat_bot_type` (Healthcare/Finance), `name`, `age`, `location`
   - Returns: `ai_message_content`, `user_chat_cache_key`

2. **Text Generation** (`POST /api/v1/llm/text-generation/`)
   - User message के जवाब में AI response
   - Parameters: `user_chat_cache_key`, `human_message`
   - Returns: `ai_message_content`

3. **Chaining** (`POST /api/v1/llm/chaining/`)
   - Sequential chain processing (Advanced AI feature)
   - Multiple AI calls को chain करता है

4. **Agent Text Generation** (`POST /api/v1/llm/agent-text-generation/`)
   - Google Search के साथ AI agent
   - Real-time information fetch करता है

### Profile Picture API

5. **Profile Picture Generator** (`POST /image`)
   - E-card generate करने के लिए
   - Parameters: `profile_image`, `name`, `designation`, `region_or_branch`
   - Returns: `image_url`

---

## 🛠️ How to Run the Project (प्रोजेक्ट कैसे चलाएं)

### Prerequisites:
1. Python 3.8+ installed
2. Redis server running (for caching)
3. Chrome browser (for Selenium web scraping)
4. OpenAI API key (for chatbots)

### Steps:

1. **Virtual Environment बनाएं:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. **Dependencies install करें:**
```bash
pip install -r requirements.txt
```

3. **Environment Variables setup करें:**
`.env` file बनाएं project root में:
```
DEBUG=True
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=localhost
```

4. **Database migrations run करें:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Superuser बनाएं (Admin panel के लिए):**
```bash
python manage.py createsuperuser
```

6. **Redis server start करें:**
```bash
redis-server
```

7. **Development server start करें:**
```bash
python manage.py runserver
```

8. **Browser में खोलें:**
```
http://127.0.0.1:8000/
```

---

## 📦 Key Dependencies (मुख्य Libraries)

### Backend:
- **Django 4.2.1**: Main web framework
- **django-allauth 0.54.0**: Authentication (Google OAuth)
- **djangorestframework 3.14.0**: REST API framework
- **langchain**: AI chain processing
- **openai**: OpenAI API integration
- **selenium 4.10.0**: Web scraping
- **redis**: Caching
- **Pillow 9.5.0**: Image processing
- **psycopg2-binary 2.9.6**: PostgreSQL database adapter

### Frontend:
- **Bootstrap**: CSS framework
- **jQuery**: JavaScript library
- **Waypoints.js**: Infinite scroll
- **Font Awesome**: Icons

---

## 🔐 Authentication Flow (Login Process)

1. **Registration:**
   - User email और password enter करता है
   - System verification email भेजता है
   - User email verify करता है
   - Account activate होता है

2. **Login:**
   - Email/Username और password से login
   - या Google OAuth से login
   - Email verified होना जरूरी है (bookmark के लिए)

3. **Password Reset:**
   - Forgot password link
   - Reset token email में भेजा जाता है
   - New password set कर सकते हैं

---

## 🤖 AI Chatbot Functionality

### Healthcare Chatbot:
- 15 years experience के Doctor की तरह respond करता है
- User profile (name, age, location) के आधार पर personalized responses
- Medical articles और nearby pharmacy/hospital addresses provide करता है
- Conversation history Redis cache में store होता है

### Finance Chatbot:
- Financial planner और wealth coach की तरह respond करता है
- Financial advice देता है
- Related articles और nearby banks/financial institutions provide करता है
- Conversation history Redis cache में store होता है

### Technical Implementation:
- **Model**: GPT-3.5-turbo (OpenAI)
- **Temperature**: 1.0 (creative responses)
- **Max Tokens**: 250 (short responses)
- **Memory**: Redis cache में conversation history
- **Cache Key Format**: `HEALTHCARE_{user_id}` या `FINANCE_{user_id}`

---

## 📊 Data Flow (Data कैसे flow होता है)

### Tools Display Flow:
1. User homepage (`/`) पर जाता है
2. `DataListView` सभी tools fetch करता है
3. Category/Tag/Search filters apply होते हैं
4. Paginated results display होते हैं (40 per page)
5. Infinite scroll से next page load होता है
6. User tool पर click करता है → `click_count` increase होता है
7. User bookmark करता है → `Favourite` model में add होता है

### Chatbot Flow:
1. User chatbot start करता है → `StartChatAPIView`
2. System initial prompt create करता है (user profile के साथ)
3. AI response generate होता है (OpenAI API call)
4. Conversation history Redis cache में store होता है
5. User next message भेजता है → `TextGenerationAPIView`
6. Previous conversation history fetch होता है (cache से)
7. New AI response generate होता है
8. Updated conversation history cache में save होता है

---

## 🎨 Frontend Structure

### Templates:
- `base.html`: Main template (header, footer)
- `home.html`: Tools listing page
- `news.html`: News listing page
- `research.html`: Research listing page
- `favourite.html`: Bookmarked tools page
- `submit.html`: Tool submission form
- `auth/login.html`: Login page
- `auth/register.html`: Registration page
- `auth/forgot_password.html`: Password reset page
- `health-care-chat-bot.html`: Healthcare chatbot page
- `tribe.html`: Tribe page

### Static Files:
- `css/style.css`: Main stylesheet
- `css/responsive.css`: Responsive design
- `js/custom.js`: Custom JavaScript
- `image/`: Images और icons
- `fonts/`: Custom fonts

---

## 🔧 Configuration Files

### `config/settings.py`:
- Django settings
- Database configuration
- Redis cache configuration
- Email configuration (SMTP)
- Google OAuth credentials
- CORS settings
- Static files और media files configuration

### `config/urls.py`:
- Main URL routing
- All app URLs include करता है

---

## 🧪 Testing

### Test Files:
- `scrap_data/tests.py`: Data model tests
- `users/tests.py`: User authentication tests
- `app_modules/llm/tests.py`: LLM functionality tests
- `app_modules/core/tests.py`: Core functionality tests

### Run Tests:
```bash
python manage.py test
```

---

## 📝 Admin Panel

Django admin panel available है:
- URL: `/admin/`
- Superuser बनाकर access कर सकते हैं
- सभी models manage कर सकते हैं:
  - Data (Tools)
  - Category
  - Tags
  - News
  - Research
  - Users
  - ToolSubmit
  - Banner

---

## 🚨 Important Notes (महत्वपूर्ण बातें)

1. **Email Verification**: Users को email verify करना जरूरी है bookmark functionality के लिए
2. **Redis Cache**: Chatbot conversation history Redis में store होता है
3. **OpenAI API Key**: `.env` file में `OPENAI_API_KEY` set करना जरूरी है
4. **Selenium**: Web scraping के लिए Chrome browser required है
5. **Database**: Development में SQLite3 use हो रहा है, Production में PostgreSQL use करना चाहिए
6. **Static Files**: Production में `python manage.py collectstatic` run करना जरूरी है

---

## 🔄 Migration History

Database migrations:
- `scrap_data/migrations/`: 26 migrations (Data model evolution)
- `users/migrations/`: 2 migrations (User model और EmailVerification)
- `config/migrations/`: 2 migrations (Initial setup)

---

## 🌐 Deployment (Production के लिए)

### Required Changes:
1. `DEBUG = False` in settings.py
2. `ALLOWED_HOSTS` में domain add करें
3. PostgreSQL database setup करें
4. Redis server setup करें
5. Static files collect करें: `python manage.py collectstatic`
6. Environment variables properly set करें
7. SSL certificate setup करें (HTTPS)
8. Email SMTP configuration verify करें

### Recommended:
- Use Gunicorn या uWSGI as WSGI server
- Use Nginx as reverse proxy
- Use Supervisor for process management
- Setup monitoring और logging

---

## 👥 Team Roles और Responsibilities

### Senior Developers:
- Architecture decisions
- Complex features implementation
- Code review
- Performance optimization
- Security implementation

### Junior Developers:
- Feature implementation
- Bug fixes
- UI/UX improvements
- Testing
- Documentation

### Non-Technical Team Members:
- Content management (Tools, News, Research add करना)
- User support
- Testing और feedback
- Marketing और promotion

---

## 📞 Support और Contact

- **Email**: getailife@sentientdigital.in
- **Domain**: https://getai.life
- **Admin Panel**: `/admin/`

---

## 🎯 Future Enhancements (भविष्य में जोड़े जा सकने वाले Features)

1. User ratings और reviews for tools
2. Advanced search filters
3. Tool comparison feature
4. User profiles और dashboards
5. Newsletter subscription
6. Social media integration
7. Mobile app (React Native/Flutter)
8. More AI chatbot types
9. Analytics dashboard
10. API documentation (Swagger/OpenAPI)

---

## 📚 Learning Resources (सीखने के लिए Resources)

### Django:
- Official Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/

### AI/LLM:
- OpenAI API Documentation: https://platform.openai.com/docs
- LangChain Documentation: https://python.langchain.com/

### Frontend:
- Bootstrap Documentation: https://getbootstrap.com/
- jQuery Documentation: https://api.jquery.com/

---

## ✅ Conclusion

यह project एक comprehensive AI tools directory platform है जो:
- AI tools को organize करता है
- User-friendly interface provide करता है
- AI-powered chatbots offer करता है
- Latest news और research papers display करता है
- User engagement features (bookmarks, submissions) provide करता है

**Technology Stack**: Django, OpenAI, LangChain, Selenium, Redis, PostgreSQL/SQLite

**Main Features**: Tools Directory, News, Research, Chatbots, User Authentication, Bookmarks

**Target Audience**: AI enthusiasts, developers, researchers, general users interested in AI tools

---

**Documentation Created For**: Senior to Junior Level Developers और Non-Technical Team Members

**Last Updated**: 2024

**Version**: 1.0

---

## 🎓 Quick Start Guide for New Team Members

### For Developers:
1. Project clone करें
2. Virtual environment setup करें
3. Dependencies install करें
4. Database migrations run करें
5. Superuser create करें
6. Redis start करें
7. Server run करें
8. Code explore करें और समझें

### For Non-Technical Members:
1. Admin panel access लें
2. Tools, News, Research add/edit/delete करना सीखें
3. User management समझें
4. Content management करें
5. User feedback collect करें

---

**Happy Coding! 🚀**

