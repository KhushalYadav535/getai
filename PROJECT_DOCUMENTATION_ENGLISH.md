# GetAI Life - Complete Project Documentation

## 📋 Project Overview

**GetAI Life** is an **AI Tools Directory Platform** where:
- Users can discover AI tools (like ChatGPT, DALL-E, etc.)
- AI tools are organized into categories
- Users can bookmark their favorite tools
- AI-powered chatbots (Healthcare and Finance) are available
- Latest AI news and research papers can be viewed
- Users can submit their own tools

**In Simple Terms**: This is a website where you can see all AI tools in one place, bookmark them, and chat with AI assistants.

---

## 🏗️ Technical Architecture

### Framework and Technology Stack:

1. **Backend**: Django 4.2.1 (Python web framework)
2. **Database**: SQLite3 (Development) / PostgreSQL (Production ready)
3. **AI/ML**: 
   - OpenAI GPT-3.5-turbo (For Chatbots)
   - LangChain (For AI chain processing)
4. **Web Scraping**: Selenium (For scraping tools and news)
5. **Caching**: Redis (For fast data access)
6. **Authentication**: Django AllAuth (Google login support)
7. **Frontend**: HTML, CSS, JavaScript, Bootstrap

---

## 📁 Project Structure

```
getai-life-main/
├── app_modules/          # Main application modules
│   ├── core/            # Core functionality
│   └── llm/             # AI/LLM related features (Chatbots)
├── scrap_data/          # Data scraping and tools management
├── users/               # User authentication and management
├── config/              # Django settings and configuration
├── templates/           # HTML templates
├── staticfiles/         # CSS, JS, Images
├── media/               # User uploaded files
└── requirements.txt     # Python dependencies
```

---

## 🗄️ Database Models

### 1. **User Model** (`users/models.py`)
- Email-based authentication
- Google OAuth support
- Email verification system
- Fields: `email`, `username`, `auth_provider`, `is_verify`

### 2. **Data Model** (`scrap_data/models.py`) - Main AI Tools
- **Fields**:
  - `title`: Tool name
  - `category`: Tool category (Design, Code, etc.)
  - `tag`: Multiple tags
  - `description`: Tool description
  - `image`: Tool image
  - `webpage`: Tool website URL
  - `is_featured`: Whether it's a featured tool
  - `click_count`: Number of clicks

### 3. **Category Model**
- Tool categories (Design, Code, Writing, etc.)
- Category images

### 4. **Tags Model**
- Tags for filtering tools

### 5. **Favourite Model**
- User's bookmarked tools
- Many-to-Many relationship with Data

### 6. **News Model**
- AI-related news articles
- Fields: `title`, `description`, `image`, `webpage`, `click_count`

### 7. **Research Model**
- Research papers/articles
- Fields: `title`, `subject`, `webpage`, `click_count`

### 8. **ToolSubmit Model**
- Tools submitted by users
- Fields: `full_name`, `tool_name`, `email`, `website`, `category`, `description`, `interested`

### 9. **Banner Model**
- Homepage banner content

---

## 🚀 Main Features

### 1. **AI Tools Directory** (`/`)
- List of all AI tools
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
- Users can submit their tools
- Form fields: Name, Tool Name, Email, Website, Category, Description

### 5. **User Authentication**
- **Registration**: With email and password
- **Login**: With email/username and password
- **Google OAuth**: Login with Google account
- **Email Verification**: Email verification required
- **Password Reset**: Forgot password functionality

### 6. **Bookmark System**
- Can bookmark tools after login
- Can view bookmarked tools on `/bookmark/` page

### 7. **AI Chatbots** (API Endpoints)
- **Healthcare Chatbot**: Doctor-like AI assistant
- **Finance Chatbot**: Financial advisor AI assistant
- Conversation memory (stored in Redis cache)

### 8. **Web Scraping**
- Functionality to scrape tools from GPTE.ai
- Functionality to scrape Google News

### 9. **Profile Picture Generator** (API)
- API to generate e-card/profile picture
- Image processing with PIL/Pillow

---

## 🔌 API Endpoints

### LLM/Chatbot APIs (`/api/v1/llm/`)

1. **Start Chat** (`POST /api/v1/llm/start-chat/`)
   - To start a chatbot
   - Parameters: `chat_bot_type` (Healthcare/Finance), `name`, `age`, `location`
   - Returns: `ai_message_content`, `user_chat_cache_key`

2. **Text Generation** (`POST /api/v1/llm/text-generation/`)
   - AI response to user message
   - Parameters: `user_chat_cache_key`, `human_message`
   - Returns: `ai_message_content`

3. **Chaining** (`POST /api/v1/llm/chaining/`)
   - Sequential chain processing (Advanced AI feature)
   - Chains multiple AI calls

4. **Agent Text Generation** (`POST /api/v1/llm/agent-text-generation/`)
   - AI agent with Google Search
   - Fetches real-time information

### Profile Picture API

5. **Profile Picture Generator** (`POST /image`)
   - To generate e-card
   - Parameters: `profile_image`, `name`, `designation`, `region_or_branch`
   - Returns: `image_url`

---

## 🛠️ How to Run the Project

### Prerequisites:
1. Python 3.8+ installed
2. Redis server running (for caching)
3. Chrome browser (for Selenium web scraping)
4. OpenAI API key (for chatbots)

### Steps:

1. **Create Virtual Environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup Environment Variables:**
Create `.env` file in project root:
```
DEBUG=True
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=localhost
```

4. **Run Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser (for Admin panel):**
```bash
python manage.py createsuperuser
```

6. **Start Redis Server:**
```bash
redis-server
```

7. **Start Development Server:**
```bash
python manage.py runserver
```

8. **Open in Browser:**
```
http://127.0.0.1:8000/
```

---

## 📦 Key Dependencies

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

## 🔐 Authentication Flow

1. **Registration:**
   - User enters email and password
   - System sends verification email
   - User verifies email
   - Account gets activated

2. **Login:**
   - Login with email/username and password
   - Or login with Google OAuth
   - Email verification required (for bookmarking)

3. **Password Reset:**
   - Forgot password link
   - Reset token sent via email
   - Can set new password

---

## 🤖 AI Chatbot Functionality

### Healthcare Chatbot:
- Responds like a Doctor with 15 years experience
- Personalized responses based on user profile (name, age, location)
- Provides medical articles and nearby pharmacy/hospital addresses
- Conversation history stored in Redis cache

### Finance Chatbot:
- Responds like a financial planner and wealth coach
- Provides financial advice
- Provides related articles and nearby banks/financial institutions
- Conversation history stored in Redis cache

### Technical Implementation:
- **Model**: GPT-3.5-turbo (OpenAI)
- **Temperature**: 1.0 (creative responses)
- **Max Tokens**: 250 (short responses)
- **Memory**: Conversation history in Redis cache
- **Cache Key Format**: `HEALTHCARE_{user_id}` or `FINANCE_{user_id}`

---

## 📊 Data Flow

### Tools Display Flow:
1. User visits homepage (`/`)
2. `DataListView` fetches all tools
3. Category/Tag/Search filters are applied
4. Paginated results are displayed (40 per page)
5. Next page loads via infinite scroll
6. User clicks on tool → `click_count` increases
7. User bookmarks → Added to `Favourite` model

### Chatbot Flow:
1. User starts chatbot → `StartChatAPIView`
2. System creates initial prompt (with user profile)
3. AI response is generated (OpenAI API call)
4. Conversation history stored in Redis cache
5. User sends next message → `TextGenerationAPIView`
6. Previous conversation history fetched (from cache)
7. New AI response is generated
8. Updated conversation history saved to cache

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
- `image/`: Images and icons
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
- Static files and media files configuration

### `config/urls.py`:
- Main URL routing
- Includes all app URLs

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

Django admin panel is available:
- URL: `/admin/`
- Access by creating superuser
- Can manage all models:
  - Data (Tools)
  - Category
  - Tags
  - News
  - Research
  - Users
  - ToolSubmit
  - Banner

---

## 🚨 Important Notes

1. **Email Verification**: Users must verify email for bookmark functionality
2. **Redis Cache**: Chatbot conversation history stored in Redis
3. **OpenAI API Key**: Must set `OPENAI_API_KEY` in `.env` file
4. **Selenium**: Chrome browser required for web scraping
5. **Database**: SQLite3 used in development, PostgreSQL recommended for production
6. **Static Files**: Must run `python manage.py collectstatic` in production

---

## 🔄 Migration History

Database migrations:
- `scrap_data/migrations/`: 26 migrations (Data model evolution)
- `users/migrations/`: 2 migrations (User model and EmailVerification)
- `config/migrations/`: 2 migrations (Initial setup)

---

## 🌐 Deployment (For Production)

### Required Changes:
1. `DEBUG = False` in settings.py
2. Add domain to `ALLOWED_HOSTS`
3. Setup PostgreSQL database
4. Setup Redis server
5. Collect static files: `python manage.py collectstatic`
6. Set environment variables properly
7. Setup SSL certificate (HTTPS)
8. Verify email SMTP configuration

### Recommended:
- Use Gunicorn or uWSGI as WSGI server
- Use Nginx as reverse proxy
- Use Supervisor for process management
- Setup monitoring and logging

---

## 👥 Team Roles and Responsibilities

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
- Content management (Add/Edit/Delete Tools, News, Research)
- User support
- Testing and feedback
- Marketing and promotion

---

## 📞 Support and Contact

- **Email**: getailife@sentientdigital.in
- **Domain**: https://getai.life
- **Admin Panel**: `/admin/`

---

## 🎯 Future Enhancements

1. User ratings and reviews for tools
2. Advanced search filters
3. Tool comparison feature
4. User profiles and dashboards
5. Newsletter subscription
6. Social media integration
7. Mobile app (React Native/Flutter)
8. More AI chatbot types
9. Analytics dashboard
10. API documentation (Swagger/OpenAPI)

---

## 📚 Learning Resources

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

This project is a comprehensive AI tools directory platform that:
- Organizes AI tools
- Provides user-friendly interface
- Offers AI-powered chatbots
- Displays latest news and research papers
- Provides user engagement features (bookmarks, submissions)

**Technology Stack**: Django, OpenAI, LangChain, Selenium, Redis, PostgreSQL/SQLite

**Main Features**: Tools Directory, News, Research, Chatbots, User Authentication, Bookmarks

**Target Audience**: AI enthusiasts, developers, researchers, general users interested in AI tools

---

**Documentation Created For**: Senior to Junior Level Developers and Non-Technical Team Members

**Last Updated**: 2024

**Version**: 1.0

---

## 🎓 Quick Start Guide for New Team Members

### For Developers:
1. Clone the project
2. Setup virtual environment
3. Install dependencies
4. Run database migrations
5. Create superuser
6. Start Redis
7. Run server
8. Explore and understand the code

### For Non-Technical Members:
1. Access admin panel
2. Learn to add/edit/delete Tools, News, Research
3. Understand user management
4. Manage content
5. Collect user feedback

---

**Happy Coding! 🚀**

